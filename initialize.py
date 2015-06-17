#!/usr/bin/env python
#coding=utf8

import sys
import os
from config import *
from urlparse import urlparse


def start():
    ### start
    print "initialize strating..."

    ### redis
    try:
        redis.Redis(connection_pool=REDIS_POOL).client_list()
        print "redis is connecting..."
    except redis.ConnectionError:
        print "Redis cannot connect! please check it."
        sys.exit(1)

    ### log mkdir
    try:
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
            print "Log direction creates succesfully!"
    except OSError:
        print "Creating log direction has error, please try 'sudo' command."
        sys.exit(1)
    except:
        print "create log direction fail......"
        sys.exit(1)
