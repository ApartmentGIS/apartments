from fabric.api import *


def prepare_test_instance():
    local('ln -sf settings.py.production settings.py')


def start_test():
    local('coverage run --source="." manage.py test --exe --noinput')
    local('coverage html')


def update_server():
    project_dir = '/home/ubuntu/apartments/apartment_gis'

    with lcd(project_dir):
        local('git pull')
        local('ln -sf /home/ubuntu/apartments/apartment_gis/apartment_gis/settings.py.production apartment_gis/settings.py')
        #
        # uncomment following lines, if you make migration
        #
        #local('python manage.py clear_table_data')
        #local('python manage.py migrate --noinput')
        #local('python manage.py data_import --apt_filename=apartments.csv')
        #local('python manage.py data_import --org_filename=organizations.csv')
        local('service postgresql restart')
        local('service nginx restart')
        local('supervisorctl restart all')