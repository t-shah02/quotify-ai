from selenium.webdriver import ChromeOptions

DEFAULT_OPTIONS_SETTINGS = [
    '--headless',
    '--no-sandbox',
    '--disable-gpu',
    '--disable-extensions',
    '--remote-debugging-port=9222',
    '--disable-dev-shm-usage'
]

BEST_OPTIONS = ChromeOptions()

for option_setting in DEFAULT_OPTIONS_SETTINGS:
    BEST_OPTIONS.add_argument(option_setting)
