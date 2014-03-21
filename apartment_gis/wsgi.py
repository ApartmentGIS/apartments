import os, sys
from django.core.handlers.wsgi import WSGIHandler

sys.path.append(os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = os.environ.get('DJANGO_SETTINGS_MODULE', 'apartment_gis.settings')

application = WSGIHandler()