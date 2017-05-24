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

# import matplotlib.pyplot as plt
import pytrends
import pandas as pd


def read_a_file(file):
    with open(file, 'r') as f:
        f_collected = f.readlines()
    return f_collected


class ImportInfo():

    def __init__(self):
        self.accountinfo = {'google_username': '', 'google_password': ''}
        self.list = []
        self.locals_file_path = os.path.split(os.path.realpath(__file__))[0]
        self.scan_files = os.listdir(self.locals_file_path)

    def ImportListInfo(self,  GUI=False):

        if self.ImportListInfobyFile() == 0:

            # if self.ImportListInfobyOtherFile(self) == 0:
            self.list = self.ImportListInfobyTyple(self)
            # else:
            #    self.list = self.ImportListInfobyOtherFile(self)

        else:
            print 'Detected the local preference file (LIST INFORMATION)'
            self.list = self.ImportListInfobyFile()
        return self.list

    def ImportListInfobyOtherFile(self, GUI_input=None, GUI=False):
        if GUI == False:
            other = raw_input('please type the path of the keywords list')
        else:
            other = GUI_input
        file_type = other.split('.')[-1]
        if file_type == 'txt':
            keywords = []
            fi = read_a_file(other)
            for f in fi:
                keywords.extend(f.split()[0].split(','))
        elif file_type == 'xlsx' or file_type == 'xls':
            outoutOFother = pd.read_excel(other)
            keywords = outoutOFother['tinker']
            ###
        elif file_type == 'csv':
            fi = pd.read_csv(other)
            keywords = fi['tinker']
        elif file_type == 'db':
            import sqlite3
            conn = sqlite3.connect(other)
            table_name = pd.read_sql_query(
                "SELECT name FROM sqlite_master WHERE type='table'ORDER BY name;", conn)
            keywords = []
            for tn in table_name.to_dict()['name'].values():
                tab = pd.read_sql_query("SELECT tinker FROM %s" % tn, conn)
                keywords.extend(tab.to_dict['tinker'].values())

        elif file_type == 'json':
            pass

        return keywords

    def ImportListInfobyFile(self, GUI=False):
        keywords = []
        if 'keywords.txt' in self.scan_files:
            fi = read_a_file('keywords.txt')
            for f in fi:
                keywords.extend(f.split()[0].split(','))
        elif 'keywords.csv' in self.scan_files:
            fi = pd.read_csv('keywords.csv')
            keywords = fi['tinker']
        else:
            keywords = 0

        return keywords

    def ImportListInfobyTyple(self, GUI=False):
        self.list = raw_input(
            "please type the tinker of targeted stocks, use comma separate:")
        self.list = self.list.split(",")
        return self.list

    def ImportAccountInfo(self, GUI=False):

        if self.ImportAccountInfobyFile() == 0:
            self.accountinfo = self.ImportAccountInfobyType()
        else:
            print 'Detected the local preference file (GOOGLE ACCOUNT)'
            self.accountinfo = self.ImportAccountInfobyFile()
        return self.accountinfo

    def ImportAccountInfobyFile(self, GUI=False):

        if 'account_info.txt' in self.scan_files:
            account_info = [f.split()
                            for f in read_a_file('account_info.txt')]
            for info in account_info:
                if 'google_username' in info:
                    self.accountinfo['google_username'] = info[-1]

                elif 'google_password' in info:
                    self.accountinfo['google_password'] = info[-1]
            return self.accountinfo

        else:
            return 0

            # onlyfiles = [f for f in os.listdir(locals_file_path) if
            # isfile(join(mypath, f))]
    def ImportAccountInfobyType(self, GUI=False):

        while '@' not in self.accountinfo['google_username']:
            print 'Invald Google Account, please use correct Google Account'
            google_username = raw_input(
                'Please type in your Google Account Username: ')
            google_password = raw_input(
                'Please type in your Google Account Password: ')
            self.accountinfo['google_username'] = google_username
            self.accountinfo['google_password'] = google_password
        return self.accountinfo


def googleTrends():
    # set up a dic
    result = {}
    a = ImportInfo()
    account = a.ImportAccountInfo()

    google_username = account['google_username']
    google_password = account['google_password']
    search_list = a.ImportListInfo()

    pytrend = pytrends.TrendReq(
        google_username, google_password, hl='en-US', tz=360, custom_useragent=None)

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
    # trending_searches_df = pytrend.trending_searches()

    # Get Google Top Charts
    # top_charts_df = pytrend.top_charts(cid='actors', date=201611)

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
    print result['interest over time'], type(result['interest over time'])
    result['interest over time'].to_csv('output.csv')
    # print a.ImportAccountInfo(), a.ImportListInfobyFile()

    # print result['interest by region']
