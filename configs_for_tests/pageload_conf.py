# -*- coding: utf-8 -*-

import os

# set up CURRENT_SERVER env variable to select
# ex: SET CURRENT_SERVER=master
CURRENT_SERVER = None
try:
    CURRENT_SERVER = os.getenv("CURRENT_SERVER").lower()
except AttributeError:
    pass

if CURRENT_SERVER == 'test':
    from .test.pageload_conf import *
else:
    from .master.pageload_conf import *
