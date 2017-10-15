# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
"""
This code is for personal use.

"""
# Copyright by Lin Lu 2017
# version control


__author__ = 'sn0wfree'
__version__ = '0.02'


# -------------------------------------------------------------------------
import requests
import requests_cache

if __name__ == '__main__':
    requests_cache.install_cache(
        cache_name="Leader", backend="sqlite", expire_date=300)
