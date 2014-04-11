# -*- coding: utf-8 -*-
from django.utils.encoding import smart_str, smart_unicode
from bs4 import BeautifulSoup as BS
import urllib
import csv
import json
import argparse


class AptDataParser():
    def __init__(self):
        self.apt_parameters_list = []
        self.cur_apt_number = 0

    def get_html_page(self, url):
        page_file = urllib.urlopen(url)
        page_html = page_file.read()
        page_file.close()
        return page_html

    def is_already_added(self, address):
        if len(self.apt_parameters_list) == 0:
            return False
        else:
            for i in xrange(0, len(self.apt_parameters_list)):
                if smart_str(address) == self.apt_parameters_list[i][0]:
                    return True
        return False

    def get_location(self, address):
        response = urllib.urlopen("http://geocode-maps.yandex.ru/1.x/?format=json&geocode=город Челябинск, " + smart_str(address))
        data = json.load(response)
        location = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        return location

    def get_address(self, apt_info):
        return smart_str(apt_info.a.b.string)

    def get_district(self, apt_info):
        return smart_str(apt_info.div.string)

    def get_price(self, basic_params):
        return int(basic_params[0].string.split()[0] + basic_params[0].string.split()[1])

    def get_rooms_num(self, basic_params):
        if len(basic_params[2].string.split('-')) == 1:
            return None
        else:
            return int(basic_params[2].string.split('-')[0])

    def get_floor_num(self, basic_params):
        return int(basic_params[3].string.split('/')[0])

    def get_storeys_num(self, basic_params):
        return int(basic_params[3].string.split('/')[1])

    def get_description(self, details_soup):
        description = details_soup.findAll('ul', {'class': 'review_right'})
        if len(description) == 1 or len(description) == 0:
            return None
        else:
            return description[1].li.contents[0].strip(' \t\n\r')

    def get_phone(self, details_soup):
        phone_number = details_soup.findAll('div', {'class': 'rl_info'})
        try:
            return phone_number[0].div.div.contents[2].split(':')[1].replace(' ', '')
        except Exception as error:
            print error
            return None

    def parse_apt_data(self, classname, soup_object):
        apt_list = soup_object.findAll('tr', {'class': classname})[::2]
        for apt in apt_list:
            address = self.get_address(apt)
            if self.is_already_added(address):
                continue

            basic_params = apt.findAll('td', {'class': 'black'})
            if len(basic_params[0].string.split()) == 1:
                continue

            rooms_num = self.get_rooms_num(basic_params)
            if rooms_num is None:
                continue

            details_url = apt.find('a', href=True)
            details_soup = BS(''.join(self.get_html_page("http://domchel.ru" + details_url['href'])))
            phone = self.get_phone(details_soup)
            if phone is None:
                continue

            district = self.get_district(apt)
            price = self.get_price(basic_params)
            floor = self.get_floor_num(basic_params)
            storeys_num = self.get_storeys_num(basic_params)
            description = self.get_description(details_soup)
            location = self.get_location(address)
            print address
            self.apt_parameters_list.append([address, district, rooms_num, price, floor, storeys_num, smart_str(description), phone, location])

    def get_apartments_list(self):
        return self.apt_parameters_list

    def write_in(self, filename, data_list):
        csvfile = open(filename, 'wb+')
        wr = csv.writer(csvfile, delimiter='#', quoting=csv.QUOTE_NONNUMERIC)
        for data_item in data_list:
            print data_item
            wr.writerow(data_item)
        csvfile.close()

    def get_apt_data(self, pages_number):
        for i in xrange(1, pages_number):
                soup = BS(''.join(self.get_html_page("http://domchel.ru/realty/lease/residential/secondary/#" + str(i) + ".php%order=DateUpdate&dir=desc&PriceUnit=1&AreaUnit=1&expand=0&PriceUnit=1")))
                self.parse_apt_data('even', soup)
                self.parse_apt_data('odd', soup)

class NurserySchoolDataParser(AptDataParser):
    def __init__(self):
        self.school_parameters_list = []

    def get_school_data(self):
        json_response = urllib.urlopen("http://maps.yandex.ru/services/search/1.x/search.json?autoscale=0&lang=ru-RU&ll=61.391702%2C55.164186&origin=maps-pager&results=261&spn=2.084656%2C0.666690&text=детские сады члеябинск&type=biz%2Cpsearch%2Cweb")
        data = json.load(json_response)
        school_list = data['features']

        for school in school_list:
            name = school['properties']['CompanyMetaData']['name']
            print name
            address = school['properties']['CompanyMetaData']['address']
            print address
            location = str(school['geometry']['coordinates'][0]) + " " + str(school['geometry']['coordinates'][1])
            print location
            phone = school['properties']['CompanyMetaData']['Phones'][0]['formatted']
            print phone
            self.school_parameters_list.append([smart_str(name), smart_str(address), phone, location])
        return self.school_parameters_list

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='This program get list of apartments and schools information')
    arg_parser.add_argument('-apt_filename', '--apt_filename', help="Input file name with csv extention to get apartments info. Don't forget to specify number of apartments")
    arg_parser.add_argument('-pages_number', '--pages_number', help="Input number of web pages you would like to parse. Don't forget to specify filename for apartments information")
    arg_parser.add_argument('-school_filename', '--school_filename', help='Input file name with csv extention to get schools info')
    args = vars(arg_parser.parse_args())

    if not (args['school_filename'] or args['apt_filename'] or args['pages_number']):
        arg_parser.print_help()
        exit(1)

    if args['apt_filename'] and args['pages_number']:
            apt_parser = AptDataParser()
            apt_parser.get_apt_data(int(args['pages_number']))
            apartments_list = apt_parser.get_apartments_list()
            print "\nTotal Number of Added Apartments: %s" % len(apartments_list)
            apt_parser.write_in(args['apt_filename'], apartments_list)
    elif args['school_filename']:
        school_parser = NurserySchoolDataParser()
        data_list = school_parser.get_school_data()
        print "\n Total Number of Added Nursery Schools: %s" % len(school_parser.school_parameters_list)
        school_parser.write_in(args['school_filename'], school_parser.school_parameters_list)
    else:
        print "Error: Add apt_filename or apt_number \n"
        arg_parser.print_help()
        exit(1)