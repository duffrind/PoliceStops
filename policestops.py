#!/usr/bin/python3
import sys
import logging
import json
import os
from app.views import app as application

logging.basicConfig(stream=sys.stderr)
application.secret_key = 'whatislove'

if __name__ == '__main__':
    application.debug = True
    port = int(os.environ.get("PORT", 5000))
    application.run(host='0.0.0.0', port=port)
