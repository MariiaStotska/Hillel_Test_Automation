from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver


class Driver:
    driver = None

    @staticmethod
    def get_chrome_driver() -> WebDriver:
        if Driver.driver is None:
            Driver.driver = webdriver.Chrome()
            Driver.driver.implicitly_wait(5)
            return Driver.driver
        else:
            return Driver.driver
