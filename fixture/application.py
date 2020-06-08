# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fixture.session import SessionHelper
from configs_for_tests.webdriver_config import IMPLICITLY_WAIT_TIMEOUT, CHROME_PATH, FF_PATH, \
    WIN_CHROME_DRIVER, WIN_FF_DRIVER, LINUX_CHROME_DRIVER, LINUX_FF_DRIVER, HUB_ADDRESS, HUB_PORT


class Application:

    def __init__(self, baseurl, browser, current_os, use_hub):
        if current_os == 'windows':
            if browser == 'chrome':
                if use_hub:
                    caps = DesiredCapabilities.CHROME
                    caps['acceptInsecureCerts'] = True
                    self.wd = webdriver.Remote(command_executor=f"http://{HUB_ADDRESS}:{HUB_PORT}/wd/hub",
                                               desired_capabilities=caps)
                else:
                    webdriver.ChromeOptions.binary_location = CHROME_PATH
                    self.wd = webdriver.Chrome(executable_path=WIN_CHROME_DRIVER)
            if browser == 'firefox':
                if use_hub:
                    # Firefox by default ['acceptInsecureCerts'] = True
                    self.wd = webdriver.Remote(command_executor=f"http://{HUB_ADDRESS}:{HUB_PORT}/wd/hub",
                                               desired_capabilities=DesiredCapabilities.FIREFOX)
                else:
                    webdriver.FirefoxOptions.binary_location = FF_PATH
                    self.wd = webdriver.Firefox(executable_path=WIN_FF_DRIVER)
        if current_os == 'linux':
            if browser == 'chrome':
                if use_hub:
                    caps = DesiredCapabilities.CHROME
                    caps['acceptInsecureCerts'] = True
                    self.wd = webdriver.Remote(command_executor=f"http://{HUB_ADDRESS}:{HUB_PORT}/wd/hub",
                                               desired_capabilities=caps)
                else:
                    self.wd = webdriver.Chrome(executable_path=LINUX_CHROME_DRIVER)
            if browser == 'firefox':
                if use_hub:
                    self.wd = webdriver.Remote(command_executor=f"http://{HUB_ADDRESS}:{HUB_PORT}/wd/hub",
                                               desired_capabilities=DesiredCapabilities.FIREFOX)
                else:
                    self.wd = webdriver.Firefox(executable_path=LINUX_FF_DRIVER)

        self.wd.delete_all_cookies()
        self.wd.maximize_window()
        self.wd.implicitly_wait(IMPLICITLY_WAIT_TIMEOUT)

        self.session = SessionHelper(self)
        self.baseurl = baseurl

    def open_home_page(self):
        wd = self.wd
        if not wd.current_url == self.baseurl:
            wd.get(self.baseurl)

    def destroy(self):
        self.wd.quit()
