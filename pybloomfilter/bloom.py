#!/usr/bin/env python
# encoding: utf-8


from pybloomfilter import bloom_interface, hash
from multiprocessing import Lock
import bitarray
import math
from numpy import log as ln


class BitArrayBloom(bloom_interface.BloomInterface):
    def __init__(self, hashCount, elemCount):
        super().__init__()
        self.hashCount = hashCount
        self.elemCount = elemCount
        self.bitArraySize = math.ceil(self.hashCount * self.elemCount / ln(2))
        self.bitArray = bitarray.bitarray(self.bitArraySize)
        self.hashFunc = hash.MMH3Hash.hash
        self.bitArray.setall(0x0)
        self.mutex = Lock()
        
    def __del__(self):
        super().__del__()
        self.bitArray.clear()
        self.bitArray = None
        self.mutex = None
    
    def get_locations(self, data):
        locations = []
        for i in range(self.hashCount):
            v = self.hashFunc(key=data, seed=0x1000 + i)
            locations.append(v % self.bitArraySize)
        return locations
    
    def put(self, data):
        locations = self.get_locations(data)
        self.mutex.acquire()
        for l in locations:
            self.bitArray[l] = 0x1
        self.mutex.release()
    
    def check(self, data):
        res = 0x1
        locations = self.get_locations(data)
        self.mutex.acquire()
        for l in locations:
            res = res & self.bitArray[l]
            if res == 0x0:
                self.mutex.release()
                return False
        self.mutex.release()
        return True
