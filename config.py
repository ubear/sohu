#!/usr/bin/env python
# coding=utf8

# configure for project

# web sites which we need to detect
SITE = "http://m.sohu.com/"

# include domain
INCLUDE_DOMAIN = ["m.sohu.com",
                  "zhibo.m.sohu.com",
                  "s.m.sohu.com",
                  "nbadata.m.sohu.com",
                  "m.film.sohu.com",
                  "m.tv.sohu.com",
                  "m.s.sohu.com",
                  "csldata.m.sohu.com",
                  "m.passport.sohu.com"
                  ]

# logging
LOG_DIR = "log"
LOG_CONTENT_FMT = '%(asctime)s-%(message)s'
LOG_FILENAME_FMT = "D_%Y-%m-%d_T%H%M"

# threading_number
THREAD_NUMBER = 100

# the total number of url
URL_TOTAL_NUM = 1000