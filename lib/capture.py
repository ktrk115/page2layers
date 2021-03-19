import time
from PIL import Image
from io import BytesIO
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait

from lib import element as lib_element
from lib.javascript import snippet as js
from lib.webdriver import get_chrome_driver, send
from lib.parse import \
    build_element_tree, get_ordered_elements, get_inner_html
from lib.util import \
    check_broken_link, get_image_hash, remove_redundant_elements, \
    get_reconstruct_image, get_tree_image, save_metadata


class ScreenCapturer(object):
    def __init__(self, window_size, headless=False, extension=None):
        self.driver = get_chrome_driver(window_size,
                                        headless=headless,
                                        extension=extension)
        self.driver.implicitly_wait(10)
        self.window_size = window_size
        self.headless = headless

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.driver.quit()

    def get_page(self, url):
        self.driver.get(url)
        time.sleep(1)

        self.driver.execute_script(js['stop_animation'])
        self.driver.execute_script(js['remove_invalid_head'])
        self.driver.execute_script(js['remove_scrollbar'])
        self.driver.execute_script(js['scroll_to_top'])

        if not self.headless:
            window_size = self.driver.execute_script(js['compute_real_window_size'],
                                                     *self.window_size)
            self.driver.set_window_size(*window_size)

        def compare_source():
            source_1 = self.driver.page_source
            time.sleep(5)
            source_2 = self.driver.page_source
            if source_1 == source_2:
                return source_1
            else:
                return False

        self.source = WebDriverWait(self.driver, 60).until(
            lambda _: compare_source(), "Unstable page source")
        self.inner_html = get_inner_html(self.source)

        # check http status and stylesheet
        user_agent = self.driver.execute_script(js['get_user_agent'])
        self.headers = {'User-Agent': user_agent, 'Referer': url}
        check_broken_link(self.driver.current_url, self.headers)

        css_urls = self.driver.execute_script(js['get_stylesheet_links'])
        for css_url in css_urls:
            if css_url is not None:
                check_broken_link(css_url, self.headers)

    def restore_page(self):
        self.driver.execute_script(
            'document.querySelector("html").innerHTML = arguments[0]',
            self.inner_html,
        )

    def screenshot(self):
        with BytesIO(self.driver.get_screenshot_as_png()) as f:
            return Image.open(f).resize(self.window_size, 1)

    def get_element_image(self, target_element, visible_elements):
        style = target_element.color_style
        ancestors = target_element.ancestors

        send(self.driver,
             "Emulation.setDefaultBackgroundColorOverride",
             {'color': {'r': 0, 'g': 0, 'b': 0, 'a': 0}})

        # change style
        for element in visible_elements:
            if element in ancestors:
                element.make_transparent()
            elif element == target_element:
                element.set_style(style)
            else:
                element.make_invisible()

        # verify style
        for element in visible_elements:
            if element in ancestors:
                element.verify_transparent()
            elif element == target_element:
                element.verify_style(style)
            else:
                element.verify_invisible()

        img = self.screenshot()

        send(self.driver,
             'Emulation.setDefaultBackgroundColorOverride')

        return img

    def download_images(self, element, out_dir):
        def check_and_save(img_repr, out_path):
            img_url = img_repr.replace('url("', '').replace('")', '')
            if img_url[:4] == 'http':
                content = check_broken_link(image_url, self.headers, return_content=True)
                with Image.open(BytesIO(content)) as img:
                    img.save(out_path)
            elif img_url == 'none':
                pass
            else:
                raise NotImplementedError(img_url)

        key = 'background-image'
        img_reprs = element.get_style([key])[key].split(', ')
        for i, img_repr in enumerate(img_reprs):
            out_path = out_dir / f'{element.index}_bg-{i}.png'
            check_and_save(img_repr, out_path)

        if element.name == 'img':
            script = 'return arguments[0].src'
            img_repr = self.driver.execute_script(script, element.find())
            out_path = out_dir / f'{element.index}_img.png'
            check_and_save(img_repr, out_path)

    def capture(self, url, out_dir):
        self.get_page(url)

        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        img = self.screenshot()
        img.save(out_dir / 'screenshot.png')
        self.img_hash = get_image_hash(img)

        lib_element.set_driver(self.driver)
        root = build_element_tree(self.source)
        elements = get_ordered_elements(root)
        visible_elements = [e for e in elements if e.is_visible]

        for element in visible_elements:
            self.restore_page()
            img = self.get_element_image(element, visible_elements)
            element.set_image(img)
        self.restore_page()
        visible_elements = [e for e in visible_elements if e.is_visible]

        remove_redundant_elements(root, visible_elements)

        # save images and metadata
        for i, element in enumerate(visible_elements):
            self.download_images(element, out_dir)
            element.z_order = i
            out_path = out_dir / f'{element.index}.png'
            element.img.save(out_path)

        save_metadata(root, out_dir / 'metadata.json')

        img = get_tree_image(root)
        img.save(out_dir / 'tree.png')

        img = get_reconstruct_image(root, self.window_size)
        img.save(out_dir / 'recon.png')

        recon_error = get_image_hash(img) - self.img_hash
        return '\t'.join([url, 'Success', f'ReconError: {recon_error}'])
