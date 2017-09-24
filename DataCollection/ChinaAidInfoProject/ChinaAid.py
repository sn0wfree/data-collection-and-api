# -*- coding: utf-8 -*-
import urllib2
import requests
import requests_cache
import sqlite3
import lxml
import pandas as pd
from bs4 import BeautifulSoup

import pandas as pd


class APIrequestData():

    def __init__(self):
        self.param_default = ['donor', 'status', 'intent', 'year', 'crs_sector_name',
                              'flow_class', 'recipient_name', 'recipient_iso2', 'recipient_iso3']

    def requestbyapi(self, param='Default'):
        if param == 'Default':
            self.req = requests.get(
                'http://china.aiddata.org/aggregates/projects?get=%s' % (','.join(self.param_default)))
        else:
            self.req = requests.get(
                'http://china.aiddata.org/aggregates/projects?get=%s' % (','.join(param)))

        self.text = self.req.text
        # print ','.join(param)

    def Store(self):

        self.dataframe = pd.DataFrame(
            eval(self.text.replace('null', '"NULL"')))

        self.dataframe.to_hdf('ChinaAid.h5', 'ChinaAid',
                              complevel=9, complib='blosc')
        #


class sqlitecahche():

    def __init__(self):
        self.cache_conn = self.InitalSqliteConnection(target)

    def InitalSqliteConnection(self, target):
        if target != 0:
            conn = sqlite3.connect(target)
        else:
            conn = sqlite3.connect(":memory:")

        return conn


class hdf5cache():

    def __init__(self, name):
        self = pd.io.pytables.HDFStore('%s-cache.hdf5' % name)

        self.dataset_key = []

    def add(self, *kwargs):
        for key, value in kwargs.items():
            self[key] = value
        self.update_key()

    def update_key(self):
        self.dataset_key = self.cache.keys()


class urllibcache(object):

    def __init__(self, fun):
        self.fun = fun
        self.cache = hdf5cache()

    def __call__(self, *args, **kwargs):
        key = str(args) + str(kwargs)
        try:
            return self.cache[key]
        except KeyError:
            self.cache[key] = rval = self.fun(*args, **kwargs)
            return rval
        except TypeError:  # incase key isn't a valid key - don't cache
            return self.fun(*args, **kwargs)


if __name__ == '__main__':
    requests_cache.install_cache(
        cache_name="ChinaAidProjectInfo", backend="sqlite", expire_date=300000)

    max_project_id = 2521
    urlpath = 'http://china.aiddata.org/projects/'

    for ident in xrange(max_project_id):
        pass
    # req = requests.get(urlpath + str(2000))
    # rr = urllib2.Request(urlpath + str(2000))
    # response = urllib2.urlopen(rr)
    # htmltext = req.text

    target = '<h1 class="project-header page-header">'
    target2 = '<h1 class="'

    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

    headers = {'User-Agent': user_agent}
    # request = urllib2.Request(urlpath + str(1653), headers=headers)
    # response = urllib2.urlopen(request)
    request = requests.get(urlpath + str(1653), headers=headers)

    # response = urllib2.urlopen(request.text)
    # soup = BeautifulSoup(response.read(), "lxml")
    # soup = BeautifulSoup(request.text, "lxml")

    req = lxml.etree.HTML(request.text)
    test = req.xpath("//div[@class='container main']/iframe")
    if len(test) == 1:
        print test[0].keys()
        for node in test:
            srcurl = node.attrib['src']
        srcrequest = requests.get(srcurl)
        srcreq = lxml.etree.HTML(srcrequest.text)
        srctest = srcreq.xpath(
            "//div[@class ='project-page ']//h1[@class ='project-header page-header']")
        srctestsmall = srcreq.xpath(
            "//div[@class ='project-page ']//h1[@class ='project-header page-header']/small[@class]")
        print srctestsmall[0].keys()
        for node in srctestsmall:
            projetc_name = node.text

            #
            # Donor
            # print Donor

            # for tag in soup.find_all(True):
            #    print(tag.name)


'''
    Donor:
        China
    Recipient Countries:
    Liberia(Suacoco, Bong County)
    Commitment Year:
        2008
    Total Amount(USD - 2014):
        $8, 273, 478.56
    CRS Sector:
        Agriculture, Forestry and Fishing
    Flow Type:
        Free - standing technical assistance
    Flow Class:
        ODA - like(Arbitrated)
    Scope:
        Official finance
    Verified:
        Checked
    Intent:
        Development
    Status:
        Completion
    Sector Comment:

    Debt Uncertain:

    Commercial:
        —
    Line of Credit:
        —
    Is Cofinanced:
        —
    Ground Truthed:
        —
    Dates:

    Start(Planned):
        —
    Start(Actual):
        28 April 2009
    End(Planned):
        01 February 2010
    End(Actual):
        01 January 2011
    Loan Details:

    Loan Type:
        —
    Interest Rate:
        —
    Maturity:
        —
    Grace Period:
        —
    Grant Element:
        —
    Transactions:

    $8, 273, 478.56 USD - 2014 ($6, 000, 000.00 USD in 2008)
    1241683516718
    1241683500133
    1
    2
    Previous
    Next
    Upload File
    Share Video
    Downloads
    Description:

    On May 28, 2007 a Chinese delegation arrived in Harper, Maryland County to conduct feasibility studies for the establishment of an agricultural demonstration center. On March 28, 2008, Chinese Ambassador Zhou Yuxiao and Liberian Foreign Minister Boolean signed a cooperation agreement for Chinese assistance on constructing an Agricultural Technology Demonstration Center. In April 2009 construction began of the China Agricultural Technology Demonstration center at the Central Agricultural Research Institute(CARI) in Suacoco, Bong County. The Center is expected to be complete in 10 months and will cost US$6 million. It will be constructed on a 2360 square meter area. According to the Chinese Embassy, the Center will cover an area of 2, 411 square meters. Groundbreaking ceremony for the center was held on April 28, 2009. An official handover ceremony was held on July 23, 2010. Yuan Longping High - tech Agriculture Co., Ltd was the main implementing organization and the agricultural demonstration center specialized in hybrid rice.
    Capacity:
        2, 411 square meters, with a laboratory, technical training and sustainable agricultural development focuses
'''
