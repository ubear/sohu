#!/usr/bin/env python
# -*- coding=utf8 -*-

import urllib2
import urlparse

from bs4 import BeautifulSoup
from lepl.apps.rfc3696 import HttpUrl

from urlcheck import config
from urlcheck.worker import CheckUrl
from urlcheck.worker import Node


class SohuUrlCheck(CheckUrl):

    def __init__(self, FULL=True):
        super(SohuUrlCheck, self).__init__(domain="http://m.sohu.com/")
        self.vaditator = HttpUrl()
        self.full_check = FULL

    def extract_url(self, node):
        nodes = []
        headers = {"User-Agent": 'Mozilla 5.10', "Connection": "close"}
        request = urllib2.Request(node.link.encode('utf-8'), headers=headers)
        try:
            response = urllib2.urlopen(request)
            if node.hypertype == Node.LINK_A:
                page = response.read().decode('utf-8')
                nodes = self.get_urls_from_page(page)
        except urllib2.HTTPError, e:
            self.url_logger.error("HTTPError-"+str(e.code)+"-"+ node.link)
        except urllib2.URLError, e:
            self.url_logger.error("URLError-"+str(e.reason)+"-"+ node.link)
        finally:
            return nodes

    def get_urls_from_page(self, page):
        nodes = []
        soup = BeautifulSoup(page)

        # tag <a>
        for tag in soup.findAll('a', href=True):
            url_item = urlparse.urljoin(self.domain, tag['href'])
            if self.vaditator(url_item) and self.check_domain(url_item):
                nodes.append(Node(url_item, Node.LINK_A)) # repeat little so do not use set()

        # other tag (css/js/image)
        if self.full_check:
            other_urls = []
            img_soup = soup.findAll('img', src=True)
            css_soup = soup.findAll("link", href=True)
            js_soup =  soup.findAll("script", {"type" : "text/javascript"}, src=True)
            for item in (img_soup, js_soup, css_soup):
                for url in item:
                    if item == css_soup:
                        url = urlparse.urljoin(self.domain, url['href'])
                    else:
                        url = urlparse.urljoin(self.domain, url['src'])
                    if self.vaditator(url): # do not need check the domain
                        other_urls.append(url)
            other_urls = set(other_urls) # because of having many repetitive urls
            if other_urls:
                for url in other_urls:
                    nodes.append(Node(url, Node.LINK_OHTER))

        return nodes

    @classmethod
    def check_domain(cls, url):
        url_hostname = urlparse.urlparse(url).hostname

        # three type of sub domain of m.sohu.com: xxx.m.sohu.com/m.xxx.sohu.com/xxx.m.xxx.sohu.com
        if url_hostname.endswith("m.sohu.com"):
            return True
        if url_hostname.startswith("m.") and url_hostname.endswith(".sohu.com"):
            return True
        if ".m." in url_hostname and url_hostname.endswith(".sohu.com"):
            return True

        # other domain that needs to test
        if url_hostname in config.OTHER_INCLUDE_DOMAIN:
            return True

        return False


if __name__ == "__main__":
    sh = SohuUrlCheck()
    sh.process()
