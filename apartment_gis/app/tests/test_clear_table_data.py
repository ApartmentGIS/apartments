import nose.tools as nt
from django_nose import FastFixtureTestCase
from django.core.management import call_command
from app.models import Apartment, Organization


class TestClearTableData(FastFixtureTestCase):
    fixtures = ['test_fixtures.json']

    def test_work(self):
        apartment_count_before = Apartment.objects.count()
        organization_count_before = Organization.objects.count()

        nt.assert_greater(apartment_count_before, 0)
        nt.assert_greater(organization_count_before, 0)

        call_command('clear_table_data')

        apartment_count_after = Apartment.objects.count()
        organization_count_after = Organization.objects.count()

        nt.assert_equal(apartment_count_after, 0)
        nt.assert_equal(organization_count_after, 0)