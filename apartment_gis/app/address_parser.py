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
                else:
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
            return smart_str(description[1].li.contents[0].strip(' \t\n\r'))

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
            self.apt_parameters_list.append([address, district, rooms_num, price, floor, storeys_num, description, phone, location])

    def get_apartments_list(self):
        return self.apt_parameters_list

    def write_in(self, filename, data_list):
        csvfile = open(filename, 'wb+')
        wr = csv.writer(csvfile, delimiter='#', quoting=csv.QUOTE_NONNUMERIC)
        for data_item in data_list:
            wr.writerow(data_item)
        csvfile.close()

    def get_apt_data(self, pages_number):
        for i in xrange(1, pages_number):
                soup = BS(''.join(self.get_html_page("http://domchel.ru/realty/lease/residential/secondary/#" + str(i) + ".php%order=DateUpdate&dir=desc&PriceUnit=1&AreaUnit=1&expand=0&PriceUnit=1")))
                self.parse_apt_data('even', soup)
                self.parse_apt_data('odd', soup)


class OrganizationDataParser(AptDataParser):
    def __init__(self):
        self.organizations_type_list = [
            'Детские сады / Ясли',
            'школы',
            'университеты',
            'больницы',
            'фитнес-клубы',
            'Торгово-развлекательные центры / Моллы']
        self.max_pagesize = 50
        self.organizations_parameters_list = []

    def get_org_url(self, org_name, page_num):
        url = 'http://catalog.api.2gis.ru/searchinrubric?what=' + str(org_name) + '&where=челябинск&page=' + \
              str(page_num) + '&pagesize=50&sort=relevance&key=ruedcr5592&version=1.3&lang=ru&output=json&limit=2000'
        return url

    def get_total_num(self, org_name):
        json_response = urllib.urlopen(self.get_org_url(org_name, 1))
        data = json.load(json_response)
        total_records = data['total']
        return int(total_records)

    def parse_org_data(self, org_type, org_list):
        for organization in org_list:
            name = organization['name']
            address = organization['address']
            location = organization['lon'] + ' ' + organization['lat']
            self.organizations_parameters_list.append([smart_str(org_type),
                                                       name.encode('utf8'),
                                                       address.encode('utf8'),
                                                       location.encode('utf8')])

    def get_organizations_data(self):
        for org_type in self.organizations_type_list:
            iter = 1
            total_records_num = self.get_total_num(org_type)
            while(total_records_num - self.max_pagesize*iter > 0 or total_records_num < self.max_pagesize):
                json_response = urllib.urlopen(self.get_org_url(org_type, iter))
                data = json.load(json_response)
                iter += 1
                org_list = data['result']
                print data['result']
                self.parse_org_data(org_type, org_list)
                if total_records_num < self.max_pagesize:
                    break
        return self.organizations_parameters_list

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='This program get list of apartments and schools information')
    arg_parser.add_argument('-apt_filename', '--apt_filename', help="Input file name with csv extention to get apartments"
                                                                    " info. Don't forget to specify number of apartments")
    arg_parser.add_argument('-pages_number', '--pages_number', help="Input number of web pages you would like to parse."
                                                                    " Don't forget to specify filename for apartments information")
    arg_parser.add_argument('-org_filename', '--org_filename', help='Input file name with csv extention to get'
                                                                    ' organizations info')
    args = vars(arg_parser.parse_args())

    if not (args['org_filename'] or args['apt_filename'] or args['pages_number']):
        arg_parser.print_help()
        exit(1)

    if args['apt_filename'] and args['pages_number']:
        apt_parser = AptDataParser()
        apt_parser.get_apt_data(int(args['pages_number']))
        apartments_list = apt_parser.get_apartments_list()
        print "\nTotal Number of Added Apartments: %s" % len(apartments_list)
        apt_parser.write_in(args['apt_filename'], apartments_list)
    elif args['org_filename']:
        org_parser = OrganizationDataParser()
        data_list = org_parser.get_organizations_data()
        print "\nTotal Number of Added Organizations: %s" % len(data_list)
        org_parser.write_in(args['org_filename'], data_list)
    else:
        print "Error: Add apt_filename or apt_number \n"
        arg_parser.print_help()
        exit(1)