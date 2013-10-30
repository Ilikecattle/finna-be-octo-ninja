import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/adam/webdev/register_slc/env/lib/python2.7/site-packages')

sys.path.append('/home/adam/webdev/register_slc')

os.environ['DJANGO_SETTINGS_MODULE'] = 'register_slc.settings'

# Activate your virtual env
activate_env=os.path.expanduser("/home/adam/webdev/register_slc/env/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
