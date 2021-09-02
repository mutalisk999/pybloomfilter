#!/usr/bin/env python
# encoding: utf-8


from pybloomfilter import bloom_interface, hash
from multiprocessing import Lock
import bitarray


class BitArrayMMH3Bloom(bloom_interface.BloomInterface):
    def __init__(self, hashCount, elemCount):
        super().__init__(hashCount, elemCount)
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


class RedisMMH3Bloom(bloom_interface.BloomInterface):
    def __init__(self, redisStore, redisKey, hashCount, elemCount):
        super().__init__(hashCount, elemCount)
        self.hashFunc = hash.MMH3Hash.hash
        self.redisStore = redisStore
        self.redisKey = redisKey

    def __del__(self):
        super().__del__()

    def get_locations(self, data):
        locations = []
        for i in range(self.hashCount):
            v = self.hashFunc(key=data, seed=0x1000 + i)
            locations.append(v % self.bitArraySize)
        return locations

    def put(self, data):
        locations = self.get_locations(data)
        setScript = '''
            for _, offset in ipairs(ARGV) do
                redis.call("setbit", KEYS[1], offset, 1)
            end
        '''
        multiply = self.redisStore.register_script(setScript)
        multiply(keys=[self.redisKey], args=locations)

    def check(self, data):
        locations = self.get_locations(data)
        checkScript = '''
            for _, offset in ipairs(ARGV) do
                if tonumber(redis.call("getbit", KEYS[1], offset)) == 0 then
                    return false
                end
            end
            return true
        '''
        multiply = self.redisStore.register_script(checkScript)
        return multiply(keys=[self.redisKey], args=locations)
    
    def destory(self):
        self.redisStore.delete(self.redisKey)
