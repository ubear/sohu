#!/usr/bin/env python
#coding=utf8
import redis
# configure for project


### web sites which we need to detect
SITE = "http://m.sohu.com/"

### include domain
INCLUDE_DOMAIN=["m.sohu.com",
                "zhibo.m.sohu.com",
                "s.m.sohu.com",
                "nbadata.m.sohu.com",
                "m.film.sohu.com",
                "m.tv.sohu.com",
                "m.s.sohu.com",
                "csldata.m.sohu.com"]

### logging
LOG_DIR = "/var/www/minitor/"
FILE_FMT = '%(asctime)s-%(levelname)s-%(message)s'



### Redis setting
REDIS_POOL = redis.ConnectionPool(host="localhost", port=6379, db=0)

### threading_number
THREAD_NUMBER = 5

### url_total_num
URL_TOTAL_NUM = 100000

### Queue capacity
QUEUE_CAPACITY = 1000



