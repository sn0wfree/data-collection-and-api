# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------
'''
this code is for personal use.

'''
# Copyright by Lin Lu 2017
# version control


__author__ = 'sn0wfree'
__version__ = '0.01'


#-------------------------------------------------------------------------

from lxml import etree
import requests
import requests_cache
import pandas as pd
import unqlite
import sqlite3
import downloadfile
import multiprocessing as mp


def DownloadMinistrylink(url_en):
    # url_en = 'https://en.wikipedia.org/wiki/State_Council_of_the_People%27s_Republic_of_China'
    # url_zh =
    # 'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E5%9B%BD%E5%8A%A1%E9%99%A2'
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

    request = requests.get(url_en, headers=headers).text
    public = 'https://en.wikipedia.org'
    requesttext = etree.HTML(request)
    xpth = '//*[@id="mw-content-text"]/div/ol[1]/*'

    w = pd.DataFrame([(a.text, public + a.attrib['href'])
                      for li in requesttext.xpath(xpth) for a in li.getchildren()], columns=['title', 'url'])
    return w

if __name__ == '__main__':
    requests_cache.install_cache(
        cache_name="Leader", backend="sqlite", expire_date=300)
    url_en = 'https://en.wikipedia.org/wiki/State_Council_of_the_People%27s_Republic_of_China'
    url_zh = 'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E5%9B%BD%E5%8A%A1%E9%99%A2'

    # ministrylink = DownloadMinistrylink(url_zh)
    # print ministrylink
    # print ministrylink['url'][1],
    r = requests.get('https://dumps.wikimedia.org/zhwiki/').text
    rt = etree.HTML(r).xpath("//pre/a[@href='latest/']")
    'latest/'
    pc = 'https://dumps.wikimedia.org/zhwiki/'
    # print dir(rt[0])
    # dlink = pc + rt[0].getprevious().attrib['href']
    dlinks = ['https://dumps.wikimedia.org/zhwiki/20171001/zhwiki-20171001-pages-meta-current.xml.bz2',
              'https://dumps.wikimedia.org/zhwiki/20171001/zhwiki-20171001-pages-articles.xml.bz2'
              ]

    # dlink = 'https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-stub-articles.xml.gz'
    # pool = mp.Pool()

    # pool.map(lambda dlink: downloadfile.python_download(dlink, dlink.split('/')[-1]), dlinks)
    for dlink in dlinks:
        downloadfile.python_download(dlink, dlink.split('/')[-1])

    # for dlink in dlinks:

    # ministrylink = pd.read_csv('Ministry-link.csv')
