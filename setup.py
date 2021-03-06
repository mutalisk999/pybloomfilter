#!/usr/bin/env python
# encoding: utf-8


from setuptools import setup

VERSION = '0.0.1'
DESCRIPTION = ""
LONG_DESCRIPTION = """
"""

setup(
    name="pybloomfilter",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    keywords=('bloomfilter', 'bloom filter', 'pybloomfilter'),
    author="mutalisk999",
    author_email="",
    url="https://github.com/mutalisk999/pybloomfilter",
    license="MIT License",
    platforms=['any'],
    test_suite="",
    zip_safe=True,
    install_requires=[
        "bitarray",
        "numpy",
        "redis",
        "pymmh3 @ git+ssh://git@github.com/mutalisk999/pymmh3.git"
    ],
    packages=['pybloomfilter']
)

