#!/usr/bin/env python
# coding=utf8

import sys

from sohu import SohuUrlCheck
from base import BaseUrlCheck


def sohu_job():
    sohu = SohuUrlCheck()
    sohu.process()

def base_job(domain):
    base = BaseUrlCheck(domain)
    base.process()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        base_job(sys.argv[1])
    else:
        sohu_job()
    print "OK"
