# -*- coding: utf-8 -*-
""" Конфигурационный файл для всех тестов"""

import os

# Selenium-server
HUB_ADDRESS = 'selenium-hub'
HUB_PORT = 4444

IMPLICITLY_WAIT_TIMEOUT = 5  # seconds

# chrome default
# use --browser chrome or --browser firefox
# for Linux
LINUX_CHROME_DRIVER = 'drivers/chromedriver'
LINUX_FF_DRIVER = 'drivers/geckodriver'
# for Windows
WIN_CHROME_DRIVER = 'drivers/chromedriver.exe'
WIN_FF_DRIVER = 'drivers/geckodriver.exe'
CHROME_PATH = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
FF_PATH = "C:/Program Files/Mozilla Firefox/firefox.exe"
# windows default
# use argument --os windows or --os linux to select operating system

###########################################################################
# Cервер default
LANGUAGE_CODE = 'ru'  # Control languages
SITE_NAME = 'master-server'
USER_NAME = 'test'
USER_PASSWORD = 'test'
USER_LABEL = 'test'

CONFIG_DIR = os.path.abspath(os.path.dirname(__file__))
MENU_PATHS = os.path.join(CONFIG_DIR, 'menu_paths.ini')


# db settings
class DataBaseConfig:
    username = 'test_user'
    password = 'test'
    dsn = 'test-db/test'
    port = 1521
    encoding = 'UTF-8'
