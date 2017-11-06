#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/PoliceStops/app")

from theapp import app as application
application.secret_key = 'DJ KHALEED'
