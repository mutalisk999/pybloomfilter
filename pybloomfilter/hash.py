#!/usr/bin/env python
# encoding: utf-8

from pybloomfilter import hash_interface
import pymmh3


class MMH3Hash(hash_interface.HashInterface):
    @staticmethod
    def hash(key, seed):
        return pymmh3.hash(key=key, seed=seed)
    

