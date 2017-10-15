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

# import urllib2

import collections

import pandas as pd
import requests
import requests_cache
from lxml import etree

import downloadfile


def DownloadMinistrylink(url_en):
    """
    Description: This function is to download the Link of Ministry in Wikipedia.

    Input: Wikipedia src page.

    Output: DataFramized data; data format: | Ministry | link |

    """
    # url_en = 'https://en.wikipedia.org/wiki/State_Council_of_the_People%27s_Republic_of_China'
    # url_zh =
    # 'https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E5%9B%BD%E5%8A%A1%E9%99%A2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

    request = requests.get(url_en, headers=headers).text
    public = 'https://en.wikipedia.org'
    requesttext = etree.HTML(request)
    xpth = '//*[@id="mw-content-text"]/div/ol[1]/*'

    w = pd.DataFrame([(a.text, public + a.attrib['href'])
                      for li in requesttext.xpath(xpth) for a in li.getchildren()], columns=['title', 'url'])
    return w


def downloadwikipagefromdump():
    """
    Description: This function is to download the Dump(article-page) of Wikipedia.

    Input: None

    Output: Stored dump files, No print out

    """
    r = requests.get('https://dumps.wikimedia.org/zhwiki/').text
    rt = etree.HTML(r).xpath("//pre/a[@href='latest/']")
    'latest/'
    pc = 'https://dumps.wikimedia.org/zhwiki/'
    print pc + rt[0].getprevious().attrib['href']

    dlinks = ['https://dumps.wikimedia.org/zhwiki/20171001/zhwiki-20171001-pages-meta-current.xml.bz2',
              'https://dumps.wikimedia.org/zhwiki/20171001/zhwiki-20171001-pages-articles.xml.bz2']
    for dlink in dlinks:
        downloadfile.python_download(dlink, dlink.split('/')[-1])

# downloadwikipagefromdump()


class Catchinfo():

    def __init__(self):
        self.collection = collections.OrderedDict()
        self.temp = []

    def loop(self, element):
        while element is not None:
            tag, value = self.detecttag(element)

            if tag == 'h3':
                if self.temp != []:
                    self.collection.update({self.temp[0]: self.temp[1:]})
                    self.temp = []
                    self.temp.append(value)
            elif tag == 'pass':
                pass
            else:
                self.temp.append(value)

            element = element.getnext()

    def detecttag(self, element):
        try:
            if element.tag == 'h3':
                name = element.getchildren()[1].text
                return 'h3', name

            elif element.tag == 'p':
                title = element.getchildren()[0].text
                # link
                link = [(child.text.strip(), child.attrib['href'])
                        for child in element.getchildren()]
                return 'p', title
            elif element.tag == 'ul':
                return 'ul', {child.text.strip(): [u.text.strip() for u in child.iterchildren()]
                              for child in element.iterchildren()}

            elif element.tag == 'div':
                return 'pass', 'div'

            elif type(element.tag) != str:
                return 'pass', 'none str'
            else:
                return 'pass', '%s' % element.tag

        except Exception as e:
            if element == None:
                return 'end', None
            else:
                return 'error', (element, element.tag)
                # raise ValueError, 'Unexpected error'


if __name__ == '__main__':
    requests_cache.install_cache(
        cache_name="Leader", backend="sqlite", expire_date=300)
    url_en = 'https://en.wikipedia.org/wiki/State_Council_of_the_People%27s_Republic_of_China'
    url_zh = 'https://zh.wikipedia.org/wiki/中华人民共和国国务院'
    headers = {
        'authority': 'zh.wikipedia.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

    # print urllib2.urlopen(urllib2.Request(url_zh,
    # headers=headers)).read().decode('utf-8')
    # print requests.get(url_zh, headers=headers).text

    with open('htmlwikiminstry.html', 'r') as wikiminstry:
        minstry = wikiminstry.read()

    minstrytext = etree.HTML(minstry)
    maininfo_name = minstrytext.xpath(
        "//span[@id='.E5.8E.86.E5.B1.8A.E5.9B.BD.E5.8A.A1.E9.99.A2.E4.B8.BB.E8.A6.81.E6.83.85.E5.86.B5']/..")[0]
    first = maininfo_name.getnext().getnext().getnext()
    # print first.tag
    li = []
    tt = minstrytext.xpath(
        "//div[@class='rellink noprint relarticle mainarticle']")
    # print tt[-1].getnext().getnext().getnext().getnext().getnext().getnext()
    # print first.getnext().getnext().getchildren()
    # print type(first.tag) == str
    # print first.getchildren()[1].text
    d = {s.text.strip(): [u.text for u in s.iterchildren()]
         for s in first.getnext().getnext().iterchildren()}

    c = Catchinfo()
    c.loop(first)
    for k, v in c.collection.items():
        if '十'.decode('utf-8') in k:
            for vs in v:
                if isinstance(vs, dict):
                    for key, values in vs.items():
                        for value in values:

                            print k, key, ":", value
