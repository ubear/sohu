#!/usr/bin/env python
# coding=utf8

import os
import time
import threading
import Queue
import logging
import urllib2
import urlparse
from datetime import datetime

# web scrapy
from bs4 import BeautifulSoup

# configuration
import config


class CheckUrl(object):

    have_checked_url_num = 0

    # configuration
    def __init__(self, domain=None):
        self.domain = domain if domain else config.SITE
        self.url_queue = Queue.Queue()
        self.url_queue.put(self.domain)
        self.url_dict = {}
        self.lock = threading.Lock()
        self.url_logger = self.__set_logger()

    # configuration for logger
    def __set_logger(self):
        log_dir_name = urlparse.urlparse(self.domain).netloc
        full_file_path = os.path.join(config.LOG_DIR, log_dir_name)
        if not os.path.exists(full_file_path):
            os.makedirs(full_file_path)
        filename = datetime.now().strftime(config.LOG_FILENAME_FMT)+'.log'
        logger = logging.getLogger(log_dir_name)
        logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter(config.LOG_CONTENT_FMT)
        file_hander = logging.FileHandler(os.path.join(full_file_path, filename))
        file_hander.setLevel(logging.DEBUG)
        file_hander.setFormatter(fmt)
        logger.addHandler(file_hander)
        return logger

    # spawn a pool of threads
    def process(self):
        threads = []
        st_time = time.time()
        for i in range(config.THREAD_NUMBER):
            mt = MetaThreading(self.extract_url, self.url_queue,
                               self.url_dict, self.lock, str(i))
            mt.setDaemon(True)
            mt.start()
            threads.append(mt)

        for thread in threads:
            thread.join()

        self.url_logger.info("Total Time:%s" % (time.time() - st_time))

    def url_include(self, url):
        if urlparse.urlparse(url).netloc in config.INCLUDE_DOMAIN:
            return True
        return False

    # extract url from page
    # return list of url
    def extract_url(self, url):
        urls = []
        headers = {"User-Agent": 'Mozilla 5.10', "Connection": "close"}
        request = urllib2.Request(url.encode('utf-8'), headers=headers)
        try:
            response = urllib2.urlopen(request)
            if self.url_include(url):
                page = response.read().decode('utf-8')
                soup = BeautifulSoup(page)
                for tag in soup.findAll('a', href=True):
                    url_item = urlparse.urljoin(self.domain, tag['href'])
                    urls.append(url_item)
            else:
                pass
        except urllib2.HTTPError, e:
            self.url_logger.error("HTTPError-"+str(e.code)+"-"+url)
        except urllib2.URLError, e:
            self.url_logger.error("URLError-"+str(e.reason)+"-"+url)
        else:
            # import traceback
            # self.url_logger.error(url+"---"+traceback.format_exc())
            pass
        finally:
            return urls


class MetaThreading(threading.Thread):
    def __init__(self, task, u_queue, u_dict, u_lock, name):
        threading.Thread.__init__(self)
        self.do_task = task
        self.task_queue = u_queue
        self.url_dict = u_dict
        self.lock = u_lock
        self.name = name

    def run(self):
        while CheckUrl.have_checked_url_num < config.URL_TOTAL_NUM:
            if not self.task_queue.empty():
                url = self.task_queue.get()
                print url
                if url in self.url_dict:
                    self.task_queue.task_done()
                    continue
                else:
                    with self.lock:
                        if url in self.url_dict:
                            self.task_queue.task_done()
                            continue
                        else:
                            self.url_dict['url'] = 1
                            CheckUrl.have_checked_url_num += 1
                urls = self.do_task(url)
                if urls:
                    for item in urls:
                        self.task_queue.put(item)
                self.task_queue.task_done()
            else:
                time.sleep(1)

if __name__ == "__main__":
    cu = CheckUrl()
    cu.process()