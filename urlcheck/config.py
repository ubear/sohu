#!/usr/bin/env python
# coding=utf8

# configure for project


# web domain which we need to detect
DOMAIN = "http://m.sohu.com/"


# logging
LOG_DIR = "/tmp/log"
LOG_CONTENT_FMT = '%(asctime)s-%(message)s'
LOG_FILENAME_FMT = "D_%Y-%m-%d_T%H%M"


# threading_number
THREAD_NUMBER = 100


# the total number of url
URL_TOTAL_NUM = 10000


# the interval for exc the job and the
INTERVAL_EXC = 10 * 60 

