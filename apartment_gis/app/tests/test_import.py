import nose.tools as nt
from django.core.management.base import CommandError
from django_nose import FastFixtureTestCase
from app.models import Apartment, Organization
from django.core.management import call_command


class TestAptImport(FastFixtureTestCase):
    fixtures = ['test_fixtures.json']

    def test_params_call(self):
        records_num_before = Apartment.objects.count()
        call_command('data_import', apt_filename='/tests/data_for_tests/test_apt_data.csv')
        nt.assert_equal(Apartment.objects.count(), records_num_before+1)

    def test_wrong_input(self):
        records_num_before = Apartment.objects.count()
        with nt.assert_raises(CommandError):
            call_command('data_import')
        nt.assert_equal(Apartment.objects.count(), records_num_before)

    def test_import_empty_file(self):
        records_num_before = Apartment.objects.count()
        call_command('data_import', apt_filename='/tests/data_for_tests/test_data_empty.csv')
        nt.assert_equal(Apartment.objects.count(), records_num_before)

    def test_import_added_apt(self):
        records_num_before = Apartment.objects.count()
        try:
            call_command('data_import', apt_filename='/tests/data_for_tests/test_apt_data_added.csv')
        except:
            nt.assert_equal(Apartment.objects.count(), records_num_before)


class TestOrgImport(FastFixtureTestCase):
    fixtures = ['test_fixtures.json']

    def test_params_call(self):
        records_num_before = Organization.objects.count()
        call_command('data_import', org_filename='/tests/data_for_tests/test_organization_data.csv')
        nt.assert_equal(Organization.objects.count(), records_num_before+1)

    def test_import_empty_file(self):
        records_num_before = Organization.objects.count()
        call_command('data_import', org_filename='/tests/data_for_tests/test_data_empty.csv')
        nt.assert_equal(Organization.objects.count(), records_num_before)

    def test_import_added_org(self):
        records_num_before = Organization.objects.count()
        try:
            call_command('data_import', org_filename='/tests/data_for_tests/test_org_data_added.csv')
        except:
            nt.assert_equal(Organization.objects.count(), records_num_before)
