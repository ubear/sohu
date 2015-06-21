#!/usr/bin/env python
# coding=utf8

import os

from apscheduler.schedulers.blocking import BlockingScheduler

from urlcheck import config
from sohu import SohuUrlCheck


def job():
    sohu = SohuUrlCheck()
    sohu.process()


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_executor('processpool')
    scheduler.add_job(job, 'interval', seconds=config.INTERVAL_EXC)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
