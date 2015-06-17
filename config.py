#!/usr/bin/env python
#coding=utf8

# configure for project
import redis

### logging
#LOG_DIR = "/var/www/minitor/"
FMT = '%(asctime)s - %(thread)d - %(message)s'

### web sites which we need to detect
SITES = {"Msouhu":"http://m.sohu.com/"}

### Redis setting
REDISPOOL = redis.ConnectionPool(host="localhost", port=6379, db=0)

### timer setting


### threading_number
THREAD_NUMBER = 2
###



