# -*- coding: utf-8 -*-
import urllib2
import requests
import requests_cache
import sqlite3
import lxml
import collections
import pandas as pd
from bs4 import BeautifulSoup
try:
    from collections import ChainMap
except ImportError:
    from chainmap import ChainMap
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


class DataContainer():

    def __init__(self):

        self.data = ChainMap()

    def add(self, **kwargs):
        self.data.new_child(kwargs)

        self.updateinfo()

    def remove(self, removed_key):
        del self.data[removed_key]

    def updateinfo(self):
        pass


class Inhtml():

    def __init__(self, src, header):
        self.requesttext = requests.get(src, headers=header).text
        self.data = {}

    def path(self, pathstr, variablename, addi=True):
        x = lxml.etree.HTML(self.requesttext).xpath(pathstr)
        if len(x) == 1:
            temp = (variablename, x[0].text)
            if addi:
                self.add(temp)
            return temp

        elif len(x) > 1:
            temp = [(variablename + 'of' + str(x.index(value)), value.text)
                    for value in x]
            if addi:
                self.add(temp)
            return temp

        else:
            if addi:
                self.add((variablename, 'NULL'))
            return (variablename, 'NULL')

    def add(self, d):
        if isinstance(d, list):
            self.data.update(dict(d))
        if isinstance(d, tuple) or isinstance(d, set):
            self.data.update(dict([d]))

        elif isinstance(d, str):
            raise ValueError, 'NO str'
        elif isinstance(d, dict):
            self.data.update(d)

        else:
            raise TypeError, 'Unknown type'

    def multipath(self, dict_value, **kwargs):

        new = [self.path(value, key) for key, value in dict_value.items(
        )] + [self.path(value, key) for key, value in kwargs.items()]

        self.add(dict(new))
        return new

    def detectdiff(self, target):
        for key, value in dict(target).items():
            pass


def list2dict(ls):

    if ':' in ls[0]:
        key = ls[0][:-1]

        value = ls[1:]
    elif ls != []:
        key = ls[0]
        value = ls[1:]
    else:
        key = 'NULL'
        value = 'NULL'
    return {key: value}


def detectchild(t):

    if len(t.getchildren()) > 1:
        # print t.xpath('./*[starts-with(name(),'ul')]')
        return [w.strip() for g in t.getchildren() for w in g.xpath('.//text()') if w.strip() != '']

    elif len(t.getchildren()) == 1:

        return [v.strip() for v in t.xpath(".//text()") if v.strip() != '']
    else:
        return []
if __name__ == '__main__':
    requests_cache.install_cache(
        cache_name="ChinaAidProjectInfo", backend="sqlite", expire_date=300000)
    Data = DataContainer()

    max_project_id = 2521
    urlpath = 'http://china.aiddata.org/projects/'

    for ident in xrange(max_project_id):
        pass

    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

    headers = {'User-Agent': user_agent}
    # request = urllib2.Request(urlpath + str(1653), headers=headers)
    # response = urllib2.urlopen(request)
    request = requests.get(urlpath + str(1653), headers=headers)

    # response = urllib2.urlopen(request.text)
    # soup = BeautifulSoup(response.read(), "lxml")
    # soup = BeautifulSoup(request.text, "lxml")

    test = lxml.etree.HTML(request.text).xpath(
        "//div[@class='container main']/iframe")
    if len(test) != 1:
        raise ValueError, 'iframe contain multi-information'
    elif 'src' in test[0].keys():
        srcframe = Inhtml(test[0].attrib['src'], headers)

        dict2 = {
            'project_name': "//div[@class ='container main']//div[@class ='project-page ']//h1[@class ='project-header page-header']",
            'project_brief': "//div[@class ='container main']//div[@class ='project-page ']//h1[@class ='project-header page-header']/small[@class]"}

        print list2dict(srcframe.multipath(dict2))

        pathstr = "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Donor']/../*"

        test = lxml.etree.HTML(srcframe.requesttext).xpath(pathstr)

        # print [t.getchildren()[0].text for t in test]
        rr = ChainMap()

        chain = ChainMap(*[list2dict(detectchild(t)) for t in test])
        print chain

        pathstr2 = "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Intent']/../*"
        test2 = lxml.etree.HTML(srcframe.requesttext).xpath(pathstr2)
        print [list2dict(detectchild(t2)) for t2 in test2]

        total = lxml.etree.HTML(srcframe.requesttext).xpath(
            "//div[@class='container main']//div[@class='project-page ']//li//text()")
        totalinfo = [ws.strip()
                     for ws in total if ws.strip() != '']
        # print 'flaggable_type'

    else:
        pass
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
