#!/usr/bin/env python3
# Copyright (c) 2017 Kai Weeks.
#
# See LICENSE for details.
"""
Database tool for raven database.

- Checks dbitems for consistency, warnings raised if data is non-conformant.
- Gives statistics on dbitems.
- Advanced searches in datastructures.
- Human readable output of dbitems.
- Manual adding of dbitems.
- Initial reset db procedures.

"""

import sys, os
import logging as logger
import json
import pprint

# Development. Production should have the dependancies installed.
#sys.path.insert(0, '/home/sikkaflex/wrkspc/raven/vendor') # absolute
sys.path.insert(0, os.path.join(sys.path[0], 'vendor')) # relative

import ravencore.main.config as raven_conf
from ravencore.utils.exceptions import *
import ravencore.utils.logging

import dbdefaults

from ravencore.user.user import User
from ravencore.main.job import Job
from ravencore.coms.mail import Newsletter, Mail_out, Mail_in

from ravencore.utils.helpers import merge_dicts2 as merge_parameters
from ravencore.utils.helpers import search_dict_keys, search_dict_values


PARAMS = {
    'user': {
        'instance': 'user',#User(),
        'attr_category': {
            'all': list(raven_conf.user_default_params.keys()),
            'basic': [
                'name',
                'email',
                'alternate_email',
                'password',
                'doomsday'
            ],
            'none': [],
        },
    },
    'mail_in': {
        'instance': 'mail_in',#Mail_in(),
        'attr_category': {
            'all': list(raven_conf.mail_in_default_params.keys()),
            'basic': [
                'fr',
                'subject',
            ],
            'all_not_headers': [
                attr for attr in list(raven_conf.mail_in_default_params.keys())
                if attr not in ['headers']
            ],
            'custom': [
                attr for attr in list(raven_conf.mail_in_default_params.keys())
                if attr not in ['headers', 'html', 'body']
            ],
            'content': [
                'fr',
                'subject',
                'body',
            ],
            'none': [],
        },
    },
    'mail_out': {
        'instance': 'mail_out',#Mail_out(),
        'attr_category': {
            'all': list(raven_conf.mail_out_default_params.keys()),
            'basic': [
                'to',
                'sender',
                'user_id',
                'subject',
                'text',
            ],
            'none': [],
        },
    },
    'newsletter': {
        'instance': 'newsletter',#Newsletter(),
        'attr_category': {
            'all': list(raven_conf.newsletter_default_params.keys()),
            'basic': [
                'subject',
                'subscribers',
                'sender',
                'user_id',
                'unsubscribe_tuples',
                #'text',
            ],
            'none': [],
        },
    },
    'job': {
        'instance': 'job',#Job(),
        'attr_category': {
            'all': list(raven_conf.job_default_params.keys()),
            'basic': [
                'user_id',
                'mail_id',
                'on_behalf_of_user',
                'user_service_id',
                'service_sequence_type',
                'service_alias',
                #'created',
                'request_carrier',
                #'debug',
            ],
            'none': [],
        },
    },
}


