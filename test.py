#!/usr/bin/env python
# -*- coding=utf8 -*-

import urlparse

from sohu import SohuUrlCheck


def __check_domain(url1):
    url_hostname = urlparse.urlparse(url1).hostname
    if url_hostname.endswith("m.sohu.com"):
        return True
    if url_hostname.startswith("m.") and url_hostname.endswith(".sohu.com"):
        return True
    return False

if __name__ == "__main__":
    u = [None, "sss", "  \n\t ", "http://m.baidu.com", "http://m.sohu.com", "http://data.m.sohu.com",
         "http://m.data.sohu.com",
         "http://s1.rr.itc.cn/h5/js/tags/v3/msohu/3.1.37/home.js"]
    # for item in u:
    #     print SohuUrlCheck.check_domain(item)

    sh = SohuUrlCheck()
    for item in u:
        print sh.vaditator(item)
