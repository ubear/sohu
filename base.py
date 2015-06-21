#!/usr/bin/env python
# -*- coding=utf8 -*-

import urllib2
import urlparse

from bs4 import BeautifulSoup
from lepl.apps.rfc3696 import HttpUrl

from urlcheck.worker import CheckUrl
from urlcheck.datastructure import Node


class BaseUrlCheck(CheckUrl):
    def __init__(self, domain):
        super(BaseUrlCheck, self).__init__(domain)
        self.vaditator = HttpUrl()

    def extract_url(self, node):
        nodes = []
        headers = {"User-Agent": 'Mozilla 5.10', "Connection": "close"}
        request = urllib2.Request(node.link.encode('utf-8'), headers=headers)
        try:
            response = urllib2.urlopen(request)
            page = response.read().decode('utf-8')
            soup = BeautifulSoup(page)
            for tag in soup.findAll('a', href=True):
                url_item = urlparse.urljoin(self.domain, tag['href'])
                if self.vaditator(url_item):
                    nodes.append(Node(url_item, Node.LINK_A))
        except urllib2.HTTPError, e:
            self.url_logger.error("HTTPError-"+str(e.code)+"-"+ node.link)
        except urllib2.URLError, e:
            self.url_logger.error("URLError-"+str(e.reason)+"-"+node.link)
        else:
            pass
        finally:
            return nodes