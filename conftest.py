# -*- coding: utf-8 -*-

import pytest
import allure
from fixture.application import Application
from configs_for_tests.webdriver_config import USER_NAME, USER_PASSWORD, USER_LABEL, SITE_NAME
from page_object.base_test import screen_shot

fixture = None


@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    current_os = request.config.getoption("--os")
    use_hub = request.config.getoption("--use_hub")

    if fixture is None:
        fixture = Application(current_os=current_os, browser=browser, use_hub=use_hub, baseurl=SITE_NAME)
    fixture.session.ensure_login(USER_NAME, USER_PASSWORD)
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    global fixture

    def fin():
        if fixture:
            fixture.session.ensure_logout(USER_LABEL)
            fixture.destroy()
    request.addfinalizer(fin)
    return fixture


def pytest_exception_interact():
    global fixture

    if fixture:
        # Прикрепить скриншот после падения UI теста
        message = 'Screenshot after test fail'
        allure.attach(fixture.wd.current_url, "URL")
        screen_shot(message, fixture.wd)


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--os", action="store", default="windows")
    parser.addoption("--use_hub", action="store", default=False)
