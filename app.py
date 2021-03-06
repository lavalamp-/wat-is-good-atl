#!/usr/bin/env python
'''
    Copyright 2012 Root the Box

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
----------------------------------------------------------------------------

This file is the main starting point for the application, based on the 
command line arguments it calls various components setup/start/etc.

'''


import os
import sys
import logging
import argparse

from datetime import datetime
from libs.ConsoleColors import *
from libs.FileHelpers import FileHelper
from data.DataGrabber import DataGrabber
from models import dbsession

__version__ = 'v0.0.1'
current_time = lambda: str(datetime.now()).split(' ')[1].split('.')[0]


def serve():
    ''' Starts the application '''
    from handlers import start_server
    print(INFO+'%s : Starting application ...' % current_time())
    start_server()


def create():
    ''' Creates/bootstraps the database '''
    from models import create_tables
    print(INFO+'%s : Creating the database ...' % current_time())
    create_tables()
    print(INFO+'%s : Bootstrapping the database ...' % current_time())
    import setup.bootstrap

def test():
    print("This is a test")
    orgs = FileHelper.get_organizations_from_file()
    DG = DataGrabber.instance()
    events = []
    for cur_org in orgs:
        for cur_event in cur_org['events']:
            events.append(DG.get_event_from_fb_dict(cur_event))
    print("Number of orgs: %s" % len(orgs))
    print("Number of events created: %s" % len(events))
    [dbsession.add(event) for event in events if event is not None]
    dbsession.flush()

def main(args):
    ''' Call functions in the correct order based on CLI params '''
    fpath = os.path.abspath(__file__)
    fdir = os.path.dirname(fpath)
    if fdir != os.getcwd():
        print(INFO+"Switching CWD to %s" % fdir)
        os.chdir(fdir)
    # Create tables / bootstrap db
    if args.create_tables:
        create()
    # Start server
    if args.start_server:
        serve()
    # Do test
    if args.do_test:
        test()


### Main
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Tornado WebApp',
    )
    parser.add_argument('-v', '--version',
        action='version',
        version=__version__,
    )
    parser.add_argument("-c", "--create-tables",
        action='store_true',
        dest='create_tables',
        help="create and initialize database tables (run once)",
    )
    parser.add_argument("-s", "--start",
        action='store_true',
        dest='start_server',
        help="start the server",
    )
    parser.add_argument("-t", "--test",
        action='store_true',
        dest='do_test',
        help='Run the test code in app.py'
    )
    main(parser.parse_args())
