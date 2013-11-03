import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/usr/local/www/register_slc/env/lib/python2.7/site-packages')

sys.path.append('/usr/local/www/register_slc')

os.environ['DJANGO_SETTINGS_MODULE'] = 'register_slc.settings'

# Activate your virtual env
activate_env=os.path.expanduser("/usr/local/www/register_slc/env/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
