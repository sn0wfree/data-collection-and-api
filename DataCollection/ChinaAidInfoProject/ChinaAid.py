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
        self.data = ChainMap()

    def xpathparser(self, pathstr, variablename, addi=True):
        x = lxml.etree.HTML(self.requesttext).xpath(pathstr)
        if len(x) == 1:
            temp = (variablename, x[0].text.strip())
            if addi:

                self.add({temp[0]: temp[1]})
            return temp

        elif len(x) > 1:
            temp = {variablename + 'of' + str(x.index(value)): value.text.strip()
                    for value in x}
            if addi:
                self.add(temp)
            return temp

        else:
            print len(x)
            if addi:
                self.add({variablename: 'NULL'})
            return (variablename, 'NULL')

    def add(self, d):
        if isinstance(d, type(ChainMap())):
            self.data = self.data.new_child(d)

        elif isinstance(d, dict):
            self.data = self.data.new_child(d)
        elif isinstance(d, list):
            if isinstance(d[0], dict):
                self.data = self.data.new_child(d)
            else:
                raise TypeError, 'Unknown type'
        else:
            raise ValueError, 'Unknown value'

    def multixpathparser(self, *args, **kwargs):

        t1 = [self.xpathparser(di[key], key, addi=False)
              for di in args for key in di.keys()]
        t2 = [self.xpathparser(value, key, addi=False)
              for key, value in kwargs.items()]
        self.add(dict(t1))
        self.add(dict(t2))

    def detectchild(self, t):

        if len(t.getchildren()) > 1:
            # print t.xpath('./*[starts-with(name(),'ul')]')
            return [w.strip() for g in t.getchildren() for w in g.xpath('.//text()') if w.strip() != '']

        elif len(t.getchildren()) == 1:

            return [v.strip() for v in t.xpath(".//text()") if v.strip() != '']
        else:
            return []

    def list2dict(self, ls):

        if ':' in ls[0]:
            key = ls[0][:-1]

            value = ls[1:]
        elif ls != []:
            key = ls[0]
            value = ls[1:]
        else:
            key = 'NULL'
            value = 'NULL'
        return (key, value)

    def parser(self, xpth):
        #xpth = "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Intent']/../*"
        test2 = lxml.etree.HTML(self.requesttext).xpath(xpth)

        chain2 = dict([self.list2dict(self.detectchild(t)) for t in test2])
        self.add(chain2)

    def parserwithoutadd(self, xpth):
        test2 = lxml.etree.HTML(self.requesttext).xpath(xpth)

        chain2 = dict([self.list2dict(self.detectchild(t)) for t in test2])
        return chain2


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
    request = requests.get(urlpath + str(1654), headers=headers)

    # response = urllib2.urlopen(request.text)
    # soup = BeautifulSoup(response.read(), "lxml")
    # soup = BeautifulSoup(request.text, "lxml")

    test = lxml.etree.HTML(request.text).xpath(
        "//div[@class='container main']/iframe")
    if len(test) != 1:
        raise ValueError, 'iframe contain multi-information'
    elif 'src' in test[0].keys():
        srcframe = Inhtml(test[0].attrib['src'], headers)
        print 'project_name'

        dict2 = {
            'project_name': "//div[@class ='container main']//div[@class ='project-page ']//h1[@class ='project-header page-header']",
            'project_brief': "//div[@class ='container main']//div[@class ='project-page ']//h1[@class ='project-header page-header']/small[@class]"}
        srcframe.multixpathparser(dict2)

        print '--------'
        print 'project_detail'

        pathstr = ["//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Donor']/../*",
                   "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Intent']/../*",
                   "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='StartPlanned']/../*",
                   "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='LoanType']/../*",
                   "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Transaction']/../*",

                   "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Capacity']",
                   "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Geocode']",


                   ]
        te1 = "//div[@class ='container main']//div[@class ='project-page ']//ul[@id='resources']/*"
        te2 = "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Description']"
        te3 = "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='ParticipatingOrganization']/../*"
        te3 = "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Contact']/../*"

        [srcframe.parser(xp) for xp in pathstr]
        print srcframe.parserwithoutadd(te2)

        backup = lxml.etree.HTML(srcframe.requesttext).xpath(
            "//div[@class='container main']//div[@class='project-page ']//li//text()")
        srcframe.add({'backup': [ws.strip()
                                 for ws in backup if ws.strip() != '']})

        for s in srcframe.data.keys():
            if s != 'backup':
                print s, ":", srcframe.data[s]
                pass

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
