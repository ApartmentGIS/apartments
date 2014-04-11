from fabric.api import *


def prepare_test_instance():
    local('ln -sf settings.py.production settings.py')


def start_test():
    local('coverage run --source="." manage.py test --noinput')
    local('coverage html')


def update_server():
    project_dir = '/home/ubuntu/apartments/apartment_gis/apartment_gis'
    with lcd(project_dir):
        local('git pull')
        local('ln -sf settings.py.production settings.py')
        local('python ../manage.py migrate app')
        local('service postgresql restart')
        local('service nginx restart')
        local('supervisorctl restart all')
