from django.shortcuts import render
from models import Apartment
from forms import FilterForm


def home(request):
	apartment_list = Apartment.objects.all()

	return render(request, 'index.html', {'apartment_list': apartment_list, 'form': FilterForm()})
