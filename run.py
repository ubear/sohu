#!/usr/bin/env python
#coding=utf8

# 执行初始化脚本
# 开始定时运行
# 本次爬取日志设置,日志文件名要带时间的
# 多线程爬取
# 结束/数据统计/比如运行了多长时间

import initialize

from woker import Scrapy_url


if __name__ == "__main__":
    initialize.start()
    sc = Scrapy_url()
    sc.scrapy()
