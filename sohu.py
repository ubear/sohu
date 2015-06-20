#!/usr/bin/env python
# coding=utf8

import urllib2
import urlparse

from bs4 import BeautifulSoup
from lepl.apps.rfc3696 import HttpUrl

from urlcheck import worker


class SohuUrlCheck(worker.CheckUrl):

    def __init__(self):
        super(SohuUrlCheck, self).__init__(domain="http://m.sohu.com/")
        self.vaditator = HttpUrl()

    def __validate_url(self, url):
        url = url.strip()
        return self.vaditator(url)

    def __check_domain(self, url):
        url_hostname = urlparse.urlparse(url).hostname
        domain_hostname = urlparse.urlparse(self.domain).hostname
        if url_hostname == domain_hostname:
            return True
        return False

    def extract_url(self, url):
        print url
        if not self.__validate_url(url):
            return []
        urls = []
        headers = {"User-Agent": 'Mozilla 5.10', "Connection": "close"}
        request = urllib2.Request(url.encode('utf-8'), headers=headers)
        try:
            response = urllib2.urlopen(request)
            if super(SohuUrlCheck, self).url_filter(url):
                page = response.read().decode('utf-8')
                soup = BeautifulSoup(page)
                for tag in soup.findAll('a', href=True):
                    url_item = urlparse.urljoin(self.domain, tag['href'])
                    if self.__check_domain(url_item):
                        urls.append(url_item)
            else:
                pass
        except urllib2.HTTPError, e:
            self.url_logger.error("HTTPError-"+str(e.code)+"-"+url)
        except urllib2.URLError, e:
            self.url_logger.error("URLError-"+str(e.reason)+"-"+url)
        else:
            pass
        finally:
            return urls