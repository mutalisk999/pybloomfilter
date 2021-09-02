#!/usr/bin/env python
# encoding: utf-8


import math
from numpy import log as ln


class BloomInterface(object):
    def __init__(self, hashCount, elemCount):
        self.hashCount = hashCount
        self.elemCount = elemCount
        self.bitArraySize = math.ceil(self.hashCount * self.elemCount / ln(2))
    
    def __del__(self):
        pass
    
    def get_locations(self, *arg):
        pass
    
    def put(self, *arg):
        pass
    
    def check(self, *arg):
        pass

