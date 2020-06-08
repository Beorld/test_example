# -*- coding: utf-8 -*-

import allure
from selenium.common.exceptions import NoAlertPresentException

from page_object.base_test import highlight as fl, screen_shot


class SessionHelper:

    def __init__(self, app):
        self.app = app

    username_id = 'username-input'
    password_id = 'password-input'
    login_button_path = "login-button"

    def input_user_name(self, user_name):

        wd = self.app.wd
        self.app.open_home_page()
        screen_shot("Auth window", wd)
        wd.find_element_by_id(self.username_id).send_keys(user_name)

    def input_user_password(self, user_password):

        wd = self.app.wd
        wd.find_element_by_id(self.password_id).send_keys(user_password)

    def click_login_button(self):

        wd = self.app.wd
        fl(wd.find_element_by_id(self.login_button_path), wd).click()

    @allure.step('Logging in')
    def login(self, user_name, user_password):

        self.input_user_name(user_name)
        self.input_user_password(user_password)
        self.click_login_button()

    def is_logged_in(self):

        wd = self.app.wd
        wd.switch_to.default_content()
        return len(wd.find_elements_by_xpath("//main-menu/div/div")) > 0

    def ensure_logout(self, username):

        if self.is_logged_in():
            self.logout(username)

    def ensure_login(self, username, password):

        if self.is_logged_in():
            return
        self.login(username, password)

    @allure.step('Logging out')
    def logout(self, user_label):

        wd = self.app.wd
        user_label_xpath = "//div/div/div/div[contains(text(),'{0}')]".format(user_label.lower())
        fl(wd.find_element_by_xpath(user_label_xpath), wd).click()

        logout_xpath = "//a[@href='/core/logout/']/div"
        fl(wd.find_element_by_xpath(logout_xpath), wd).click()

        try:
            wd.switch_to.alert.accept()
        except NoAlertPresentException:
            pass

