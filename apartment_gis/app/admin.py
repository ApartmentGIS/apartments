from django.contrib import admin
from models import Apartment, NurserySchool

class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('address', 'district', 'rooms_num', 'month_price', 'floor')

class NurserySchoolAdmin(admin.ModelAdmin):
    lilst_display = ('name', 'address')

admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(NurserySchool, NurserySchoolAdmin)