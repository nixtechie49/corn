# encoding:utf-8

import logging as log
import sched
import threading
import time

import cache

__author__ = 'rock'

_1_min = 60
_1_hour = 60 * _1_min
_1_day = _1_hour * 24

s = sched.scheduler(time.time, time.sleep)


def clean_cache():
    s.enter(_1_min, 0, clean_cache)
    temp = []
    for k in cache.iterator:
        now = int(round(time.time() * 1000))
        log.debug('now[%d] iter is : %s', now, k)
        k_time = int(k.split('_')[-1])
        if (now - k_time) > (_1_hour * 1000):
            temp.append(k)
    if len(temp) > 0:
        log.info('clean iterator cache.')
    for k in temp:
        log.debug('del iterator cache %s', k)
        del cache.iterator[k]
    del temp


def clean_worker():
    s.enter(_1_min, 0, clean_cache)
    s.run()


class WorkerThread(threading.Thread):
    def __init__(self, name=None, func=None):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.daemon = True

    def run(self):
        self.func()


t = WorkerThread(name='Worker-Thread', func=clean_worker)


def start():
    t.start()


def stop():
    for e in s.queue:
        s.cancel(e)
