# -*- coding: utf-8 -*-
from django.utils.encoding import smart_str, smart_unicode
from bs4 import BeautifulSoup as BS
import urllib
import csv
import time

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
				#print "print ADREESS %s" % type(smart_str(address))
				#print "print PARAMS %s" % type(self.parameters_list[i][0])
				if (smart_str(address) == self.parameters_list[i][0]):
					print "ADREESS %s" % smart_str(address)
					print "PARAMS %s" % self.parameters_list[i][0]
					print "TRUE"
					return True
		return False
		
	def get_data(self, classname, soup_object):
		print "PRIIINT %s" % classname
		#print "PRIIINT %s " % len(self.parameters_list)
		apt_list = soup_object.findAll('tr', {'class': classname})[::2]
		print len(apt_list)
		k = 0
		for apt in apt_list:
			print '%s) %s' % (k, apt.a.b.string)
			k += 1
			address = apt.a.b.string
			if ( self.is_already_added(address) == True):
				print "print 1"
				continue

			district = apt.div.string

			basic_params = apt.findAll('td', {'class':'black'})
			if ( len(basic_params[0].string.split())==1):
				print "print 2"
				continue

			price = int(basic_params[0].string.split()[0] + basic_params[0].string.split()[1])

			if ( len(basic_params[2].string.split('-'))==1):
				print "print 3"
				continue
			rooms_num = int(basic_params[2].string.split('-')[0])
			#print rooms_num
			floor = int(basic_params[3].string.split('/')[0])
			#print floor
			storeys_num = int(basic_params[3].string.split('/')[1])
			#print storeys_num
			details_url = apt.find('a', href=True)
			print details_url['href']
			details_soup = BS(''.join(parser.get_html_page("http://domchel.ru" + details_url['href'])))
			#print details_soup
			description = self.get_description(details_soup)
			phone = self.get_phone(details_soup)
			if (phone == None):
				print "print 5"
				continue
			self.parameters_list.append([smart_str(address), smart_str(district), rooms_num, price, floor, storeys_num, smart_str(description), phone])
			print "PRIIINT %s " % len(self.parameters_list)
	
	def get_description(self, details_soup):
		description = details_soup.findAll('ul', {'class':'review_right'})
		print description
		if (len(description)==1 or len(description) == 0):
			return None
		else:
			return description[1].li.contents[0].split('\t')[1]
	
	def get_phone(self, details_soup):
		phone_number = details_soup.findAll('div', {'class':'rl_field'})
		print ( len(phone_number), phone_number)
		if ( len(phone_number)== 3 ):
			return phone_number[0].contents[2].split(':')[1].replace(' ','')
		if ( len(phone_number)== 5 ):
			return phone_number[1].contents[2].split(':')[1].replace(' ','')
		if( len(phone_number)== 4 or len(phone_number) == 0 ):
			print details_soup
			return None

if __name__ == '__main__':
	parser = AptDataParser()
	csvfile = open('apartment_data_2.csv', 'wb+')
	wr = csv.writer(csvfile, delimiter='#', quoting=csv.QUOTE_NONNUMERIC)
	i = 0
	for i in xrange(15,30):
		print i
		soup = BS(''.join(parser.get_html_page("http://domchel.ru/realty/lease/residential/secondary/#" + str(i) + ".php%order=DateUpdate&dir=desc&PriceUnit=1&AreaUnit=1&expand=0&PriceUnit=1")))
		parser.get_data('even', soup)
		parser.get_data('odd', soup)
		print 'PAUSE'
		time.sleep(60)
	
		#print data_list

	print "PRIIINT %s " % len(parser.parameters_list)
	for data_item in parser.parameters_list:
		print data_item[0]
		wr.writerow(data_item)
	      
	csvfile.close()
	