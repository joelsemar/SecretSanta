import os, sys
sys.path.insert(0, '/var/www/SecretSanta')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()    

