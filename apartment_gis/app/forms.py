# -*- coding: utf-8 -*-
import floppyforms as forms


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

ROOMS_NUM_CHOICES = (
	('all', u'все'),
	('1', '1'),
	('2', '2'),
	('big', 'большие')
)


class BtnCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
	template_name = 'floppyforms/btn_checkbox_select_multiple.html'


class CustomRangeInput(forms.RangeInput):
	template_name = 'floppyforms/custom_range_input.html'


class FilterForm(forms.Form):
	district = forms.MultipleChoiceField(label=u'Район', widget=BtnCheckboxSelectMultiple(attrs={'class': 'districts'}), choices=DISTRICT_CHOICES)
	rooms_num = forms.MultipleChoiceField(label=u'Количество комнат', widget=BtnCheckboxSelectMultiple(attrs={'class': 'rooms_nums'}), choices=ROOMS_NUM_CHOICES)
	month_price = forms.IntegerField(label=u'Цена за месяц', widget=CustomRangeInput(attrs={
		'id': 'price-max',
		'min': 6000,
		'max': 50000,
		'step': 1000,
		'measure': u'рублей'
	}))
	kindergarten_distance = forms.IntegerField(label=u'Детский сад', widget=CustomRangeInput(attrs={
		'id': 'kindergarten',
		'min': 300,
		'max': 3000,
		'step': 100,
		'measure': u'метров'
	}))