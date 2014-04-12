from django.contrib import admin
from models import Apartment, Organization

class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('address', 'district', 'rooms_num', 'month_price', 'floor')

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'address')

admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Organization, OrganizationAdmin)