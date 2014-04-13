# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Q
from django.contrib.gis.measure import D
import operator
from models import Apartment, Organization
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

ORGANIZATIONS = (
    ('kindergarten', 'KIN'),
    ('school', 'SCH'),
    ('university', 'UNI'),
    ('hospital', 'HOS'),
    ('fitnessclub', 'FIT'),
    ('shopmall', 'SHP')
)


def home(request):
    filter = {
        'district': ['all'],
        'rooms_num': ['all'],
        'month_price': 50000,
        # 'kindergarten_checkbox': '',
        'kindergarten_distance': 3000,
        # 'school_checkbox': '',
        'school_distance': 3000,
        # 'university_checkbox': '',
        'university_distance': 3000,
        # 'hospital_checkbox': '',
        'hospital_distance': 3000,
        # 'fitnessclub_checkbox': '',
        'fitnessclub_distance': 3000,
        # 'shopmall_checkbox': '',
        'shopmall_distance': 3000
    }

    check_organizations = []

    if request.method == 'GET':
        if ('district' in request.GET) and (request.GET['district'] is not None):
            filter['district'] = request.GET.getlist('district')
        if ('rooms_num' in request.GET) and (request.GET['rooms_num'] is not None):
            filter['rooms_num'] = request.GET.getlist('rooms_num')
        if ('month_price' in request.GET) and (request.GET['month_price'] is not None):
            filter['month_price'] = request.GET['month_price']

        for organization in ORGANIZATIONS:
            if (organization[0] + '_checkbox' in request.GET) and (request.GET[organization[0] + '_checkbox'] is not None):
                filter[organization[0] + '_checkbox'] = request.GET[organization[0] + '_checkbox']
                check_organizations.append(organization)
                if (organization[0] + '_distance' in request.GET) and (request.GET[organization[0] + '_distance'] is not None):
                    filter[organization[0] + '_distance'] = request.GET[organization[0] + '_distance']

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
            rooms.append(Q(rooms_num=r))

        args.append(reduce(operator.or_, rooms))

    kwargs['month_price__lte'] = filter['month_price']

    apartment_list = Apartment.objects.filter(*args, **kwargs)
    apartment_list_with_organizations = apartment_list

    for organization in check_organizations:
        apartment_list_for_organization = []

        for department in Organization.objects.filter(type=organization[1]):
            good_variants = apartment_list.filter(location__distance_lte=(department.location, D(m=filter[organization[0] + '_distance'])))
            if len(good_variants) != 0:
                apartment_list_for_organization = list(set(apartment_list_for_organization) | set(good_variants))

        apartment_list_with_organizations = list(set(apartment_list_with_organizations) & set(apartment_list_for_organization))

    filter_form = FilterForm(filter)

    return render(request, 'index.html', {
        'apartment_list': apartment_list_with_organizations,
        'filter_form': filter_form
    })