# -*- coding: utf-8 -*-
from django.db.models import Count, Max, Min
import floppyforms as forms
from models import Apartment


DISTRICT_CHOICES = (
    ('all', u'все'),
    ('metal', u'Металлургический'),
    ('szapa', u'Северо-запад'),
    ('svost', u'Северо-восток'),
    ('trakt', u'Тракторозаводской'),
    ('centr', u'Центральный'),
    ('sovet', u'Советский'),
    ('lenin', u'Ленинский')
)

class BtnCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'floppyforms/btn_checkbox_select_multiple.html'


class CustomRangeInput(forms.RangeInput):
    template_name = 'floppyforms/custom_range_input.html'


class LabelCheckbox(forms.CheckboxInput):
    template_name = 'floppyforms/label_checkbox.html'


def getRoomNumChoices():
    rooms_num_db = Apartment.objects.values('rooms_num').annotate(rooms_count=Count('rooms_num')).order_by('rooms_num')
    rooms_num_choices = [('all', u'все')]
    for room in rooms_num_db:
        rooms_num_choices.append((room['rooms_num'], room['rooms_num']))

    return rooms_num_choices


def getMinMonthPrice():
    return Apartment.objects.all().aggregate(Min('month_price'))['month_price__min']


def getMaxMonthPrice():
    return Apartment.objects.all().aggregate(Max('month_price'))['month_price__max']


class FilterForm(forms.Form):
    district = forms.MultipleChoiceField(label=u'Район', widget=BtnCheckboxSelectMultiple(attrs={'class': 'districts'}), choices=DISTRICT_CHOICES)
    rooms_num = forms.MultipleChoiceField(label=u'Количество комнат', widget=BtnCheckboxSelectMultiple(attrs={'class': 'rooms_nums'}), choices=getRoomNumChoices())
    month_price = forms.IntegerField(label=u'Цена за месяц', widget=CustomRangeInput(attrs={
        'id': 'price-max',
        'min': getMinMonthPrice(),
        'max': getMaxMonthPrice(),
        'step': 1000,
        'measure': u'рублей'
    }))
    fitnessclub_checkbox = forms.BooleanField(label='', widget=LabelCheckbox(attrs={'label': u'Фитнес центр', 'marker_icon': 'green.png'}), required=False)
    fitnessclub_distance = forms.IntegerField(label='', widget=CustomRangeInput(attrs={
        'id': 'fitnessclub',
        'min': 300,
        'max': 3000,
        'step': 100,
        'measure': u'метров'
    }))
    hospital_checkbox = forms.BooleanField(label='', widget=LabelCheckbox(attrs={'label': u'Больница', 'marker_icon': 'red.png'}), required=False)
    hospital_distance = forms.IntegerField(label='', widget=CustomRangeInput(attrs={
        'id': 'hospital',
        'min': 300,
        'max': 3000,
        'step': 100,
        'measure': u'метров'
    }))
    kindergarten_checkbox = forms.BooleanField(label='', widget=LabelCheckbox(attrs={'label': u'Детский сад', 'marker_icon': 'pink.png'}), required=False)
    kindergarten_distance = forms.IntegerField(label='', widget=CustomRangeInput(attrs={
        'id': 'kindergarten',
        'min': 300,
        'max': 3000,
        'step': 100,
        'measure': u'метров'
    }))
    school_checkbox = forms.BooleanField(label='', widget=LabelCheckbox(attrs={'label': u'Школа', 'marker_icon': 'blue.png'}), required=False)
    school_distance = forms.IntegerField(label='', widget=CustomRangeInput(attrs={
        'id': 'school',
        'min': 300,
        'max': 3000,
        'step': 100,
        'measure': u'метров'
    }))
    university_checkbox = forms.BooleanField(label='', widget=LabelCheckbox(attrs={'label': u'Университет', 'marker_icon': 'ocean.png'}), required=False)
    university_distance = forms.IntegerField(label='', widget=CustomRangeInput(attrs={
        'id': 'university',
        'min': 300,
        'max': 3000,
        'step': 100,
        'measure': u'метров'
    }))
    shopmall_checkbox = forms.BooleanField(label='', widget=LabelCheckbox(attrs={'label': u'Торговый центр', 'marker_icon': 'black.png'}), required=False)
    shopmall_distance = forms.IntegerField(label='', widget=CustomRangeInput(attrs={
        'id': 'shopmall',
        'min': 300,
        'max': 3000,
        'step': 100,
        'measure': u'метров'
    }))