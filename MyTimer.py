# !/usr/bin/env python

"""
    NAME    : Open Hadith Dataset
    Author  : Tarek Eldeeb
"""

import time


class Timer(object):
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.time1 = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('%s consumed %.2f seconds' % (self.name, time.time() - self.time1))
