from fabric.api import *

def update_server():
    project_dir = '/home/ubuntu/apartments/apartment_gis/apartment_gis'
    with lcd(project_dir):
        local('git pull')
        local('rm settings.py')
        local('ln -s settings.py.production settings.py')
        local('python ../manage.py syncdb')
        local('sudo service postgresql restart')
        local('sudo service nginx restart')
        local('sudo supervisorctl restart all')
