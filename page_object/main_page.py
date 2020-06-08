# -*- coding: utf-8 -*-_
""" PageObject для главной страницы """

import time
import configparser

import allure
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from page_object.base_test import screen_shot, highlight as fl, wait_frame_be_available, \
    wait_elem_be_clickable, switch_to_frame, avoid_blocking_panel
from configs_for_tests.pageload_conf import language
from configs_for_tests.webdriver_config import MENU_PATHS, LANGUAGE_CODE
from page_object.left_bar import get_local_name


class MainPage:

    def __init__(self, app):
        self.app = app

    @allure.step("Открыть левую панель")
    def open_left_bar(self, drv):
        avoid_blocking_panel(drv)

        open_left_bar_path = "//app-lmenu/div/div/i[contains(@class,'right')]"

        try:
            open_elem = drv.find_element_by_xpath(open_left_bar_path)
            open_elem.click()
        except NoSuchElementException:
            pass

    def open_page(self, page_id):
        drv = self.app.wd

        lang = language
        conf = configparser.ConfigParser()
        conf.read(MENU_PATHS, encoding='utf-8')
        menu_section = 'menu_list'

        def select_language(paths):
            try:
                if lang == 'ru':
                    return paths.split(';')[0]
                if lang == 'en':
                    return paths.split(';')[1]
                if lang == 'fr':
                    return paths.split(';')[2]
                else:
                    print("Language settings are incorrect")
            except IndexError:
                print(f'Menu-item "{paths.split(";")[0]}" on "{lang}" language is not available. '
                      f'Please check menu_paths.ini file')

        # view menu level
        menu_level = conf.getint(section=page_id, option='MENU_LEVEL')

        # Получаем сразу название меню
        menu = conf.get(menu_section, conf.get(page_id, "MENU1")).strip('"')
        menu = select_language(menu)

        # 1 - в основном меню на главной странице
        if menu_level == 1:
            self.menu_go_to(menu_name=menu)

        # 2 - в выпадающем списке
        elif menu_level == 2:
            menu_item = conf.get(page_id, "MENU2").strip('"')
            menu_item = select_language(menu_item)
            self.menu_go_to(menu)
            self.go_to_menu_item(menu, menu_item)

        # 3 - в выпадающем списке в подменю
        elif menu_level == 3:
            # Получаем тег подменю
            menu_item_tag = conf.get(page_id, "MENU2")
            # по подменю получаем название подменю
            menu_item = conf.get(menu_section, menu_item_tag).strip('"')
            menu_item = select_language(menu_item)
            sub_menu = conf.get(page_id, "MENU3").strip('"')
            sub_menu = select_language(sub_menu)
            self.menu_go_to(menu)
            self.go_to_sub_menu(menu, menu_item, sub_menu)

        else:
            assert False, f"Wrong menu level {menu_level}. Check menu_paths.ini"

        # Открываем левую панель, если не открыта по умолчанию
        self.open_left_bar(drv)

    @allure.step("Загрузка фрейма")
    def switch_to_frame_and_load(self, frame_src):
        drv = self.app.wd

        drv.switch_to.default_content()

        conf = configparser.ConfigParser()
        conf.read(MENU_PATHS, encoding='utf-8')

        # время загрузки из конфига
        load_time = conf.getint(section=frame_src, option='LOAD_TIME')

        try:
            wait_frame_be_available(frame_src, drv, load_time)
        except TimeoutException:
            pass

        drv.switch_to.default_content()
        self.enable_auto_zoom()
        switch_to_frame(frame_src, drv)
        screen_shot("Вид фрейма", drv)

    @allure.step('Открытие выпадающего списка меню "{1}"')
    def menu_go_to(self, menu_name):

        drv = self.app.wd

        xpath = f"//div/div/div[contains(text(),'{menu_name}')]"
        wait_elem_be_clickable(xpath, drv, 25)

        fl(drv.find_element_by_xpath(xpath), drv).click()

    @allure.step('Вход в пункт меню "{2}"')
    def go_to_menu_item(self, menu_name, menu_item_name):
        drv = self.app.wd

        xpath = f"//div/div/div[contains(text(),'{menu_name}')]/following::" \
            f"ul[contains(@class, 'list-children-open')]/li/div/a[text()='{menu_item_name}']"

        elem = drv.find_element_by_xpath(xpath)
        fl(elem, drv).click()

    @allure.step('Вход в под-пункт меню "{3}"')
    def go_to_sub_menu(self, menu_name, menu_item_name, sub_menu_name):
        drv = self.app.wd

        xpath = f"//div/div/div[contains(text(),'{menu_name}')]/following::" \
            f"ul/li/div[text()='{menu_item_name}']"
        fl(drv.find_element_by_xpath(xpath), drv).click()

        submenu_path = xpath + f"/following::ul/li/div/a[text()='{sub_menu_name}']"

        elem = drv.find_element_by_xpath(submenu_path)
        fl(elem, drv).click()

    @allure.step('Закрываем активное окно')
    def close_active_frame(self):

        drv = self.app.wd

        # переход к основному окну
        drv.switch_to.default_content()

        close_window = "//div[@class='close-button']"
        try:
            wait_elem_be_clickable(close_window, drv, 15)
        except TimeoutException:
            pass

        screen_shot("Окно перед закрытием", drv)
        try:
            crest = drv.find_element_by_xpath(close_window)
            crest.click()
        except NoSuchElementException:
            screen_shot("The window cannot be closed", drv)
            assert False, "Can't close window. Please check attached picture"

        time.sleep(1)

    @allure.step('Включение автомасштабирования')
    def enable_auto_zoom(self):
        """
        Включаем автомасштабирование страницы во избежание горизонтального скролла
        :return:
        """
        drv = self.app.wd

        menu_path = "//div[@class='extra-button']/span/i"
        drv.find_element_by_xpath(menu_path).click()

        auto_scale = get_local_name(LANGUAGE_CODE, 'auto_scale')
        autoscale_path = f"//div[contains(text(),'{auto_scale}')]/span/span/i"
        try:
            autoscale_elem = drv.find_element_by_xpath(autoscale_path)
            if 'check' not in autoscale_elem.get_attribute('class'):
                autoscale_elem.click()
        except NoSuchElementException:
            pass

        dropdown_elem = drv.find_element_by_xpath(menu_path)
        if 'down' in dropdown_elem.get_attribute('class'):
            dropdown_elem.click()

    @allure.step("Проверяем, что элементы загружены на форме")
    def check_elements_loaded(self, data_strings, method='xpath'):
        """
        Для тестовых серваков - если отчет загружен, но данных нет на текущую дату/смену - ввести вручную,
        так как при 0 элементах фейлим тест
        :param data_strings: Путь для нахождения элементов
        :param method: xpath by default; use 'css' to select css selection
        :return: False если элементов 0
        """
        drv = self.app.wd
        if method == 'xpath':
            elems = drv.find_elements_by_xpath(data_strings)
        elif method == 'css':
            elems = drv.find_elements_by_css_selector(data_strings)
        else:
            assert False, f'Selector method {method} is incorrect'

        count = len(elems)
        allure.attach("Количество найденных элементов: " + str(count), "Количество элементов")

        screen_shot("Вид страницы", drv)
        assert count > 0, 'Empty report - found 0 elements'
