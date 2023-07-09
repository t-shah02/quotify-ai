from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from typing import List


BROWSER_TIMEOUT = 10
INSTAGRAM_LOGIN_URL = 'https://www.instagram.com/accounts/login/'


class InstagramPoster(webdriver.Chrome):
    def __init__(self, username: str, password: str, headless: bool = False, no_sandbox: bool = False):
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless')
        if no_sandbox:
            options.add_argument('--no-sandbox')

        super().__init__(options=options)

        self.username = username
        self.password = password
        self.is_authenticated = False

    def login(self):
        self.get(INSTAGRAM_LOGIN_URL)

        submit_btn_xpath = '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]/button'
        auth_fields: List[WebElement] = WebDriverWait(self, timeout=BROWSER_TIMEOUT).until(
            lambda driver: driver.find_elements(By.TAG_NAME, 'input'))
        submit_btn: WebElement = WebDriverWait(self, timeout=BROWSER_TIMEOUT).until(
            lambda driver: driver.find_element(By.XPATH, submit_btn_xpath))

        username_field, password_field = auth_fields
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)

        submit_btn.click()

    def post_content(self, image_file_path: str, post_caption: str):

        create_post_btn_xpath = '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[7]/div/span/div/a'
        create_post_btn: WebElement = WebDriverWait(self, timeout=BROWSER_TIMEOUT).until(
            lambda driver: driver.find_element(By.XPATH, create_post_btn_xpath))

        create_post_btn.click()

        upload_files_btn_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/form/input'
        upload_files_btn: WebElement = WebDriverWait(self, timeout=BROWSER_TIMEOUT).until(
            lambda driver: driver.find_element(By.XPATH, upload_files_btn_xpath))

        upload_files_btn.send_keys(image_file_path)

        next_btn_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div[3]/div/div'
        next_btn: WebElement = WebDriverWait(self, timeout=BROWSER_TIMEOUT).until(
            lambda driver: driver.find_element(By.XPATH, next_btn_xpath))

        next_btn.click()

        another_next_btn_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div[3]/div/div'
        another_next_btn: WebElement = WebDriverWait(self, timeout=BROWSER_TIMEOUT).until(
            lambda driver: driver.find_element(By.XPATH, another_next_btn_xpath))

        another_next_btn.click()

        caption_fieldtext_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea'
        caption_fieldtext: WebElement = WebDriverWait(self, timeout=BROWSER_TIMEOUT).until(
            lambda driver: driver.find_element(By.XPATH, caption_fieldtext_xpath))

        caption_fieldtext.send_keys(post_caption)

        share_btn_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div[3]/div/div'
        share_btn: WebElement = WebDriverWait(self, timeout=BROWSER_TIMEOUT).until(
            lambda driver: driver.find_element(By.XPATH, share_btn_xpath))

        share_btn.click()
