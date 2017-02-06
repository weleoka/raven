#!/usr/bin/env python3
"""
Dipdap cgi script for handling form submissions from Dipdap web client.
"""
import cgi
import copy
import pprint

# Development. Production should have the dependancies installed.
sys.path.insert(0, '/home/sikkaflex/wrkspc/raven/vendor') # absolute
#sys.path.insert(0, os.path.join(sys.path[0], '../vendor')) # relative

import ravencore.web_api.config as api_config
import ravencore.web_api.forms as forms
import ravencore.web_api.content as content
import ravencore.web_api.proc as proc

import incl.header
import incl.footer


if dd_conf.db['type'] == "csv":
    DATABASE = dd_conf.db['name']

form = cgi.FieldStorage()
request_type = '' # String telling request type.
form_data = [] # list of tuples. Name value pairs.
html = []
html += incl.header.get_header()

unsubscribe = form.getvalue('unsubscribe_uuid')
print("SDFASDFSA {}".format(unsubscribe))

"""
request_type = form.getvalue('URL-query') if not api_config.basic['debug'] else 'book-search-form'

# html += ["Form length: %s \n" % (str(len(form.keys())))]

if request_type == 'new-entry-form':
    form_data = [
        ('title', form.getfirst('title', None)),
        ('author', form.getfirst('author', None)),
        ('genre', form.getfirst('genre', None)),
        ('score', form.getfirst('score', None)),
        ('finish', form.getfirst('finish', None)),
        ('comments', form.getfirst('comments', None))
    ]
    # Copy the original form so msgs can be apended to it.
    tmp_form_entity = copy.deepcopy(forms.new_book_form)

    if proc.validate_form_data(tmp_form_entity, form_data, html = True):
        entry = proc.prepare_db_entry(form_data)
        #dd_utils.filesystem.append_to_file(entry, DATABASE)
        html += ['New entry made.']

    else:
        html += content.make_form(tmp_form_entity)
        # html += ['New entry form failed server side validation.']

elif request_type == 'book-search-form':
    form_data = [
        ('column', form.getfirst('column', 1)),
        ('search', form.getfirst('search', None))
    ]

    if proc.validate_form_data(dd_main.forms.book_search_form, form_data, html = True):
        #dataset = dd_utils.filesystem.read_library_file(DATABASE)
        #res = dd_utils.proc.search_csv(dataset, form_data)
        html += content.output_html_table(res, api_config.db_csv_column_template)

    else:
        html += ['Search form failed server side validation.']

else:
    html += ['Invalid request recieved.']

html += ['<a href="index.py">Return</a>']
"""

html += incl.footer.get_footer()

try: # Stringify all the work!

    print(''.join(html))

except TypeError:

    raise TypeError("One of these list items are not a string: \n%s" % (pprint.pformat(html)))





