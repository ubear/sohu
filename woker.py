#!/usr/bin/env python
#coding=utf8

import datetime
import httplib
import logging
import Queue
import time
import threading
import urllib2
import urlparse
from bs4 import BeautifulSoup

import redis

import config


### global variables ###
task_queue = Queue.Queue()
lock = threading.Lock()
tested_url_num = 0


class Scrapy_url(object):
    global task_queue
    global test_url_num

    # configure/logger
    def __init__(self, domain=None):
        if domain:
            self.domain = domain
        else:
            self.domain = config.SITE
        prefix = urlparse.urlparse(self.domain).netloc
        filename = datetime.datetime.now().strftime(prefix+":D_%Y-%m-%d_T%H:%M")+'.txt'
        self.slogger = logging.getLogger(prefix)
        logging.basicConfig(level=logging.DEBUG,
                            format=config.FILE_FMT,
                            filename="log/"+filename, #os.path.join(config.LOG_DIR,filename),
                            filemode='w')
        task_queue.put(self.domain)
        redis.Redis(connection_pool=config.REDIS_POOL).set(self.domain, 1)#防止重复

    # check queue and put the initial url
    # spawn a pool of threads
    def scrapy(self):
        threads = []
        st_time = time.time()
        for i in range(config.THREAD_NUMBER):
            et = Extract_threading(self.process, str(i))
            et.setDaemon(True)
            et.start()
            threads.append(et)

        for thread in threads:
            thread.join()

        #task_queue.join()
        test_url_num = 0
        task_queue.queue.clear()

        print "total time:%s" % (time.time() - st_time)

    # extract data from html
    def process(self, url):
        urls = []
        headers = {"User-Agent":'Mozilla 5.10', "Connection":"close"}
        request = urllib2.Request(url.encode('utf-8'), headers=headers)
        try:
            response = urllib2.urlopen(request)
            if self.filter_url(url):
                page = response.read().decode('utf-8')
                soup = BeautifulSoup(page)
                for tag in soup.findAll('a', href=True):
                    url_item = urlparse.urljoin(self.domain, tag['href'])
                    urls.append(url_item)
            else:
                pass
        except urllib2.HTTPError, e:
            self.slogger.error("HTTPError-"+str(e.code)+"---"+url)
        except urllib2.URLError, e:
            self.slogger.error("URLError-"+str(e.code)+"---"+url)
        except httplib.HTTPException, e:
            pass
        except UnicodeDecodeError,e:
            pass
        except UnicodeEncodeError, e:
            self.slogger.warning("UnicodeEncodeError-"+url+"---"+e.message)
        except Exception:
            import traceback
            self.slogger.error(url+"---"+traceback.format_exc())
        finally:
            return urls

    def filter_url(self, url):
        if urlparse.urlparse(url).netloc in config.INCLUDE_DOMAIN:
            return True
        else:
            return False


class Extract_threading(threading.Thread):
    def __init__(self, task, name):
        threading.Thread.__init__(self)
        self.do_task = task
        self.redis = redis.Redis(connection_pool=config.REDIS_POOL)
        self.name = name
        print "Threading---"+self.name+ " is running..."

    def run(self):
        global task_queue
        global lock
        global tested_url_num
        while tested_url_num < config.URL_TOTAL_NUM:
            if not task_queue.empty():
                url = task_queue.get()
                urls = self.do_task(url)
                if urls:
                    for item in urls:
                        if not self.redis.exists(item):
                            task_queue.put(item)
                            self.redis.set(url, 1)
                        else:
                            pass
                task_queue.task_done()
                with lock:
                    tested_url_num += 1

                if task_queue.qsize() >= config.QUEUE_CAPACITY:
                    print "Threading---"+self.name+ " is closing..."
                    break
            else:
                time.sleep(1)


if __name__ == "__main__":
    sc = Scrapy_url()
    sc.scrapy()
