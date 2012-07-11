import sys
import os
INTERP = "/usr/local/bin/python2.7"

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

import site
site.addsitedir('/home/seler/rails/commentary/site-packages')
site.addsitedir('/home/seler/rails/commentary/commentary')
site.addsitedir('/home/seler/rails/commentary')
#site.addsitedir('/home/seler/rails')

#sys.path.insert(0,'/home/seler/rails')
sys.path.insert(0,'/home/seler/rails/commentary')
sys.path.insert(0,'/home/seler/rails/commentary/commentary')
sys.path.insert(0,'/home/seler/rails/commentary/site-packages')

os.environ['LD_LIBRARY_PATH'] = '/usr/local/lib'
os.environ['DJANGO_SETTINGS_MODULE'] = 'commentary.settings'

import django.core.handlers.wsgi

#lapie bledy 500 ale potencjalnie wolniejsza metoda uruchomienia
from paste.exceptions.errormiddleware import ErrorMiddleware
application = django.core.handlers.wsgi.WSGIHandler()
application = ErrorMiddleware(application, debug=True)

#nie lapie bledow 500 ale szybszy
#application = django.core.handlers.wsgi.WSGIHandler()
