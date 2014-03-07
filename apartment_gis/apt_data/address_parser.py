# -*- coding: utf-8 -*-
from django.utils.encoding import smart_str, smart_unicode
from bs4 import BeautifulSoup as BS
import urllib
import csv
import time
import json
from pprint import pprint

class AptDataParser():
	def __init__(self):
		self.parameters_list = []
		
	def get_html_page(self, url):
		page_file = urllib.urlopen(url)
		page_html = page_file.read()
		page_file.close()
		return page_html
	
	def is_already_added(self, address):
		if (len(self.parameters_list) == 0):
			return False
		else:
			for i in xrange(0, len(self.parameters_list)):
				if (smart_str(address) == self.parameters_list[i][0]):
					return True
		return False
	
	def get_location(self, address):
		response = urllib.urlopen("http://geocode-maps.yandex.ru/1.x/?format=json&geocode=город Челябинск, " + smart_str(address))
		data = json.load(response)
		location = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
		print "coord %s" % location
		return location
		
	def get_data(self, classname, soup_object):
		apt_list = soup_object.findAll('tr', {'class': classname})[::2]
		print len(apt_list)
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
			details_soup = BS(''.join(parser.get_html_page("http://domchel.ru" + details_url['href'])))
			description = self.get_description(details_soup)
			phone = self.get_phone(details_soup)
			if (phone == None):
				continue
			location = self.get_location(address)
			self.parameters_list.append([smart_str(address), smart_str(district), rooms_num, price, floor, storeys_num, smart_str(description), phone, location])
			print "PRIIINT %s " % len(self.parameters_list)
	
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

if __name__ == '__main__':
	parser = AptDataParser()
	csvfile = open('apartment_data_coord.csv', 'wb+')
	wr = csv.writer(csvfile, delimiter='#', quoting=csv.QUOTE_NONNUMERIC)
	i = 0
	for i in xrange(1,30):
		print i
		soup = BS(''.join(parser.get_html_page("http://domchel.ru/realty/lease/residential/secondary/#" + str(i) + ".php%order=DateUpdate&dir=desc&PriceUnit=1&AreaUnit=1&expand=0&PriceUnit=1")))
		parser.get_data('even', soup)
		parser.get_data('odd', soup)
		print 'PAUSE'
		time.sleep(30)

	print "List of addresses: %s \n" % len(parser.parameters_list)
	for data_item in parser.parameters_list:
		print data_item[0]
		wr.writerow(data_item)
	      
	csvfile.close()