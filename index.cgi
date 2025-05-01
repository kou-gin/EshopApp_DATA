#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app", "lib"))

try:
    from app import app
    from flup.server.cgi import WSGIServer
    WSGIServer(app).run()
except Exception:
    with open("/home/gins-net25/www/error.log", "w") as f:
        f.write(traceback.format_exc())