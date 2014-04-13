# -*- coding: utf-8 -*-
import nose.tools as nt
from django.utils.encoding import smart_str
from app.address_parser import AptDataParser, OrganizationDataParser
import os
from bs4 import BeautifulSoup as BS
import csv
import subprocess
import time
import json
from mock import Mock

class TestParams(object):
    def __init__(self):
        self.filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../address_parser.py')
        self.ODP = OrganizationDataParser

    def test_no_input_params(self):
        p = subprocess.Popen(['python', self.filepath], stdout=subprocess.PIPE)
        p.communicate()
        nt.assert_true(p.returncode == 1)

    def test_input_apt_filename(self):
        p = subprocess.Popen(['python', self.filepath, '--apt_filename', 'test.csv'], stdout=subprocess.PIPE)
        p.communicate()
        nt.assert_true(p.returncode == 1)

    def test_input_apt_number(self):
        p = subprocess.Popen(['python', self.filepath, '--pages_number', '1'], stdout=subprocess.PIPE)
        p.communicate()
        nt.assert_true(p.returncode == 1)


class TestHtmlResponse(object):
    def __init__(self):
        self.ODP = OrganizationDataParser()
        self.target_org = 'Торгово-развлекательные центры / Моллы'

    def test_getting_org_url(self):
        expected_url = 'http://catalog.api.2gis.ru/searchinrubric?what=Торгово-развлекательные центры / Моллы&' \
                       'where=челябинск&page=1&pagesize=50&sort=relevance&key=ruedcr5592&version=1.3&lang=ru&' \
                       'output=json&limit=2000'
        nt.assert_equal(self.ODP.get_org_url(self.target_org, 1), expected_url)


class TestParser(object):
    def __init__(self):
        self.ADP = AptDataParser()
        self.ODP = OrganizationDataParser()
        self.address = 'Ленина пр-кт, д. 34'
        self.details_correct_file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'details_correct_fixtures.html'), 'rb')
        self.details_incorrect_file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'details_incorrect_fixtures.html'), 'rb')
        self.apt_fixtures = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'apartments_fixtures.html'), 'rb')
        self.apt_fixtures_no_room = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'apartments_fixtures_no_room.html'), 'rb')
        self.kindergarden_fixtures = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'kindergarden_test_data.json'), 'rb')

    def test_adding_new_address(self):
        nt.assert_false(self.ADP.is_already_added(self.address))

    def test_adding_same_address(self):
        self.ADP.apt_parameters_list.append([smart_str(self.address)])
        nt.assert_true(self.ADP.is_already_added(self.address))

    def test_adding_different_address(self):
        different_address = 'Цвиллинга, д. 35'
        self.ADP.apt_parameters_list.append([smart_str(self.address)])
        nt.assert_false(self.ADP.is_already_added(different_address))

    def test_getting_location(self):
        expected_coords = '61.420367 55.161203'
        nt.assert_equal(self.ADP.get_location(self.address), expected_coords)

    def test_getting_description(self):
        info = BS(self.details_correct_file.read())
        expected_response = smart_str('интернет, лоджия')
        nt.assert_equal(self.ADP.get_description(info), expected_response)

    def test_getting_no_description(self):
        info = BS(self.details_incorrect_file.read())
        nt.assert_equal(self.ADP.get_description(info), None)

    def test_getting_phone(self):
        info = BS(self.details_correct_file.read())
        expected_phone = u'8(908)041-75-48\n'
        nt.assert_equal(self.ADP.get_phone(info), expected_phone)

    def test_getting_no_phone(self):
        info = BS(self.details_incorrect_file.read())
        nt.assert_equal(self.ADP.get_phone(info), None)

    def test_getting_address(self):
        info = BS(self.apt_fixtures.read())
        expected_address = smart_str('Комарова ул, д. 135')
        nt.assert_equal(self.ADP.get_address(info), expected_address)

    def test_getting_district(self):
        info = BS(self.apt_fixtures.read())
        expected_district = smart_str('Тракторозаводской р-н')
        nt.assert_equal(self.ADP.get_district(info), expected_district)

    def test_getting_price(self):
        info = BS(self.apt_fixtures.read())
        basic_info = info.findAll('td', {'class': 'black'})
        expected_price = 11000
        nt.assert_equal(self.ADP.get_price(basic_info), expected_price)

    def test_getting_no_rooms_num(self):
        info = BS(self.apt_fixtures_no_room.read())
        basic_info = info.findAll('td', {'class': 'black'})
        nt.assert_equal(self.ADP.get_rooms_num(basic_info), None)

    def test_getting_rooms_num(self):
        info = BS(self.apt_fixtures.read())
        basic_info = info.findAll('td', {'class': 'black'})
        expected_rooms_num = 1
        nt.assert_equal(self.ADP.get_rooms_num(basic_info), expected_rooms_num)

    def test_getting_floor_num(self):
        info = BS(self.apt_fixtures.read())
        basic_info = info.findAll('td', {'class': 'black'})
        expected_floor_num = 4
        nt.assert_equal(self.ADP.get_floor_num(basic_info), expected_floor_num)

    def test_getting_storeys_num(self):
        info = BS(self.apt_fixtures.read())
        basic_info = info.findAll('td', {'class': 'black'})
        expected_storeys_num = 9
        nt.assert_equal(self.ADP.get_storeys_num(basic_info), expected_storeys_num)

    def test_parsing_kindergardens(self):
        org_type = 'Детские сады / Ясли'
        expected_result = [
            smart_str(org_type),
            smart_str('Детский сад №307, Колокольчик'),
            smart_str('Гвардейская, 10'),
            smart_str('61.37222182939 55.144250919395')]
        data = []
        for line in self.kindergarden_fixtures:
            data.append(json.loads(line))
        self.ODP.parse_org_data(org_type, data[0]['result'])
        nt.assert_equal(self.ODP.organizations_parameters_list[0], expected_result)


class TestCSV(object):
    def __init__(self):
        self.ADP = AptDataParser()

    def test_file_existence(self):
        target_filename = 'test_existence.csv'
        self.ADP.write_in(target_filename, [])
        nt.assert_true(os.path.exists(target_filename))

    def test_file_empty(self):
        target_filename = 'test_empty.csv'
        self.ADP.write_in(target_filename, [])
        nt.assert_equal(os.path.getsize(target_filename), 0)

    def test_writing_in_csv(self):
        target_filename = 'test_writing.csv'
        expected_row = '1#2#3#4'
        self.ADP.write_in(target_filename, [[1, 2, 3, 4]])
        csvfile = open(target_filename)
        reader = csv.reader(csvfile)
        for row in reader:
            response = row
        nt.assert_equal(response[0], expected_row)






