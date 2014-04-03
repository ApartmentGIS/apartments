from fabric.api import local

def update_server():
    local('git pull')
	local('rm settings.py')
	local('ln -s settings.py.production settings.py')
	local('python ../manage.py syncdb')
	local('service postgresql restart')
	local('service nginx restart')
	local('supervisorctl restart all')
