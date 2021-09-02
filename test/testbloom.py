#!/usr/bin/env python
# encoding: utf-8

from pybloomfilter import bloom
import redis


def testBitArrayMMH3Bloom1():
    b = bloom.BitArrayMMH3Bloom(14, 1000)
    for i in range(1000):
        b.put("key-%d" % i)
    for i in range(1000):
        assert b.check("key-%d" % i)


def testBitArrayMMH3Bloom2():
    b = bloom.BitArrayMMH3Bloom(14, 1000)
    for i in range(1000):
        b.put("key-%d" % i)
    for i in range(2000, 3000):
        assert not b.check("key-%d" % i)


def testRedisMMH3Bloom1():
    r = redis.Redis()
    b = bloom.RedisMMH3Bloom(r, "bloom", 14, 1000)
    for i in range(1000):
        b.put("key-%d" % i)
    for i in range(1000):
        assert b.check("key-%d" % i)
    b.destory()
    
    
def testRedisMMH3Bloom2():
    r = redis.Redis()
    b = bloom.RedisMMH3Bloom(r, "bloom", 14, 1000)
    for i in range(1000):
        b.put("key-%d" % i)
    for i in range(2000, 3000):
        assert not b.check("key-%d" % i)
    b.destory()


if __name__ == "__main__":
    testBitArrayMMH3Bloom1()
    testBitArrayMMH3Bloom2()
    testRedisMMH3Bloom1()
    testRedisMMH3Bloom2()

