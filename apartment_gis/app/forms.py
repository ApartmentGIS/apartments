from django import forms

# DISTRICT_CHOICES = (
# 	(Leninsky, )
# )

class FilterForm(forms.Form):
	district = forms.MultipleChoiceField()
	rooms_num = forms.MultipleChoiceField()
	month_price = forms.DecimalField(min_value=0, max_value=15000)