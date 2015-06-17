#!/usr/bin/env python
#coding=utf8

import sys
from config import *

### start
print "initialize strating..."

### redis
try:
    redis.Redis(connection_pool=REDISPOOL).client_list()
    print "redis is connecting..."
except redis.ConnectionError:
    print "Redis cannot connect! please check it."
    sys.exit(1)

### log mkdir

