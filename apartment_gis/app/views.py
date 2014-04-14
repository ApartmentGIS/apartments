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


class ApartmentsFilter():
    def __init__(self, request_params):
        self.filter = {
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
        self.request_params = request_params
        self.check_organizations = []
        self.apartment_list = []

    def get_filter(self):
        return self.filter

    def update_filter_by_common_params(self, common_params):
        for param_name in common_params:
            if (param_name in self.request_params) and (self.request_params[param_name] is not None):
                if(isinstance(self.filter[param_name], (list, tuple))):
                    self.filter[param_name] = self.request_params.getlist(param_name)
                else:
                    self.filter[param_name] = self.request_params[param_name]

    def update_filter_by_organizations(self, organizations):
        for organization in organizations:
            if (organization[0] + '_checkbox' in self.request_params) and (self.request_params[organization[0] + '_checkbox'] is not None):
                self.filter[organization[0] + '_checkbox'] = self.request_params[organization[0] + '_checkbox']
                self.check_organizations.append(organization)

                if (organization[0] + '_distance' in self.request_params) and (self.request_params[organization[0] + '_distance'] is not None):
                    self.filter[organization[0] + '_distance'] = self.request_params[organization[0] + '_distance']

    def update_filter_from_request(self):
        self.update_filter_by_common_params(['district', 'rooms_num', 'month_price'])
        self.update_filter_by_organizations(ORGANIZATIONS)

    def get_filtered_by_common_params(self):
        args = []
        kwargs = {}

        if self.filter['district'][0] != 'all':
            districts = []
            for d in self.filter['district']:
                districts.append(Q(district__contains=DISTRICTS[d]))
            args.append(reduce(operator.or_, districts))

        if self.filter['rooms_num'][0] != 'all':
            rooms = []
            for r in self.filter['rooms_num']:
                rooms.append(Q(rooms_num=r))
            args.append(reduce(operator.or_, rooms))

        kwargs['month_price__lte'] = self.filter['month_price']

        return Apartment.objects.filter(*args, **kwargs)

    def get_filtered_by_organizations(self):
        apartment_list = self.get_filtered_by_common_params()
        apartment_list_with_organizations = apartment_list

        for organization in self.check_organizations:
            apartment_list_for_organization = []

            for department in Organization.objects.filter(type=organization[1]):
                appropriate_variants = apartment_list.filter(location__distance_lte=(department.location, D(m=self.filter[organization[0] + '_distance'])))
                if len(appropriate_variants) != 0:
                    apartment_list_for_organization = set(apartment_list_for_organization) | set(appropriate_variants)

            apartment_list_with_organizations = set(apartment_list_with_organizations) & set(apartment_list_for_organization)

        return list(apartment_list_with_organizations)



def home(request):
    if request.method == 'GET':
        apartmentsFilter = ApartmentsFilter(request.GET)
        apartmentsFilter.update_filter_from_request()

        apartment_list = apartmentsFilter.get_filtered_by_organizations()

        filter_form = FilterForm(apartmentsFilter.get_filter())

        return render(request, 'index.html', {
            'apartment_list': apartment_list,
            'filter_form': filter_form
        })