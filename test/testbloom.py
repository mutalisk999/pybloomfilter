#!/usr/bin/env python
# encoding: utf-8

from pybloomfilter import bloom


def testBitArrayBloom1():
    b = bloom.BitArrayBloom(14, 1000)
    for i in range(1000):
        b.put("key-%d" % i)
    for i in range(1000):
        assert b.check("key-%d" % i)


def testBitArrayBloom2():
    b = bloom.BitArrayBloom(14, 1000)
    for i in range(1000):
        b.put("key-%d" % i)
    for i in range(2000, 3000):
        assert not b.check("key-%d" % i)
        

if __name__ == "__main__":
    testBitArrayBloom1()
    testBitArrayBloom2()
