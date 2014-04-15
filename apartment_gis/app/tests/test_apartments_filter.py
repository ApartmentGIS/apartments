import nose.tools as nt
from django.http import QueryDict
from app.views import ApartmentsFilter, ORGANIZATIONS
from app.models import Apartment, Organization


INIT_FILTER = {
    'district': ['all'],
    'rooms_num': ['all'],
    'month_price': 50000,
    'kindergarten_distance': 3000,
    'school_distance': 3000,
    'university_distance': 3000,
    'hospital_distance': 3000,
    'fitnessclub_distance': 3000,
    'shopmall_distance': 3000
}


class TestGetFilter(object):
    def __init__(self):
        self.init_filter = INIT_FILTER.copy()

    def test_with_empty_params(self):
        apartmentsFilter = ApartmentsFilter(QueryDict(''))

        nt.assert_equal(self.init_filter, apartmentsFilter.get_filter())

    def test_with_param(self):
        expected_filter = self.init_filter.copy()
        expected_filter['district'] = [u'metal']
        expected_filter['rooms_num'] = [u'1']
        expected_filter['month_price'] = u'12345'
        expected_filter['fitnessclub_checkbox'] = u'on'
        expected_filter['fitnessclub_distance'] = u'500'
        expected_filter['hospital_checkbox'] = u'on'
        expected_filter['hospital_distance'] = u'1000'

        query_dict = QueryDict('district=metal&rooms_num=1&month_price=12345&fitnessclub_checkbox=on&fitnessclub_distance=500&hospital_checkbox=on&hospital_distance=1000')

        apartmentsFilter = ApartmentsFilter(query_dict)
        apartmentsFilter.update_filter_from_request()

        nt.assert_equal(expected_filter, apartmentsFilter.get_filter())


class TestUpdateFilterByCommonParams(object):
    def __init__(self):
        self.init_filter = INIT_FILTER.copy()

    def test_with_empty_params(self):
        apartmentsFilter = ApartmentsFilter(QueryDict(''))
        apartmentsFilter.update_filter_by_common_params(['district', 'rooms_num', 'month_price'])

        nt.assert_equal(self.init_filter, apartmentsFilter.get_filter())

    def test_with_not_empty_params(self):
        expected_filter = self.init_filter.copy()
        expected_filter['district'] = [u'metal', u'lenin']
        expected_filter['rooms_num'] = [u'1', u'2']
        expected_filter['month_price'] = u'12345'

        query_dict = QueryDict('district=metal&district=lenin&rooms_num=1&rooms_num=2&month_price=12345')

        apartmentsFilter = ApartmentsFilter(query_dict)
        apartmentsFilter.update_filter_by_common_params(['district', 'rooms_num', 'month_price'])

        nt.assert_equal(expected_filter, apartmentsFilter.get_filter())

    def test_dont_change_organizations_params(self):
        expected_filter = self.init_filter.copy()
        expected_filter['district'] = [u'metal', u'lenin']
        expected_filter['rooms_num'] = [u'1', u'2']
        expected_filter['month_price'] = u'12345'

        query_dict = QueryDict('district=metal&district=lenin&rooms_num=1&rooms_num=2&month_price=12345&hospital_checkbox=on&hospital_distance=1000')

        apartmentsFilter = ApartmentsFilter(query_dict)
        apartmentsFilter.update_filter_by_common_params(['district', 'rooms_num', 'month_price'])

        nt.assert_equal(expected_filter, apartmentsFilter.get_filter())


class TestUpdateFilterByOrganizations(object):
    def __init__(self):
        self.init_filter = INIT_FILTER.copy()

    def test_with_empty_params(self):
        apartmentsFilter = ApartmentsFilter(QueryDict(''))
        apartmentsFilter.update_filter_by_organizations(ORGANIZATIONS)

        print apartmentsFilter.get_filter()

        nt.assert_equal(self.init_filter, apartmentsFilter.get_filter())

    def test_with_not_empty_params(self):
        expected_filter = self.init_filter.copy()
        expected_filter['fitnessclub_checkbox'] = u'on'
        expected_filter['fitnessclub_distance'] = u'500'
        expected_filter['hospital_checkbox'] = u'on'
        expected_filter['hospital_distance'] = u'1000'

        query_dict = QueryDict('fitnessclub_checkbox=on&fitnessclub_distance=500&hospital_checkbox=on&hospital_distance=1000')

        apartmentsFilter = ApartmentsFilter(query_dict)
        apartmentsFilter.update_filter_by_organizations(ORGANIZATIONS)

        nt.assert_equal(expected_filter, apartmentsFilter.get_filter())

    def test_dont_change_common_params(self):
        expected_filter = self.init_filter.copy()
        expected_filter['fitnessclub_checkbox'] = u'on'
        expected_filter['fitnessclub_distance'] = u'500'
        expected_filter['hospital_checkbox'] = u'on'
        expected_filter['hospital_distance'] = u'1000'

        query_dict = QueryDict('district=metal&rooms_num=1&month_price=12345&fitnessclub_checkbox=on&fitnessclub_distance=500&hospital_checkbox=on&hospital_distance=1000')

        apartmentsFilter = ApartmentsFilter(query_dict)
        apartmentsFilter.update_filter_by_organizations(ORGANIZATIONS)

        nt.assert_equal(expected_filter, apartmentsFilter.get_filter())