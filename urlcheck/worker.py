#!/usr/bin/env python
# -*- coding=utf8 -*-

import os
import time
import threading
import Queue
import logging
import urlparse
from datetime import datetime

import config
from datastructure import Node

# Job's flag
job_flag = {}


class CheckUrl(object):

    # configuration
    def __init__(self, domain="http://m.sohu.com/"):
        self.domain = domain
        self.url_queue = Queue.Queue()
        self.url_queue.put(Node(self.domain, Node.LINK_A))
        self.lock = threading.Lock()
        self.hostname = self.get_hostname(self.domain) 
        self.filename = datetime.now().strftime(config.LOG_FILENAME_FMT)
        self.url_logger = self.__set_logger()
        self.job_flag = self.__set_job_flag()

    def get_hostname(self, url):
        return urlparse.urlparse(url).hostname

    # set the class to JobFlag
    def __set_job_flag(self):
        flag = self.hostname + self.filename
        job_flag[flag] = 0
        return flag

    # configuration for logger
    def __set_logger(self):
        log_dir_name = self.hostname
        full_file_path = os.path.join(config.LOG_DIR, log_dir_name)
        if not os.path.exists(full_file_path):
            os.makedirs(full_file_path)
        filename = self.filename + '.log'
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
                               self.lock, self.job_flag, str(i))
            mt.setDaemon(True)
            mt.start()
            threads.append(mt)

        for thread in threads:
            thread.join()
        self.url_logger.info("Total Time:%s" % (time.time() - st_time))

    # extract url from page return list of url
    def extract_url(self, url):
        pass


class MetaThreading(threading.Thread):
    def __init__(self, task, u_queue, u_lock, u_flag, name):
        threading.Thread.__init__(self)
        self.do_task = task
        self.task_queue = u_queue
        self.url_dict = {}
        self.lock = u_lock
        self.flag = u_flag
        self.name = name

    def run(self):
        # print "Threading-"+self.name+" is running..."
        while job_flag[self.flag] <= config.URL_TOTAL_NUM:
            if not self.task_queue.empty():
                node = self.task_queue.get()
                if node.link not in self.url_dict:
                    with self.lock:
                        if node.link not in self.url_dict:  # check multi threads
                            self.url_dict[node.link] = 1
                            job_flag[self.flag] += 1
                        else:
                            self.task_queue.task_done()
                            continue
                else:
                    self.task_queue.task_done()
                    continue
                nodes = self.do_task(node)
                if nodes:
                    for item in nodes:
                        self.task_queue.put(item)
                self.task_queue.task_done()
            else:
                time.sleep(5)
        # print "Threading-"+self.name+" is closing..."


if __name__ == "__main__":
    cu = CheckUrl()
    cu.process()