class Db_tool:
    """
    Class representing the raven db_tool.

    """


    def __init__(self):
        """
        Constructor for class.

        parameters:
            incoming_mail_out_params: dict. Mail_out parameters

        return:
            void
        """
        name = '.'.join([__name__, self.__class__.__name__])
        self.logger = ravencore.utils.logging.getLogger(name)

        self.search_param = [] # List of search strings.
        self.attr_search_res = [] # Results for an attribute search go here as (path, attribute_value) tuples.
        self.data_search_res = [] # Results for an attribute value search go here as (path, attribute_value) tuples.

        self.db = raven_conf.dbredis()


    def read_param(self):
        try:
            if sys.argv[1] == 'reset':
                while True:
                    opt = input("Really reset it all or only default data structures (d)? (y/n/d)")
                    if opt == 'y':
                        self.__reset_users()
                        self.__reset_newsletters()
                        self.__reset_mail_in()
                        self.__reset_mail_out()
                        self.__reset_job()
                        self.__reset_default_data_structures()
                        break
                    elif opt == 'd':
                        self.__reset_default_data_structures()
                    elif opt == 'n': break
        except IndexError:
            pass


    def main(self):
        """
        Db_tool for Raven main function

        parameters:
            void

        returns:
            boolean:
        """
        self.read_param()


    def process_items(self, items_type=None,item_id_str=None,attr_category=['basic'],attr=[],
            check=True,depth=2,search=None, **kwargs):
        """
        Gets an item or iterates through multiple items in db and prints.

        Print levels correspond to object attributes and weather or not they should be output.
        If None is passed then attributes under alias 'basic' will be printed.

        A search string can be supplied in which case the attributes them selves, and their values
        will be checked for a match. If the value is a dictionary it in turn will have its keys and
        values searched. If a value is a list then the list items will be checked for a match.

        Note that the search only searches attributes which are in attr_category or attr.

        parameters:
            items_type: obj. An instance of a Dbitem subclass as an iterator.
            item_id_str: string. If a single object is to be printed.
            attr_category: list. Decide which attribute categories to print.
            attr: string
            check: bool. Check if object has all the required attributes.
            depth: int. How far to descend into nested data structures. (Does not apply to search)
            search: string. If set only values a key matching the search will be printed.

        return:
            complex
        """
        tmp = PARAMS.get(items_type)
        instance_type = tmp.get('instance')
        items = self.create_instance(instance_type, item_id_str)
        attributes = []

        if attr_category is None:
            attr_category = ['basic']
        else:
            for cat in attr_category:
                attributes += tmp.get('attr_category')[cat]
        if attr:
            attributes += attr

        net_pass = True
        check_str = "" # If any item fails check this variables are set.

        self.attr_search_res = list()
        self.data_search_res = list()

        i = 0
        op = ["\n\n- - - {} - - -".format(instance_type)] # This is where all program op goes.

        attrs_not_valid = [attr for attr in attributes if attr not in items.default_attributes.keys()]
        if attrs_not_valid:
            for non_valid in attrs_not_valid:
                op += ["\nWARN: selected attr {} is not an attr of {} object.".format(attr, instance_type)]
                attributes.remove(non_valid)

        for item in items:
            item.fetch()
            i += 1

            attrs_not_set = [] # A list of attributes not set. ie. None, [], ''.
            attrs_not_valid = [] # Attributes not in items default attributes.
            attrs_not_selected = [] # Item default attributes but not selected for print or search.

            op += "\n\n(old)" if item.is_processed() else "\n\n(new)"

            if len(item.id) < 7: op += ["\t{}:\t".format(item.id)]
            if len(item.id) > 7: op += ["\t{}:".format(item.id)]

            if check:
                item_pass, check_str = self.check_item(item)
                net_pass = item_pass if not item_pass else net_pass
                op += ["\t\t\t{}".format(check_str)]

            attrs_not_set = [attr for attr in attributes if getattr(item, attr) in [None, [], '', {}]]
            if attrs_not_set:
                op += ["\nselected but empty attributes: {}".format(attrs_not_set)]
            attrs_not_selected = [attr for attr in item.default_attributes.keys() if attr not in attributes]
            if attrs_not_selected:
                op += ["\nnon-selected attributes: {}".format(len(attrs_not_selected))]

            for attr in attributes:
                if attr in attrs_not_set: continue
                else: data = getattr(item, attr, None)

                if isinstance(data, dict):
                    op += ["\n{}: ".format(attr)]
                    op += [pprint.pformat(data)]
                else:
                    op += ["\n{}: {}".format(attr, data)]

            self.search_in_item(item, attributes, search, **kwargs)
            self.output_handler(item, op, **kwargs)

        if i == 0:
            op += ["\n\nNo relevant %s items in db." % (items_type)]

        return self.output_handler(item, op, iter_complete=True, **kwargs)


    def output_handler(self,item,output=None,iter_complete=False,output_level='all',output_pipe='stdout', **kwargs):
        """
        Parameters select which output and to route to where.

        parameters:
            item: obj. The item.
            output_level: string. What to output
                - 'all' keep all output to pass on.
                - 'search' keep search results only.
            output_pipe: string. What to do with class output data.
                - 'stdout' print to console.
                - 'return' return a python object with class output.
            output: list. A list of strings of human readable output.
            iter_complete: bool. False until all items have been iterated.

        return:
            complex
        """
        if output_level == None: output_level = 'all'
        if output_pipe == None: output_pipe = 'stdout'
        if output is None: return

        if output_level == 'all':
            if output_pipe == 'stdout':
                if not iter_complete:
                    output += self.format_search_res()
                elif iter_complete:
                    print("{}".format(''.join(output)))
            elif output_pipe == 'return':
                if iter_complete:
                    return output

        elif output_level == 'search':
            if output_pipe == 'stdout':
                if not iter_complete:
                    # output += self.format_search_res()
                    print("\n{}".format(item.id))
                    print("{}".format(''.join(self.format_search_res())))
                elif iter_complete:
                    pass
                    # print(''.join(output))
            elif output_pipe == 'return':
                if iter_complete:
                    if len(self.attr_search_res) > 1:
                        self.attr_search_res = [res for res in self.attr_search_res if res]
                    if len(self.data_search_res) > 1:
                        self.data_search_res = [res for res in self.data_search_res if res]
                    return self.attr_search_res, self.data_search_res


    def search_in_item(self, item, attributes, search, search_path=[], **kwargs):
        """
        Searches an objects attributes.

        parameters:
            item: obj. The item who's attributes are being searched.
            attributes: The attributes being searched.
            search: list. A list of strings to search for.
            search_path: list. Only return results from specific path.

        return:
            void
        """
        if not search: return
        self.search_param = search

        for attr in attributes:
            data = getattr(item, attr, None)
            top_path = [item.id, attr]

            for search_str in self.search_param:

                if attr == search_str:
                    self.attr_search_res.append((top_path, data))
                if data == search_str:
                    self.data_search_res.append(top_path)

                if isinstance(data, dict):
                    self.attr_search_res += search_dict_keys(search_str, data, top_path)
                    self.data_search_res += search_dict_values(search_str, data, top_path)

        if search_path:
            tmp_list = []

            for search_res in self.data_search_res:
                if len(search_res) == len(search_path): # They are equal length.
                    #print("We are equal", search_res, search_path)
                    matches = [ # All search_path_items have to exist in search_res.
                        search_path_item for search_path_item in search_path
                        if search_path_item in search_res
                    ]

                    if len(matches) == len(search_path):
                        tmp_list.append(search_res)

                else:
                    #print("We are not equal.", search_res, len(search_res), search_path, len(search_path))
                    pass
            self.data_search_res = tmp_list

            # self.data_search_res = [
            #     search_res for search_res in self.data_search_res # The search results, a list of lists.
            #     if len([ # All search_path_items have to exist in search_res.
            #         search_path_item for search_path_item in search_path
            #         if search_path_item in [search_res for search_res in self.data_search_res]
            #     ]) == len(search_path)
            # ]


    def format_search_res(self):
        """
        Outputs results of a search.

        parameters:

        return:
            list. The strings of search results in a list.
        """
        search_res_output = []

        if self.attr_search_res:
            search_res_output += ["\nAttribute search results for {}".format(self.search_param)]

            for path, value in self.attr_search_res:

                if isinstance(value, dict):
                    search_res_output += ["\n{} value:".format(path)]
                    search_res_output += ["\n" + pprint.pformat(value)]
                else:
                    search_res_output += ["\n{} value: '{}':".format(path, value)]

        if self.data_search_res:
            search_res_output += ["\nValue search results for {}".format(self.search_param)]
            search_res_output += [
                "\n{}".format(path) for path in self.data_search_res
            ]

        elif not self.attr_search_res and not self.data_search_res:
            search_res_output += ["\nNo results for search."]

        # Reset the search results for the next item:
        self.attr_search_res = []
        self.data_search_res = []

        return search_res_output


    def create_instance(self, instance_type, item_id_str):
        """
        Checks that the db item has all the required attributes.

        parameters:
            instance_type: string. An instance type identifier
            item_id_str: string. A specific instance of the object.

        return:
            void
        """
        #-> This is not done right. This is so that if item_id_str is set
        #   then the instatiated class will be a non-iterable. Current hackish workaround:
        if instance_type == 'user':
            items = User(item_id_str)
        if instance_type == 'mail_in':
            items = Mail_in(item_id_str)
        if instance_type == 'mail_out':
            items = Mail_out(item_id_str)
        if instance_type == 'newsletter':
            items = Newsletter(item_id_str)
        if instance_type == 'job':
            items = Job(item_id_str)

        return items


    def check_item(self, item):
        """
        Checks that the db item has all the required attributes.

        parameters:
            item: obj. The instance of a dbitem subclass.

        return:
            void
        """
        net_pass = True
        failed_attr_str = ""
        net_chck_res_str = "(attr_check: OK)"

        for attr in item.default_attributes.keys():
            data = getattr(item, attr, 'error')

            if data is 'error':
                self.logger.warning("%s is lacking an attribute: %s" % (item.id, attr))
                #raise ValueError("%s is lacking an attribute: %s" % (item.id, attr))
                net_pass = False
                failed_attr_str += attr + ","

        if not net_pass:
            net_chck_res_str = "(attr_check: FAILED - %s)" % (failed_attr_str)

        return net_pass, net_chck_res_str



