# -*- coding: utf-8 -*-
from django.utils.encoding import smart_str, smart_unicode
from bs4 import BeautifulSoup as BS
import urllib
import csv
import time
import json
import argparse

class AptDataParser():
    def __init__(self):
        self.apt_parameters_list = []

    def get_html_page(self, url):
        page_file = urllib.urlopen(url)
        page_html = page_file.read()
        page_file.close()
        return page_html

    def is_already_added(self, address):
        if (len(self.apt_parameters_list) == 0):
            return False
        else:
            for i in xrange(0, len(self.apt_parameters_list)):
                if (smart_str(address) == self.apt_parameters_list[i][0]):
                    return True
        return False

    def get_location(self, address):
        response = urllib.urlopen("http://geocode-maps.yandex.ru/1.x/?format=json&geocode=город Челябинск, " + smart_str(address))
        data = json.load(response)
        location = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        return location

    def parse_apt_data(self, classname, soup_object):
        apt_list = soup_object.findAll('tr', {'class': classname})[::2]
        k = 0
        for apt in apt_list:
            print '%s) %s' % (k, apt.a.b.string)
            k += 1
            address = apt.a.b.string
            if ( self.is_already_added(address) == True):
                continue

            district = apt.div.string

            basic_params = apt.findAll('td', {'class':'black'})
            if ( len(basic_params[0].string.split())==1):
                continue

            price = int(basic_params[0].string.split()[0] + basic_params[0].string.split()[1])

            if ( len(basic_params[2].string.split('-'))==1):
                continue
            rooms_num = int(basic_params[2].string.split('-')[0])
            floor = int(basic_params[3].string.split('/')[0])
            storeys_num = int(basic_params[3].string.split('/')[1])
            details_url = apt.find('a', href=True)
            details_soup = BS(''.join(self.get_html_page("http://domchel.ru" + details_url['href'])))
            description = self.get_description(details_soup)
            phone = self.get_phone(details_soup)
            if (phone == None):
                continue
            location = self.get_location(address)
            self.apt_parameters_list.append([smart_str(address), smart_str(district), rooms_num, price, floor, storeys_num, smart_str(description), phone, location])

    def get_description(self, details_soup):
        description = details_soup.findAll('ul', {'class':'review_right'})
        if (len(description)==1 or len(description) == 0):
            return None
        else:
            return description[1].li.contents[0].split('\t')[1]

    def get_phone(self, details_soup):
        phone_number = details_soup.findAll('div', {'class':'rl_field'})
        if ( len(phone_number)== 3 ):
            return phone_number[0].contents[2].split(':')[1].replace(' ','')
        if ( len(phone_number)== 5 ):
            return phone_number[1].contents[2].split(':')[1].replace(' ','')
        if( len(phone_number)== 4 or len(phone_number) == 0 ):
            return None

    def write_in(self, filename, data_list):
        csvfile = open(filename, 'wb+')
        wr = csv.writer(csvfile, delimiter='#', quoting=csv.QUOTE_NONNUMERIC)
        for data_item in data_list:
            print data_item[0]
            wr.writerow(data_item)
        csvfile.close()

    def get_apt_data(self, apt_number):
        for i in xrange(1,int(apt_number)):
                soup = BS(''.join(self.get_html_page("http://domchel.ru/realty/lease/residential/secondary/#" + str(i) + ".php%order=DateUpdate&dir=desc&PriceUnit=1&AreaUnit=1&expand=0&PriceUnit=1")))
                self.parse_apt_data('even', soup)
                self.parse_apt_data('odd', soup)
                #time.sleep(15)

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
    arg_parser.add_argument('-apt_number', '--apt_number', help="Input number of apartments you would like to add. Don't forget to specify filename for apartments information")
    arg_parser.add_argument('-school_filename', '--school_filename', help='Input file name with csv extention to get schools info')
    args = vars(arg_parser.parse_args())

    if not (args['school_filename'] or args['apt_filename'] or args['apt_number']):
        arg_parser.print_help()
        exit(0)

    if(args['apt_filename'] and args['apt_number']):
            apt_parser = AptDataParser()
            apt_parser.get_apt_data(args['apt_number'])
            print "\n Total Number of Added Apartments: %s" % len(apt_parser.apt_parameters_list)
            apt_parser.write_in(args['apt_filename'], apt_parser.apt_parameters_list)
    elif(args['school_filename']):
        school_parser = NurserySchoolDataParser()
        data_list = school_parser.get_school_data()
        print "\n Total Number of Added Nursery Schools: %s" % len(school_parser.school_parameters_list)
        school_parser.write_in(args['school_filename'], school_parser.school_parameters_list)
    else:
        print "Error: Add apt_filename or apt_number \n"
        arg_parser.print_help()
        exit(0)