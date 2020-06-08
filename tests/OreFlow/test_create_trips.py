# -*- coding: utf-8 -*-

import pytest

from configs_for_tests.pageload_conf import COMPANY_NAME, shift_number, shift_date, pit_name
from tests.OreFlow.mine_helper import MineTrips, data_file
from page_object.left_bar import select_one_company, select_pit, select_shift, select_date, refresh
from page_object.base_test import load_dict_from_json

#####################################################################
testdata = []
data = load_dict_from_json(data_file)
for trip in data['trips']:
    testdata.append(trip)
#####################################################################


@pytest.mark.master
@pytest.mark.test
@pytest.mark.smoke
class TestMineTrips:

    @pytest.mark.run(order=20101)
    @pytest.mark.dependency()
    def test_open_page(self, app):

        page = MineTrips(app)
        page.open_frame()

    @pytest.mark.run(order=20102)
    @pytest.mark.dependency(depends=['TestMineTrips::test_open_page'])
    def test_select_company(self, app):

        select_one_company(COMPANY_NAME, app.wd)

    @pytest.mark.run(order=20103)
    @pytest.mark.dependency(depends=['TestMineTrips::test_open_page'])
    def test_select_date(self, app):

        select_date(shift_date, app.wd)

    @pytest.mark.run(order=20104)
    @pytest.mark.dependency(depends=['TestMineTrips::test_open_page'])
    def test_select_shift(self, app):

        select_shift(shift_number, app.wd)

    @pytest.mark.run(order=20105)
    @pytest.mark.dependency(depends=['TestMineTrips::test_open_page'])
    def test_select_pit(self, app):

        select_pit(pit_name, app.wd)

    @pytest.mark.run(order=20106)
    @pytest.mark.dependency(depends=['TestMineTrips::test_open_page'])
    def test_refresh(self, app):

        refresh(app.wd)

    @pytest.mark.run(order=20107)
    @pytest.mark.dependency(depends=['TestMineTrips::test_open_page'])
    @pytest.mark.parametrize("trip_details", testdata)
    def test_create_new_trip(self, app, trip_details):

        page = MineTrips(app)
        page.create_new_trip(trip_details)

    @pytest.mark.run(order=20199)
    @pytest.mark.dependency(depends=['TestMineTrips::test_open_page'])
    def test_page_closed(self, app):

        page = MineTrips(app)
        page.close_active_frame()
