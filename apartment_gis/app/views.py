# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Q
import operator
from models import Apartment
from forms import FilterForm


DISTRICTS = {
	'metal': u'Металлургический',
	'szapa': u'Северо-запад',
	'svost': u'Северо-восток',
	'trakt': u'Тракторозаводской',
	'centr': u'Центральный',
	'sovet': u'Советский',
	'lenin': u'Ленинский'
}

def home(request):
	filter = {
		'district': ['all'],
		'rooms_num': ['all'],
		'month_price': 50000,
		'kindergarten_distance': 3000
	}

	if request.method == 'GET':
		if ('district' in request.GET) and (request.GET['district'] is not None):
			filter['district'] = request.GET.getlist('district')
		if ('rooms_num' in request.GET) and (request.GET['rooms_num'] is not None):
			filter['rooms_num'] = request.GET.getlist('rooms_num')
		if ('month_price' in request.GET) and (request.GET['month_price'] is not None):
			filter['month_price'] = request.GET['month_price']
		if ('kindergarten_distance' in request.GET) and (request.GET['kindergarten_distance'] is not None):
			filter['kindergarten_distance'] = request.GET['kindergarten_distance']

	args = []
	kwargs = {}

	if filter['district'][0] != 'all':
		districts = []
		for d in filter['district']:
			districts.append(Q(district__contains=DISTRICTS[d]))
		args.append(reduce(operator.or_, districts))

	if filter['rooms_num'][0] != 'all':
		rooms = []
		for r in filter['rooms_num']:
			if r == '1' or r == '2':
				rooms.append(Q(rooms_num=r))
			elif r == 'big':
				rooms.append(Q(rooms_num__gte=3))

		args.append(reduce(operator.or_, rooms))

	kwargs['month_price__lte'] = filter['month_price']

	apartment_list = Apartment.objects.filter(*args, **kwargs)
	filter_form = FilterForm(filter)

	return render(request, 'index.html', {
		'apartment_list': apartment_list,
		'filter_form': filter_form
	})