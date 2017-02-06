#!/usr/bin/env python3
import sys, os
# Development. Production should have the dependancies installed.
sys.path.insert(0, '/home/sikkaflex/wrkspc/raven/vendor') # absolute
#sys.path.insert(0, os.path.join(sys.path[0], '../vendor')) # relative

import ravencore.main.config as raven_conf
from ravencore.utils.exceptions import *
import ravencore.utils.logging

import incl.header
import incl.footer

import ravencore.web_api.forms as forms
import ravencore.web_api.content as content


html = []
html += incl.header.get_header()
html += content.make_form(forms.new_book_form)
html += content.make_form(forms.book_search_form)
html += incl.footer.get_footer()
print(''.join(html))

