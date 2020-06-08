# -*- coding: utf-8 -*-

import time
import configparser
from datetime import date

import allure
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotVisibleException, TimeoutException, NoSuchElementException

from page_object.base_test import highlight as fl, wait_elem_be_clickable, screen_shot, avoid_blocking_panel
from configs_for_tests.master.webdriver_config import LANGUAGE_CODE


def get_local_name(language, control_name):
    """
    :param language: language code
    :param control_name: control_name from "control_names.ini"
    """
    conf = configparser.ConfigParser()
    conf.read("control_names.ini", encoding='utf-8')
    name = conf.get(section='controls', option=control_name)
    try:
        if language == 'ru':
            name = name.split(';')[0].strip(' ')
        if language == 'us':
            name = name.split(';')[1].strip(' ')
    except IndexError:
        name = name.split(';')[0].strip(' ')  # return default if name does not exist in other language

    return name


def select_item_from_dropdown(select_path, item_name, drv):
    """
    :param select_path:
    :param item_name: Текст (часть текста) для выбора из списка
    :param drv:
    :return:
    """
    avoid_blocking_panel(drv)

    select_elem = drv.find_element_by_xpath(select_path)
    try:
        drv.execute_script("arguments[0].scrollIntoView();", select_elem)
    except Exception as e:
        print(e)

    # Клик на меню
    select_elem.click()

    # Выбор смены по option.value
    option_path = select_path + f"/option[contains(text(), '{item_name}')]"
    fl(drv.find_element_by_xpath(option_path), drv).click()

    # закрываем дроп-даун
    drv.find_element_by_xpath(select_path).click()


def enter_date(date_elem, shift_date, drv):
    """
    :param date_elem: Элемент календаря (даты), НЕ путь к нему
    :param shift_date:
    :param drv:
    :return:
    """
    avoid_blocking_panel(drv)

    # Фокус стоит на YYYY
    date_elem.click()
    # Щелкаем 2 раза влево, чтобы начать ввод даты с начала
    date_elem.send_keys(Keys.ARROW_LEFT)
    date_elem.send_keys(Keys.ARROW_LEFT)
    try:
        date_elem.send_keys(Keys.ARROW_LEFT)
        date_elem.send_keys(Keys.ARROW_LEFT)
    except NoSuchElementException:
        pass
    for i in shift_date:
        date_elem.send_keys(i)
    fl(date_elem, drv)


@allure.step("Ввод даты")
def select_date(shift_date, drv):
    """
    :param shift_date: Формат ввода 'dd.mm.yyyy'
    :param drv:
    :return:
    Warning!: если в поле ввода месяц стоит 02 (февраль), то числа 29 и 30 нельзя ввести - фокус ввода смещается
    в сторону месяца! если текущий месяц февраль, то вводим сначала в поле даты '01.01'
    """
    avoid_blocking_panel(drv)

    locale = get_local_name(LANGUAGE_CODE, 'date')
    date_path = f"//app-date/div/div/label[text()='{locale}']/following-sibling::" \
                "datetimepicker/div/div/input"

    # Найти элемент инпут с календарем
    date_elem = drv.find_element_by_xpath(date_path)
    if date.today().month == 2:  # инкостылирование
        enter_date(date_elem, '01.01', drv)

    enter_date(date_elem, shift_date, drv)


@allure.step("Выбор смены")
def select_shift(shift_number, drv):
    """
    :param shift_number: В виде текста - часть значения
    :param drv:
    :return:
    """
    avoid_blocking_panel(drv)

    locale = get_local_name(LANGUAGE_CODE, 'shift')
    select_path = f"//app-work-regime/div/div/label[text()='{locale}']/following-sibling::select"
    try:
        select_item_from_dropdown(select_path, shift_number, drv)
    except ElementNotVisibleException:
        try:
            time.sleep(5)
            select_item_from_dropdown(select_path, shift_number, drv)
        except ElementNotVisibleException:
            allure.attach("Невозможно выбрать смену")
            screen_shot("Текущий вид", drv)


@allure.step("Выбор предприятия из выпадающего списка")
def select_one_company(company_name, drv):
    avoid_blocking_panel(drv)

    # путь к дроп дауну
    locale = get_local_name(LANGUAGE_CODE, 'enterprise')
    select_path = f"//div/label[text()='{locale}']/following::" \
                  "select"

    try:
        select_item_from_dropdown(select_path, company_name, drv)
    except ElementNotVisibleException:
        screen_shot("Невозможно выбрать предприятие", drv)


@allure.step("Выбор карьера из выпадающего списка")
def select_pit(pit_name, drv):
    avoid_blocking_panel(drv)

    # путь к дроп дауну
    locale = get_local_name(LANGUAGE_CODE, 'pit')
    select_path = f"//div/label[text()='{locale}']/following::" \
                  "select"
    try:
        select_item_from_dropdown(select_path, pit_name, drv)
    except ElementNotVisibleException:
        screen_shot("Невозможно выбрать карьер", drv)


@allure.step('Нажать кнопку "Обновить" на левой панели')
def refresh(drv):
    avoid_blocking_panel(drv)
    locale = get_local_name(LANGUAGE_CODE, 'refresh')
    refresh_xp = f"//button[contains(text(),'{locale}')]"
    try:
        wait_elem_be_clickable(refresh_xp, drv, 60)
    except TimeoutException:
        screen_shot('Кнопка "Обновить" недоступна', drv)

    fl(drv.find_element_by_xpath(refresh_xp), drv).click()
