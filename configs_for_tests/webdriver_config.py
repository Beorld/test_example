# -*- coding: utf-8 -*-

import os

# set up CURRENT_SERVER env variable to select
# ex: SET CURRENT_SERVER=test
CURRENT_SERVER = None
try:
    CURRENT_SERVER = os.getenv("CURRENT_SERVER").lower()
except AttributeError:
    pass

if CURRENT_SERVER == 'test':
    from .test.webdriver_config import *
else:
    from .master.webdriver_config import *
