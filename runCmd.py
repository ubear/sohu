#!/usr/bin/env python
# -*- coding=utf8 -*-

import sys

from sohu import SohuUrlCheck
from sample import SampleUrlCheck


def sohu_job():
    sohu = SohuUrlCheck()
    sohu.process()

def sample_job(domain):
    sample = SampleUrlCheck(domain)
    sample.process()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sample_job(sys.argv[1])
    else:
        sohu_job()
    print "OK"