### Object specific methods for reseting object presence in db.

    def __reset_apscheduler(self):
        """
        Removes all the jobs and jobstores for the Apscheduler.

        parameters:

        return:
            void
        """
        self.db.delete(raven_conf.apscheduler_runtime_keys_redis)
        self.db.delete(raven_conf.apscheduler_jobstore_redis)

    def __reset_users(self):
        """
        Resets the users to defaults.

        parameters:

        return:
            void
        """
        user_count = 0

        for user_id, user_dict in dbdefaults.base_userdb.items():
            user_count += 1

            user_params = dict(merge_parameters(raven_conf.user_default_params, user_dict))
            self.db.set(user_id, json.dumps(user_params))
        #-> User() also has a processed key. It is not reset here.
        self.logger.info("User database loaded with %s default users." % (user_count))

    def __reset_newsletters(self):
        keep = []
        items = Newsletter()
        [self.db.delete(item.id) for item in items if item.id not in keep]
        self.db.delete(items.get_processed_key())

    def __reset_mail_in(self):
        keep = ['mail_in1', 'mail_in2', 'mail_in3']
        items = Mail_in()
        [self.db.delete(item.id) for item in items if item.id not in keep]
        self.db.delete(items.get_processed_key())

    def __reset_mail_out(self):
        keep = []  #['mail_out1', 'mail_out2', 'mail_out3']
        items = Mail_out()
        [self.db.delete(item.id) for item in items if item.id not in keep]
        self.db.delete(items.get_processed_key())

    def __reset_job(self):
        keep = []  # ['job1', 'job2', 'job3']
        items = Job()
        [self.db.delete(item.id) for item in items if item.id not in keep]
        self.db.delete(items.get_processed_key())

    def __reset_default_data_structures(self):
        for dds_name, dds_data in raven_conf.default_data_structures.items():
            self.db.set(dds_name, json.dumps(dds_data))

if __name__ == "__main__":

    # Set up the logging of db_tools.
    ravencore.utils.logging.initialiseLogging()

    my_logger = ravencore.utils.logging.getLogger()
    my_logger.info("Db_tool for Raven_com v%s" % (raven_conf.basic['version']))
    my_logger.info("SYS.PATH: %s" % (sys.path))

    db_tool = Db_tool()

    try:
        db_tool.main()

    except KeyboardInterrupt:
        logger.info("Db_tool halted by keyboard interrupt.")
        sys.exit(0)
