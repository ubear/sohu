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
    # import urllib
    import urllib2
    from bs4 import BeautifulSoup

    # sock = urllib.urlopen("http://m.sohu.com/")
    # soup = BeautifulSoup(sock.read())
    # sock.close()
    #
    # img = soup.findAll("img", src=True)
    # script = soup.findAll("script", {"type" : "text/javascript"}, src=True)
    # css = soup.findAll("link", href=True)
    #
    # print img
    # print script
    # print css

    headers = {"User-Agent": 'Mozilla 5.10', "Connection": "close"}
    request = urllib2.Request("http://m.sohu.com/", headers=headers)
    response = urllib2.urlopen(request)
    page = response.read().decode('utf-8')
    soup = BeautifulSoup(page)
    img = soup.findAll("img")
    script = soup.findAll("script", {"type" : "text/javascript"}, src=True)
    css = soup.findAll("link", href=True)

    print img
    print script
    print css



