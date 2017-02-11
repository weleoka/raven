#!/usr/bin/env python3
# Copyright (c) 2017 Kai Weeks.
#

from db_tool import Db_tool

def run_test():

    db_tool = Db_tool()

    my_dict = {
        'items_type': 'mail_in',
        'item_id_str': '',
        'attr_category': [None],
        'check': True,
        'depth': 4,
        'search': '',
    }
    #db_tool.process_items(**my_dict)
    my_dict = {
        'items_type': 'job',
        'item_id_str': '',
        'attr_category': [None],
        'check': True,
        'depth': 4,
        'search': '',
    }
    #db_tool.process_items(**my_dict)


    my_dict = {
        'items_type': 'mail_out',
        'item_id_str': '',
        'attr_category': [None],
        'check': True,
        'depth': 4,
        'search': '',
    }
    #db_tool.process_items(**my_dict)
    my_dict = {
        'items_type': 'newsletter',
        'item_id_str': '',
        'attr_category': [None],
        'check': True,
        'depth': 4,
        'search': None,
    }
    #db_tool.process_items(**my_dict)

    my_dict = {
        'items_type': 'user',
        'item_id_str': '',
        'attr_category': ['basic'],
        'attr': ['services'],
        'check': True,
        'depth': 4,
        'search': ['maluel40.transat@gmail.com'],
        'search_path': ['parameters', 'source_addresses'],
        'output_level': 'search',
        'output_pipe': 'return',
    }
    #db_tool.process_items(**my_dict)









    # Find all services of the required type.
    my_dict = {
        'items_type': 'user',
        'attr_category': ['all'],
        #'attr': ['services'],
        'search_path': [],
        'search': ['newsletter'],
        'output_level': 'search',
        'output_pipe': 'return',
    }
    #db_tool.process_items(**my_dict)
    
    att_res, data_res = db_tool.process_items(**my_dict)

    for path in data_res:
        search_path = path[0:-1] + ['parameters', 'source_addresses'] # Take away the service_alias add custom.
        my_dict = {
            'items_type': 'user',
            'attr': ['services'],
            'search_path': search_path,
            'search': ['kai.weeks@gmail.com'],
            'output_level': 'search',
            'output_pipe': 'return',
        }

        att_res, data_res = db_tool.process_items(**my_dict)
        print("\n\n", data_res)



if __name__ == "__main__":

    try:
        run_test()

    except KeyboardInterrupt:
        logger.info("Db_tool halted by keyboard interrupt.")
        sys.exit(0)
