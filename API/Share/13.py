#-*- coding:utf-8 -*-

#-------------------
__version__ = "0.2"
__author__ = "sn0wfree"
'''
This tool is for download the shares
'''
#-------------------
import urllib2
import csv
import cookielib
import os


def ImportListInfobyFile(locals_file_path, target=False, GUI=False):
    keywords = []

    scan_files = os.listdir(locals_file_path)
    if target != False:

        with open(target, 'r') as ticker:
            ticker = ticker.readlines()
            for line in ticker:
                keywords.append(line.strip())

    else:

        if 'keywords.txt' in scan_files:
            fi = read_a_file('keywords.txt')
            for f in fi:
                keywords.extend(f.split()[0].split(','))
        elif 'keywords2.txt' in scan_files:
            fi = read_a_file('keywords2.txt')
            for f in fi:
                keywords.extend(f.split()[0].split(','))
        elif 'keywords.csv' in scan_files:
            fi = pd.read_csv('keywords.csv')
            keywords = fi['tinker']
        else:
            keywords = 0

    return keywords
if __name__ == '__main__':

    #site = "http://xueqiu.com/S/AAPL/historical.csv"
    #site= "http://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getHistoricalData.jsp?symbol=JPASSOCIAT&fromDate=1-JAN-2012&toDate=1-AUG-2012&datePeriod=unselected&hiddDwnld=true"
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    #req = urllib2.Request(site, headers=hdr)
    symbolTest = 'APPL'
    ticker = 'ticker.csv'
    locals_file_path = os.path.split(os.path.realpath(__file__))[0]
    # with open(ticker) as csvfile:
    #    reader = csv.DictReader(csvfile)
    # print reader
    Symbol = ImportListInfobyFile(locals_file_path, ticker)

    try:

        for symbol in Symbol:

            if '^' not in symbol:
                site = "http://xueqiu.com/S/" + symbol + "/historical.csv"
                req = urllib2.Request(site, headers=hdr)
                page = urllib2.urlopen(req)
                #content = page.read()
                with open(Exchange + '/' + symbol + '.csv', 'w') as symbolCSV:
                    symbolCSV.write(page.read())
            else:
                print 'symbol contains ^, not valid, passed...'

    except urllib2.HTTPError, e:
        print e.fp.read()
