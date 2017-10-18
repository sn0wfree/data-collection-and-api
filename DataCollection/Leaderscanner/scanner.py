# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
"""
This code is for personal use.

"""
# Copyright by Lin Lu 2017
# version control


__author__ = 'sn0wfree'
__version__ = '0.02'


import datetime
import multiprocessing as mp
import sys

import chardet
import pandas as pd
# -------------------------------------------------------------------------
import requests
import requests_cache
import xlrd
from lxml import etree


def RepalceYMD2Eng(pdseries, status='Store'):
    symbollist = ['年'.decode(
        'utf-8'), '月'.decode('utf-8'), '日'.decode('utf-8')]
    for symbol in symbollist:
        pdseries = pdseries.str.replace(symbol, '-')
        # pdseries =[d[:-2] if str(d)[-1] == '-' else d for d in
        # pdseries.tolist()]
    c = []
    year = []
    for d in pdseries.tolist():
        year.append(d[0:4])
        try:
            if d[-1] == '-':

                c.append(d[:-1])
            elif d == 'Now':
                if status == 'Parse':
                    c.append(str(datetime.date.today()))
                else:
                    c.append(d)
            else:
                c.append(d)
        except Exception:
            c.append(d)

    return c, year


def ImportMinistryData(status='cache'):
    if status == 'cache':
        try:
            ministry = pd.read_hdf('ministry.h5', 'ministrylist')

        except Exception as e:
            print e
            status = 'ReadFile'
    if status == 'ReadFile':
        ministry_file = pd.ExcelFile("ministry.xlsx")
        ministry_list = []
        for sheetname in ministry_file.sheet_names:
            tempdf = ministry_file.parse(sheetname)[
                ['Name', 'Start', 'End', 'Jobtitle']]
            tempdf['Ministry Section'] = [sheetname] * tempdf.shape[0]
            ministry_list.append(tempdf)
        ministry = pd.concat(ministry_list)
        ministry = ministry.reindex()
        ministry['End'], ministry['EndYear'] = RepalceYMD2Eng(ministry['End'])
        ministry['Start'], ministry['StartYear'] = RepalceYMD2Eng(ministry[
                                                                  'Start'])
        # ministry.to_hdf('ministry.h5', 'ministrylist')
    return ministry


def progress_test(counts, lenfile, speed):
    bar_length = 20

    process = counts / float(lenfile)

    ETA = speed * (lenfile - counts) / float(60)
    hashes = '#' * int(process * bar_length)
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("""\r%d%%|%s|completed %d *5 projects|Speed : %.4f s/5 projects|ETA: %s min""" %
                     (process * 100, hashes + spaces, counts, speed, ETA))

    sys.stdout.flush()


class ScanFMPRCGov():

    def __init__(self, urllist):
        self.url = urllist
        self.data = []

    def multiprocessing(self, variableslist, func='default'):
        pool = mp.Pool()
        if func == 'default':
            return pool.map(self.ScanWebPage, variableslist)
        else:
            return pool.map(func, variableslist)

    def ScanWebPage(self, url):
        r = self.RequestDecodeHtmlParse(url).xpath(
            "//div[@class='rebox_title']")[0]
        root = url.split('/default')[0]

        if r.text == '外事日程'.decode('utf-8') and r.getnext().attrib['class'] == 'rebox_news':
            for u in r.getnext().getchildren():
                if u.tag == 'ul':

                    for li in u.getchildren():
                        text = li.xpath('string(.)')[:-12]
                        date = li.xpath('string(.)')[-11:-1]
                        if len(li.getchildren()) == 1:
                            href = root + \
                                li.getchildren()[0].attrib['href'][1:]
                        else:
                            href = [root + x.attrib['href'][1:]
                                    for x in li.iterchildren()]

                        self.data.append((text, date, href))
        return self.data

    def RequestDecodeHtmlParse(self, url):
        response = requests.get(url)

        return etree.HTML(response.content.decode(sys.getfilesystemencoding()))
if __name__ == '__main__':

    requests_cache.install_cache(
        cache_name="Leader", backend="sqlite", expire_date=300)
    # ministry = ImportMinistryData()

    # Jobtitle = [title.decode('utf-8')for title in ['部长', '副总理', '总理', '秘书长', '行长']]
    # ministryup = ministry[ministry.Jobtitle != '国务委员'.decode('utf-8')]
    # print ministryup[ministryup.StartYear >= str(2000)]

    public = ['http://www.fmprc.gov.cn/web/wjdt_674879/wsrc_674883/default_%d.shtml' %
              d for d in xrange(1, 67)]
    public.append(
        'http://www.fmprc.gov.cn/web/wjdt_674879/wsrc_674883/default.shtml')
    #url = public[1]
    # print url
    scanner = ScanFMPRCGov(public)
    data = scanner.multiprocessing(public)

    pd.DataFrame(data, columns=['Text', 'Date', 'Url']).to_csv('fmprcscan.csv')


# print RepalceYMD2Eng(ministry['End'],status='Parse')
# /html/body/div[1]/div[5]/div[2]/div[2]
# (2017-10-03)
#
