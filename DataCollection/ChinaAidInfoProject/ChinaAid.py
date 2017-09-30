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


def InitalSqliteConnection(target):
    if target != 0:
        conn = sqlite3.connect(target)
    else:
        conn = sqlite3.connect(":memory:")

    return conn


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

    def __init__(self, src, header, publicaddress, AutoCollect=False):
        self.requesttext = requests.get(src, headers=header).text
        self.data = ChainMap()
        self.link = ChainMap()
        self.publicaddress = publicaddress
        self.AutoCollection(AutoCollect=AutoCollect)

    def AutoCollection(self, AutoCollect=False):
        if AutoCollect:
            dict2 = {
                'project_name': "//div[@class ='container main']//div[@class ='project-page ']//h1[@class ='project-header page-header']",
                'project_brief': "//div[@class ='container main']//div[@class ='project-page ']//h1[@class ='project-header page-header']/small[@class]"}
            self.multixpathparser(dict2)
            pathstr = ["//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Donor']/../*",
                       "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Intent']/../*",
                       "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='StartPlanned']/../*",
                       "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='LoanType']/../*",
                       "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Transaction']/../*",
                       "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='ParticipatingOrganization']/../*",
                       "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Contact']/../*",
                       "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Description']",
                       "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Geocode']",

                       "//div[@class ='container main']//div[@class ='project-page ']//li[@flaggable_type='Capacity']"
                       ]
            [self.parser(xp) for xp in pathstr]
            backup = lxml.etree.HTML(self.requesttext).xpath(
                "//div[@class='container main']//div[@class='project-page ']//li//text()")
            self.add({'Backup': [ws.strip()
                                 for ws in backup if ws.strip() != '']})

            self.HrefAdd(hrefxpth='default')
        else:
            pass

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

    def HrefAdd(self, hrefxpth):
        if hrefxpth == '' or hrefxpth == 'default':
            hrefxpth = "//div[@class='container main']//div[@class='project-page ']//a[@href]"
        else:
            pass

        href = lxml.etree.HTML(self.requesttext).xpath(hrefxpth)
        hrefstatusdict = []
        hrefinsitelink = []
        hrefinsitelinkbackup = []

        for a in href:
            try:
                l = (a.text, a.attrib['href'])
            except UnicodeEncodeError, e:
                l = (a.text.encode('utf-8'), a.attrib['href'])

            if l[0] != None and 'http' not in l[0] and 'More about this resource' not in l[0]:
                # print l[0].encode('utf-8')
                if l[1][0] == '/':
                    hrefstatusdict.append((l[0], urlpath[:-2] + l[1]))
                else:
                    hrefstatusdict.append((l[0], urlpath + l[1]))

            elif l[0] == None:

                if l[1][0] == '/':
                    hrefinsitelink.append(urlpath[:-2] + l[1])
                else:
                    hrefinsitelink.append(urlpath + l[1])

            elif 'More about this resource' in l[0]:
                if l[1][0] == '/':
                    hrefinsitelink.append(urlpath[:-2] + l[1])
                else:
                    hrefinsitelink.append(urlpath + l[1])

            elif 'http' in l[0]:
                hrefinsitelinkbackup.append(l[0])

        self.link['Status'] = dict(hrefstatusdict)
        self.link['InSiteLink'] = hrefinsitelink
        self.link['InSiteLinkBackup'] = hrefinsitelinkbackup
        # print hrefinsitelink
        # print hrefinsitelinkbackup

    def xpathparser(self, pathstr, variablename, addi=True):
        x = lxml.etree.HTML(self.requesttext).xpath(pathstr)
        if len(x) == 1:
            if addi:
                self.add({variablename: x[0].text.strip()})

            return (variablename, x[0].text.strip())
        elif len(x) > 1 and addi:
            temp = {variablename + 'of' + str(x.index(value)): value.text.strip()
                    for value in x}
            if addi:
                self.add(temp)
            return temp

        else:

            if addi:
                self.add({variablename: 'NULL'})
            return (variablename, 'NULL')

    def multixpathparser(self, *args, **kwargs):

        t1 = [self.xpathparser(di[key], key, addi=False)
              for di in args for key in di.keys()]
        t2 = [self.xpathparser(value, key, addi=False)
              for key, value in kwargs.items()]
        self.add(dict(t1))
        self.add(dict(t2))

    def detectchild(self, t, hrefstatus=False):

        if len(t.getchildren()) > 1:
            text = [w.strip() for g in t.getchildren()
                    for w in g.xpath('.//text()') if w.strip() != '']

            # print t.xpath('./*[starts-with(name(),'ul')]')
            #     print pr
            if hrefstatus:
                href = {}
                for g in t.getchildren():
                    if g.tag == 'a' and 'href' in g.attrib.keys():
                        try:
                            href[text[0]] = (g.text, g.attrib['href'])
                        except UnicodeEncodeError:
                            href[text[0]] = (g.text.encode(
                                'utf-8'), g.attrib['href'])
                if href != {}:
                    self.link = self.link.new_child(href)
            else:
                pass

            # href[g.text] = g.attrib['href']
            # href.append(dict(g.text, g.attrib['href']))

        elif len(t.getchildren()) == 1:
            text = [v.strip() for v in t.xpath(".//text()") if v.strip() != '']

            if hrefstatus:
                href = {}
                for g in t.getchildren():
                    if g.tag == 'a' and 'href' in g.attrib.keys():
                        try:
                            href[text[0]] = (g.text, g.attrib['href'])
                        except UnicodeEncodeError:
                            href[text[0]] = (g.text.encode(
                                'utf-8'), g.attrib['href'])
                if href != {}:
                    self.link = self.link.new_child(href)
            else:
                pass
        else:
            text = []
        return text

    def list2dict(self, ls):

        if ':' in ls[0]:
            key = ls[0][: -1]

            value = ls[1:]
        elif ls != []:
            key = ls[0]
            value = ls[1:]
        else:
            key = 'NULL'
            value = 'NULL'
        return (key, value)

    def parser(self, xpth, addi=True, special=False):

        var = xpth.split('@flaggable_type=')[-1].split("'")[1]
        test2 = lxml.etree.HTML(self.requesttext).xpath(xpth)
        if var not in ['Description', 'ParticipatingOrganization', 'Contact', 'Geocode']:
            chain2 = dict([self.list2dict(self.detectchild(t)) for t in test2])
        else:
            if len(test2) == 1:
                chain2 = {var: self.detectchild(test2[0])}
            else:
                print var
                chain2 = {
                    var: dict([self.list2dict(self.detectchild(t)) for t in test2])}

        if addi:
            if chain2 != {}:
                self.add(chain2)
        else:
            return chain2


def main(testurlpath, headers='default'):
    if headers == 'default':
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    else:
        pass

    request = requests.get(testurlpath, headers=headers)

    test = lxml.etree.HTML(request.text).xpath(
        "//div[@class='container main']/iframe")
    if len(test) != 1:
        raise ValueError, 'iframe contain multi-information'
    elif 'src' in test[0].keys():
        srcframe = Inhtml(test[0].attrib['src'], headers,
                          publicaddress='http://china.aiddata.org/', AutoCollect=True)

    return srcframe.data, srcframe.link

if __name__ == '__main__':
    requests_cache.install_cache(
        cache_name="ChinaAidProjectInfo", backend="sqlite", expire_date=300000)
    Data = DataContainer()

    urlpath = 'http://china.aiddata.org/projects/'
    projectid = 2521
    testurlpath = urlpath + str(projectid)
    #--------

    dataset = main(testurlpath)
    print dataset[0]

    #-----------


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
