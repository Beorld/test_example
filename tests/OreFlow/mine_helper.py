# -*- coding: utf-8 -*-

import os
import random

import allure
from selenium.webdriver.support.select import Select

from page_object.main_page import MainPage
from page_object.base_test import attach_json_from_dict, wait_elem_be_clickable, wait_elem_disappear, get_translated
from configs_for_tests.pageload_conf import ORE_DATA_PATH


frame_src = "mine_trips"
data_file = os.path.join(ORE_DATA_PATH, 'trip_details.json')


class MineTrips(MainPage):

    def open_frame(self):

        self.open_page(frame_src)

    @allure.step("Create manual trip")
    def create_new_trip(self, trip_details):
        wd = self.app.wd
        self.switch_to_frame_and_load(frame_src)

        # step 1
        def open_form():
            button_name = get_translated(frame_src, 'manual_trip')
            path = f"//button[text()='{button_name}']"
            wd.find_element_by_xpath(path).click()

        def select_dropdown(dropdown, value):
            path = f"//td[contains(text(),'{dropdown}')]/following-sibling::td/select"
            select = Select(wd.find_element_by_xpath(path))
            select.select_by_visible_text(value)

            wait_elem_be_clickable(path, wd, 10)

        def select_field(field, value):
            path = f"//td[contains(text(),'{field}')]/following-sibling::td//input"
            elem = wd.find_element_by_xpath(path)
            elem.clear()
            elem.send_keys(value)

        def submit_new_trip():
            create_text = get_translated(frame_src, 'create')
            submit = f"//button[contains(text(),'{create_text}')]"
            wait_elem_be_clickable(submit, wd, 15)
            wd.find_element_by_xpath(submit).click()

        wait_elem_disappear("//div[@class='loader']", 120, wd)

        open_form()
        select_dropdown(get_translated(frame_src, 'truck'), trip_details['truck'])
        select_dropdown(get_translated(frame_src, 'camera'), trip_details['camera'])
        select_dropdown(get_translated(frame_src, 'orepass'), trip_details['orepass'])
        select_dropdown(get_translated(frame_src, 'work_type'), trip_details['work_type'])
        select_dropdown(get_translated(frame_src, 'ore_type'), trip_details['ore_type'])
        select_field(get_translated(frame_src, 'trips'), trip_details['trips'] + random.randint(-3, 3))
        select_field(get_translated(frame_src, 'distance'), trip_details['distance'])

        submit_new_trip()
        attach_json_from_dict(trip_details, 'Trip Details')
