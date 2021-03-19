from anytree import NodeMixin
from selenium.webdriver.support.ui import WebDriverWait

from lib.javascript import snippet as js


TRANSPARENT_STYLE = {
    'color': 'rgba(0, 0, 0, 0)',
    'background-color': 'rgba(0, 0, 0, 0)',
    'background-image': 'none',
    'border-style': 'hidden',
    'box-shadow': 'none',
}
INVISIBLE_STYLE = TRANSPARENT_STYLE.copy()
INVISIBLE_STYLE.update({'visibility': 'hidden'})


class Base(NodeMixin):
    __index = 0
    driver = None

    def __init__(self, selector, parent, ctx_parent):
        self.selector = selector
        self.name = selector.split(' > ')[-1].split(':')[0]
        self.img = None

        self.parent = parent
        if parent is None:
            Base.__index = 0

        self.ctx_parent = ctx_parent
        self.ctx_children = []
        if ctx_parent is not None:
            ctx_parent.ctx_children.append(self)

        self.index = Base.__index
        Base.__index += 1

        keys = TRANSPARENT_STYLE.keys()
        self.color_style = self.get_style(keys)
        self.z_value = self.get_z_value()
        self.has_background = self.check_has_background()

    def __str__(self):
        return self.selector

    def find(self):
        return self.driver.find_element_by_css_selector(self.selector)

    def get_z_value(self):
        z = 0.
        style = self.get_style(['position', 'z-index'])
        if style['position'] != 'static':
            if style['z-index'] != 'auto':
                z = float(style['z-index'])
        return z

    def get_style(self, keys):
        raise NotImplementedError

    def set_style(self, style):
        raise NotImplementedError

    def verify_style(self, style):
        raise NotImplementedError

    def make_transparent(self):
        self.set_style(TRANSPARENT_STYLE)

    def verify_transparent(self):
        self.verify_style(TRANSPARENT_STYLE)

    def make_invisible(self):
        self.set_style(INVISIBLE_STYLE)

    def verify_invisible(self):
        self.verify_style(INVISIBLE_STYLE)

    def set_image(self, img):
        bbox = img.getbbox()
        if bbox is not None:
            self.img = img.crop(bbox)
            self.box = bbox
        else:
            self.is_visible = False

    def check_has_background(self):
        k_img = 'background-image'
        k_color = 'background-color'
        style = self.get_style([k_img, k_color])
        return style[k_img] != 'none' or \
            style[k_color] != 'rgba(0, 0, 0, 0)'


class Element(Base):
    def __init__(self, selector, text, attrs,
                 parent=None, ctx_parent=None):
        super().__init__(selector, parent, ctx_parent)

        self.text = text
        self.attrs = attrs

        self.is_visible = False
        if self.find().is_displayed():
            if self.is_in_view:
                self.is_visible = True
        self.is_context = self.check_is_context()

    def get_style(self, keys):
        return self.driver.execute_script(js['get_style'],
                                          self.selector, list(keys))

    def set_style(self, style):
        css_text = ''.join(
            [f'{k}: {v} !important;' for k, v in style.items()]
        )
        self.driver.execute_script(js['set_style'], self.selector, css_text)

    def verify_style(self, style):
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script(
                js['is_same_style'], self.selector, style
            ), "Style does not match")

    @property
    def is_in_view(self):
        return self.driver.execute_script(js['is_in_view'], self.selector)

    @property
    def has_before(self):
        return self.driver.execute_script(js['has_pseudo_element'],
                                          self.selector, ':before')

    @property
    def has_after(self):
        return self.driver.execute_script(js['has_pseudo_element'],
                                          self.selector, ':after')

    def check_is_context(self):
        return self.driver.execute_script(js['is_context'], self.selector)


class PseudoElement(Base):
    def __init__(self, base_element, ctx_parent, pseudo_type):
        super().__init__(base_element.selector,
                         base_element, ctx_parent)

        self.pseudo_type = pseudo_type
        self.name = f':{pseudo_type}'
        self.base_element = base_element
        self.is_visible = self.base_element.is_visible
        self.is_context = False

    def __str__(self):
        return f'{self.selector} :{self.pseudo_type}'

    def get_style(self, keys):
        return self.driver.execute_script(js['get_style'],
                                          self.selector, list(keys), self.name)

    def set_style(self, style):
        class_name = f'pseudoStyle{self.index}'
        css_text = ''.join(
            [f'{k}: {v} !important;' for k, v in style.items()]
        )
        self.driver.execute_script(js['set_pseudo_style'],
                                   self.selector, css_text, class_name, self.name)

    def verify_style(self, style):
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script(
                js['is_same_style'], self.selector, style, self.name
            ), "Style does not match")


def set_driver(driver):
    Base.driver = driver
