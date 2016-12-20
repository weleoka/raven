#!/usr/bin/env python3
# Copyright (c) 2017 Kai Weeks.
# See LICENSE for details.
"""
Main app to connect an email snd/rcv functionality and fish instructions out of messages. 
These messages act as commands for Raven.

Raven presents an Email API to interface to web API services. 

Please report any issues to weleoka at github.
"""

import sys, os 

# Development. Production should have the dependancies installed.
sys.path.insert(0, os.path.join(sys.path[0], 'vendor'))

import traceback
import fileinput # https://docs.python.org/2/library/fileinput.html
import subprocess
import logging

import ravencore.config as ravenconf
import ravencore.logging_tools
from ravencore.gmail_in import Gmail_in

import pprint

ravencore.logging_tools.initialiseLogging(ravencore.config)


def main():
    """
    Raven's main function

    The function from which all else takes place.

    parameters:
        void

    returns:
        boolean:
    """
    logging.info("Raven v%s" % (ravencore.config.basic['version']))
    
    mail_in = Gmail_in(ravenconf.email_in)
    mail_in.connect()
    all_messages = mail_in.all()

    for mail in all_messages:
        print(mail.header.decode(encoding='UTF-8',errors='strict'))
        print(mail.body.decode(encoding='UTF-8',errors='strict'))
 
        for attachment in mail.attachments:
            print('Saving attachment: %s' % (attachment.name))
            print('Size: %s KB' % (attachment.size))
            attachment.save('attachments/%s' % (attachment.name))







if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        logging.info("Raven halted by keyboard interrupt.")
        sys.exit()





    '''
        if raven.email.Email_in.connectIMAP():
        logging.info("Established IMAP connection to %s" % email_in.server)
        email_in.closeIMAP()
        logging.info("Closed IMAP connection to %s" % email_in.server)

    else:
        logging.info("Failed to establish IMAP connection to %s" % email_in.server)

'''