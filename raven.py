#!/usr/bin/env python3
# Copyright (c) 2017 Kai Weeks.
# See LICENSE for details.
"""
Main app to connect an email snd/rcv functionality and fish instructions out of messages.

These messages act as commands for Raven.

Raven presents an Email API to interface with web API services. 

Please report any issues to weleoka at github.
"""

import sys, os
import logging as logger
import pprint

# Development. Production should have the dependancies installed.
sys.path.insert(0, os.path.join(sys.path[0], 'vendor'))

import ravencore.main.config as raven_conf
import ravencore.utils.logging_tools

from ravencore.main.queue import Queue
from ravencore.main.job import Job

from ravencore.coms.gmail import Gmail_in
from ravencore.coms.gmail import Gmail_out

from ravencore.user.user import User
from ravencore.user.request import Request

ravencore.utils.logging_tools.initialiseLogging(raven_conf)



def main():
    """
    Raven's main function

    The function from which all else takes place.

    parameters:
        void

    returns:
        boolean:
    """
    logger.info("Raven v%s" % (raven_conf.basic['version']))
    
    #test_user_query()
    #test_send_mail_saildocs(query)
    # position = test_dolink()
    test_autogrib()

    #test_HTTP_headers()
    #test_recieve_mail()
    #test_send_mail()


def test_autogrib():
    queue = Queue()
    current_user = User('user2')
    service_request = Request(current_user, 'service1')
    job = Job(service_request)

    queue.add_to_request_queue(job)

    mail_out = Gmail_out()#.connect()
    mail_out.new_mail(job.job['mail'])
    mail_out.close()



def test_send_mail_saildocs():
    mail_out = Gmail_out().connect()
    mail_out.saildocs_request_mail()
    mail_out.close()



def test_send_mail():
    mail_out = Gmail_out().connect()
    mail_out.test_mail()
    mail_out.close()

def test_recieve_mail():
    mail_in = Gmail_in().connect()
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
        logger.info("Raven halted by keyboard interrupt.")
        sys.exit()