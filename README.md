# pybloomfilter

### about pybloomfilter
pybloomfilter is a python bloom filter implementation using murmur3 hash algorithm.

### how to use

* using bit array 

```
    import pybloomfilter
    b = pybloomfilter.BitArrayMMH3Bloom(14, 64)
    b.put("aaa")
    print(b.check("aaa"))
    print(b.check("bbb"))
```


* using redis

```
    import pybloomfilter, redis
    r = redis.Redis(host="127.0.0.1", port=6379)
    b = pybloomfilter.RedisMMH3Bloom(r, "bloom", 14, 64)
    b.put("aaa")
    print(b.check("aaa"))
    print(b.check("bbb"))
```



