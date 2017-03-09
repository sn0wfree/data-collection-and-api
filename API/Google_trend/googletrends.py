# -*- coding:utf-8 -*-

#-------------------
__version__ = "0.8"
__author__ = "sn0wfree"
'''
This tool is for connecting the Google Trends Service
'''
#-------------------
import os
import requests_cache
import gc
import matplotlib.pyplot as plt
import pytrends
import pandas as pd


def googleTrends():
    # set up a dic
    result = {}
    #google_username = raw_input('Please type in your Google account username: ')

    #google_password = raw_input('Please type in your Google account password: ')
    google_account = 'default'
    if google_account == 'default':
        google_username = 'snowpythontest@gmail.com'
        google_password = '19920815'
    else:
        pass
    #search_list = raw_input('Please type in your search list: ')
    search_list = ''

    search_list_default = ['pizza', 'bagel']

    pytrend = pytrends.TrendReq(
        google_username, google_password, hl='en-US', tz=360, custom_useragent=None)
    if search_list == '':
        search_list = search_list_default
    pytrend.build_payload(kw_list=search_list)

    # Interest Over Time
    interest_over_time_df = pytrend.interest_over_time()
    result['interest over time'] = interest_over_time_df

    # Interest by Region
    interest_by_region_df = pytrend.interest_by_region()
    result['interest by region'] = interest_by_region_df
    # print interest_by_region_df

    # Related Queries, returns a dictionary of dataframes
    related_queries_dict = pytrend.related_queries()
    result['related queries'] = related_queries_dict
    # print related_queries_dict

    # Get Google Hot Trends data
    #trending_searches_df = pytrend.trending_searches()

    # Get Google Top Charts
    #top_charts_df = pytrend.top_charts(cid='actors', date=201611)

    # Get Google Keyword Suggestions
    suggestions_dict = {}
    for l in search_list:

        suggestions_dict[l] = pytrend.suggestions(keyword=l)
    result['suggestions'] = suggestions_dict
    return result
if __name__ == '__main__':
    requests_cache.install_cache(
        cache_name="googletrends_request_cache", backend="sqlite", expire_date=1800)
    result = googleTrends()
    result['interest by region'].boxplot()
