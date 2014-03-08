from django.contrib import admin
from models import Apartment

class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('address', 'district', 'rooms_num', 'month_price', 'floor')

admin.site.register(Apartment, ApartmentAdmin)