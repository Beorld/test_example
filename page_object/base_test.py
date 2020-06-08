# -*- coding: utf-8 -*-
""" Базовые функции для тестов """

import os
import logging
import time
import configparser
import json
from datetime import date, timedelta

import allure
from selenium.webdriver.support import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from configs_for_tests.master.webdriver_config import LANGUAGE_CODE


def get_translated(report_url, word):
    """
    :param report_url: url from helpers like frame_src = "core_analytic_entities_chart"
    :param word: word you want to get in selected language
    """
    conf = configparser.ConfigParser()
    conf.read("control_names.ini", encoding='utf-8')
    name = conf.get(section=report_url, option=word)
    try:
        if LANGUAGE_CODE == 'ru':
            name = name.split(';')[0].strip(' ')
        if LANGUAGE_CODE == 'us':
            name = name.split(';')[1].strip(' ')
    except IndexError:
        name = name.split(';')[0].strip(' ')  # return default if name does not exist in other language

    return name


def screen_shot(message, drv):
    """
    :param message: Сообщение в Аллюр отчёт
    :param drv:
    :return: Сделать скриншот в формате PNG и прикрепить его к Аллюре отчёту
    """
    drv.switch_to.default_content()  # Для фулл-скриншота в Фаерфоксе, а не только фрейма
    time.sleep(3)
    try:
        base64_png_file = drv.get_screenshot_as_png()
        allure.attach(base64_png_file, message, allure.attachment_type.PNG)
    except TimeoutException:
        try:
            base64_png_file = drv.get_screenshot_as_png()
            allure.attach(base64_png_file, message, allure.attachment_type.PNG)
        except TimeoutException:
            print("Ok, screenshot is not available")


def attach_json(json_data, message):
    """
    Прикрепить данные JSON к Аллюре отчёту
        :param message: Сообщение в Аллюре отчёт
        :param json_data: Строка с JSON
    """
    allure.attach(json_data, message, allure.attachment_type.JSON)


def highlight(element, driver):
    """Highlights (blinks) an element"""
    def apply_style(style):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, style)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 2px solid red;")
    time.sleep(.5)
    apply_style(original_style)

    return element


def avoid_blocking_panel(drv):
    wait.WebDriverWait(drv, 10).until(ec.invisibility_of_element_located((By.ID, "BlockLoaderPanel")))


def wait_elem_be_visible(elem_path, driver, sec):
    wait.WebDriverWait(driver, sec).until(ec.visibility_of_element_located((By.XPATH, elem_path)))


def wait_elem_be_clickable(elem_path, driver, sec):
    wait.WebDriverWait(driver, sec).until(ec.element_to_be_clickable((By.XPATH, elem_path)))


def wait_frame_be_available(frame_src_path, driver, sec):
    xpath = "//iframe[contains(@src, '" + frame_src_path + "')]"
    wait.WebDriverWait(driver, sec).until(ec.frame_to_be_available_and_switch_to_it(xpath))


def wait_elem_disappear(elem_xpath, wait_time, drv):
    try:
        wait.WebDriverWait(drv, wait_time).until(ec.invisibility_of_element_located((By.XPATH, elem_xpath)))
    except TimeoutException:
        pass


def switch_to_frame(frame_src, drv):
    """
    :param frame_src: link (name) of report, ex: ug_dash_sdo_plan_fact_detail
    :param drv:
    :return:
    """
    xpath = "//iframe[contains(@src, '" + frame_src + "')]"
    frame_element = drv.find_element_by_xpath(xpath)
    drv.switch_to.frame(frame_element)


def get_yesterday_date():
    """
    :return format dd.mm.yyyy
    """
    yesterday = date.today() - timedelta(days=1)
    return yesterday.strftime('%d.%m.%Y')


def load_dict_from_json(filename):
    """
    # Returns jsondata as well
    """
    with open(filename, 'r', encoding='utf8') as f:
        data = json.load(f)
    f.close()
    return data


def attach_json_from_dict(value, message):
    jsondata = json.dumps(value, indent=2)
    attach_json(jsondata, message)


def get_logger(log_name):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__name__)), 'logs')
    logging.basicConfig(filename=os.path.join(log_dir, log_name),
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S',
                        level=logging.INFO)
    return logging.getLogger()
