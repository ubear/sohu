#!/usr/bin/env python
#coding=utf8
try:
    import sys
    import time
    import threading
    import Queue
    import urlparse
    import logging
    import config
    import urllib2
    import redis
    from bs4 import BeautifulSoup
except ImportError:
    print >> sys.stderr, """\
There was a problem importing one of the Python modules required to run yum.
The error leading to this problem was:
%s
Please install a package which provides this module, or
verify that the module is installed correctly.
It's possible that the above module doesn't match the current version of Python,
which is:
%s
""" % (sys.exc_info(), sys.version)
    sys.exit(1)

### global variables ###
task_queue = Queue.Queue()
lock = threading.Lock()

class Scrapy_url(object):
    global task_queue

    # configure/logger
    def __init__(self, domain="http://m.sohu.com/"):
        self.domain = domain



    # check queue and put the initial url
    # spawn a pool of threads
    def scrapy(self):
        task_queue.put(self.domain)
        redis.Redis(connection_pool=config.REDISPOOL).set(self.domain, 1)#防止重复
        for i in range(config.THREAD_NUMBER):
            et = Extract_threading(self.process, str(i))
            et.setDaemon(True)
            et.start()
        task_queue.join()

    # extract data from html
    def process(self, url):
        urls = list()
        headers = {"User-Agent":'Mozilla 5.10', "Connection":"close"}
        request = urllib2.Request(url, headers=headers)
        try:
            response = urllib2.urlopen(request)
            status = response.getcode()
            if status != 200:
                print "error:Not200"+url+str(status)
            page = response.read().decode(response.headers['content-type'].split('charset=')[-1])
            soup = BeautifulSoup(page)
            for tag in soup.findAll('a', href=True):
                tag['href'] = urlparse.urljoin(url, tag['href'])
                urls.append(tag['href'])
            return urls
        except:
            print "errror:"+url
            return None



class Extract_threading(threading.Thread):
    def __init__(self, task, name):
        threading.Thread.__init__(self)
        self.do_task = task
        self.redis = redis.Redis(connection_pool=config.REDISPOOL)
        print "Threading---"+name+ " is running..."

    def run(self):
        global task_queue
        while True:
            if not task_queue.empty():
                url = task_queue.get()
                print url
                urls = self.do_task(url)
                if urls:
                    for item in urls[0:5]:
                        if not self.redis.exists(item):
                            task_queue.put(item)
                            self.redis.set(url, 1)
                        else:
                            pass
                task_queue.task_done()
            else:
                print "is empety"
                time.sleep(10)

if __name__=="__main__":
    sc = Scrapy_url()
    sc.scrapy()