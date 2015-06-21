#!/usr/bin/env python
# coding=utf8

import urllib2
import urlparse

from bs4 import BeautifulSoup
from lepl.apps.rfc3696 import HttpUrl

from urlcheck import worker
from urlcheck import config


class SohuUrlCheck(worker.CheckUrl):

    def __init__(self):
        super(SohuUrlCheck, self).__init__(domain="http://m.sohu.com/")
        self.vaditator = HttpUrl()

    def extract_url(self, url):
        urls = []
        headers = {"User-Agent": 'Mozilla 5.10', "Connection": "close"}
        request = urllib2.Request(url.encode('utf-8'), headers=headers)
        try:
            response = urllib2.urlopen(request)
            page = response.read().decode('utf-8')
            soup = BeautifulSoup(page)
            for tag in soup.findAll('a', href=True):
                url_item = urlparse.urljoin(self.domain, tag['href'])
                if self.vaditator(url_item) and self.check_domain(url_item):
                    urls.append(url_item)
        except urllib2.HTTPError, e:
            self.url_logger.error("HTTPError-"+str(e.code)+"-"+url)
        except urllib2.URLError, e:
            self.url_logger.error("URLError-"+str(e.reason)+"-"+url)
        else:
            pass
        finally:
            return urls

    @classmethod
    def check_domain(cls, url):
        url_hostname = urlparse.urlparse(url).hostname

        # two type of sub domain of m.sohu.com: xxx.m.sohu.com/m.xxx.sohu.com
        if url_hostname.endswith("m.sohu.com"):
            return True
        if url_hostname.startswith("m.") and url_hostname.endswith(".sohu.com"):
            return True

        # other domain that needs to test
        if url_hostname in config.OTHER_INCLUDE_DOMAIN:
            return True
        return False

    def test(self):
        u = ["http://m.baidu.com", "http://m.sohu.com", "http://data.m.sohu.com",
         "http://m.data.sohu.com",
         "http://s1.rr.itc.cn/h5/js/tags/v3/msohu/3.1.37/home.js"]

        for item in u:
            print self.check_domain(item)


if __name__ == "__main__":
    sh = SohuUrlCheck()
    sh.test()
