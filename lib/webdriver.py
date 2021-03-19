import json
from selenium import webdriver


def send(driver, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    if 'status' in response:
        raise Exception(response.get('value'))
    return response.get('value')


def get_chrome_driver(window_size, headless=False, extension=None):
    options = webdriver.ChromeOptions()
    options.add_argument("disable-gpu")
    options.add_argument("disable-infobars")
    options.add_argument("disable-setuid-sandbox")
    options.add_argument("no-sandbox")
    options.add_argument("hide-scrollbars")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("enable-experimental-web-platform-features")
    options.add_argument("window-size={},{}".format(*window_size))

    if extension is not None and headless:
        raise RuntimeError('Chrome extensions do not work in headless mode.')

    if headless:
        options.add_argument("headless")

    if extension:
        for path in extension:
            options.add_extension(path)

    dc = webdriver.DesiredCapabilities.CHROME.copy()
    dc['acceptInsecureCerts'] = True
    return webdriver.Chrome(chrome_options=options, desired_capabilities=dc)


def get_firefox_driver(window_size, headless=False, extension=None):
    # Note: Extensions seem to work in headless mode, but the browser cannot take
    # a screenshot with a transparent background.

    width, height = window_size

    options = webdriver.FirefoxOptions()
    options.add_argument(f"--width={width}")
    options.add_argument(f"--height={height}")
    if headless:
        options.add_argument("--headless")

    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.display.background_color', 'rgba(0,0,0,0)')
    profile.update_preferences()

    return webdriver.Firefox(firefox_options=options, firefox_profile=profile)
