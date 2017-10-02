# -*- coding: utf-8 -*-
import urllib2
import requests
import requests_cache
import sqlite3
import unqlite
import sys
import multiprocessing as mp
import lxml
import time
import random
import collections
import pandas as pd
from bs4 import BeautifulSoup
try:
    from collections import ChainMap
except ImportError:
    from chainmap import ChainMap


class SqliteDatabase():

    def __init__(self, targetpath):
        self.conn = self.InitalSqliteConnection(targetpath)
        self.table = self.UpdateTable()

    def InitalSqliteConnection(self, target):
        if target != 0:
            conn = sqlite3.connect(target)
        else:
            conn = sqlite3.connect(":memory:")

        return conn

    def CreaTetable(self, tablename, **varnameandtype):
        '''
        input Table Name as one variable and Variable Name & Variable Type as a series of dict-like parameter
        '''
        cursor = self.conn.cursor()
        command = ''
        for key, value in varnameandtype.items():
            command = command + key + ' ' + value + ','
        try:
            if command != '':

                cursor.execute("CREATE TABLE IF NOT EXISTS  %s (%s)" %
                               (tablename, command))
                self.conn.commit()
                return True
            else:

                pass
        except:
            print "Create table failed, table %s already exist" % tablename
            return False
        if command == '':
            raise ValueError, 'Empty Variable Name and Type, please define the Variables'

    def UpdateTable(self):
        cursor = self.conn.cursor()
        command = '''SELECT name FROM sqlite_master
        WHERE type='table'
        ORDER BY name;
        '''

        return cursor.execute(command)

    def insert(self, tablename, *var):
        cursor = self.conn.cursor()
        p = '?' + ',?' * (len(var) - 1)

        c.execute("INSERT INTO %s VALUES (%s)" % (tablename, p), var)
        self.conn.commit()
        self.table = self.UpdateTable()

    def Delete(self, tablename, **delvars):
        c = self.conn.cursor()
        for delvar, value in delvars.items():
            c.execute("DELETE FROM %s WHERE %s = ?" %
                      (tablename, delvar), (value,))
        self.conn.commit()
        self.table = self.UpdateTable()

    def display(self, tablename):
        c = self.conn.cursor()
        c.execute("SELECT * FROM %s" % tablename)
        print c.fetchall()

    def Update(self, tablename, wherevars, setvars):
        c = self.conn.cursor()

        wher = [(wherevar, wherevalue)
                for wherevar, wherevalue in wherevars.items()]
        command1 = '? = ?' + ',? = ?' * (len(wher) - 1)

        serv = [(setvar, setvalue)
                for setvar, setvalue in setvars.items()]
        command2 = '? = ?' + ',? = ?' * (len(serv) - 1)

        c.execute("UPDATE %s SET %s WHERE %s" %
                  (tablename, command1, command2), wher + serv)
        self.conn.commit()
        self.table = self.UpdateTable()


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
        self.src = src
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

            l = (DetectAscii(a.text, printout=False), a.attrib['href'])

            if l[0] != None and 'http' not in l[0] and 'More about this resource' not in l[0]:
                # print l[0].encode('utf-8')
                if l[1][0] == '/':
                    hrefstatusdict.append((l[0],  self.src + l[1]))
                else:
                    hrefstatusdict.append((l[0], self.src + '/' + l[1]))

            elif l[0] == None:

                if l[1][0] == '/':
                    hrefinsitelink.append(self.src + l[1])
                else:
                    hrefinsitelink.append(self.src + '/' + l[1])

            elif 'More about this resource' in l[0]:
                if l[1][0] == '/':
                    hrefinsitelink.append(self.src + l[1])
                else:
                    hrefinsitelink.append(self.src + '/' + l[1])

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

                        href[text[0]] = (DetectAscii(
                            g.text, printout=False), g.attrib['href'])

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

                        href[text[0]] = (DetectAscii(
                            g.text, printout=False), g.attrib['href'])

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
                # print var
                chain2 = {
                    var: dict([self.list2dict(self.detectchild(t)) for t in test2])}

        if addi:
            if chain2 != {}:
                self.add(chain2)
        else:
            return chain2


class UrlGenerator():

    def __init__(self, initialpage):
        if initialpage == '' or initialpage == 'default':
            self.initialpage = 'http://china.aiddata.org/projects?utf8=%E2%9C%93&search='
        else:
            self.initialpage = initialpage
        self.projectinfo = []
        self.count = 0
        self.columnnames = []
        self.columnslink = []
        self.__status__ = 'Idle - Idle'
        self.RequestUrl(self.initialpage)

    def RequestUrl(self, url):
        t = lxml.etree.HTML(requests.get(url).text)

        for table in t.xpath("//table[@class='table table-hover']"):

            for t in table.getchildren():
                if self.columnnames == [] and t.tag == 'thead':

                    self.columnnames = [th.xpath('a/text()')[0]
                                        for th in t.xpath('//th')]

                    self.columnslink = [th.xpath('a[@href]')[0].attrib[
                        'href'] for th in t.xpath('//th')]

                elif t.tag == 'tbody':
                    project = [[self.ProjectTitleParse(
                        td) for td in tr.getchildren() if self.ProjectTitleParse(td) != None] for tr in t.xpath("//tr")]
                    if project[0][0][0] == 'ID':
                        project = project[1:]
                    test = pd.DataFrame(project, columns=self.columnnames)
                    test['Url'] = [title[1] for title in list(test.Title)]
                    test['Title'] = [title[0] for title in list(test.Title)]
                    self.projectinfo.append(test)
        returnvalue = self.DoNext(t, urlversion='parsed')
        if returnvalue == 0:
            self.projectinfo = pd.concat(self.projectinfo)
            # self.projectinfo.to_hdf('ChinaAid.h5', 'ChinaAid')
            self.projectinfo.to_csv('ChinaAid_own.csv')
            pass
        else:
            time.sleep(1)
            self.count = self.count + 1
            print "                  ", self.count

            self.RequestUrl(returnvalue)

    def ProjectTitleParse(self, td):
        if len(td) < 1:

            return DetectAscii(td.text, printout=False)

        elif len(td) == 1 and td[0].tag == 'a':
            if 'href' in td[0].attrib.keys():

                url_temp = 'http://china.aiddata.org' + \
                    td[0].attrib['href']

            else:
                url_temp = ''
            if td[0].text is not None:
                return (DetectAscii(td[0].text, printout=False), url_temp)

            elif td[0].getchildren()[0].tag == 'span':
                return (DetectAscii(td[0].getchildren()[0].text, printout=False), url_temp)

    def DoNext(self, url, urlversion='parsed'):
        if urlversion == 'parsed':
            t = url.xpath(
                "//div[@class='pagination']//li[@class='next next_page ']/a[@rel='next' and @href]")
        else:
            t = lxml.etree.HTML(requests.get(url).text).xpath(
                "//div[@class='pagination']//li[@class='next next_page ']/a[@rel='next' and @href]")
        if t != []:

            return 'http://china.aiddata.org' + [ts.attrib['href'] for ts in t][0]

        else:
            self.__status__ = 'Working - Meet Last Page; Will Stop'
            return 0


def main(testurlpath, headers='default'):
    if headers == 'default':
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    else:
        pass

    request = requests.get(testurlpath, headers=headers)

    test = lxml.etree.HTML(request.text).xpath(
        "//div[@class='container main']/iframe")

    if 'src' in test[0].keys():
        srcframe = Inhtml(test[0].attrib['src'], headers,
                          publicaddress='http://china.aiddata.org/', AutoCollect=True)
        return srcframe.data, srcframe.link
    elif len(test) != 1:
        raise ValueError, 'iframe contain multi-information'


def DetectAscii(text, printout=True):

    try:
        if printout:

            print text.encode('utf-8')

        else:
            return text.encode('utf-8')

    except AttributeError:
        if printout:
            print text
        else:
            return text


class nolsql(unqlite.UnQLite):

    def __init__(self,  path):
        if path == 'default' or path == ':mem:':
            unqlite.UnQLite.__init__(self)
        else:
            unqlite.UnQLite.__init__(self, filename=path)
        self.conflict = []
        self.duplicate = {}

    def detectduplicate(self, key, value):
        if key not in self.keys():
            self.append(key, value)
        else:
            if self[key] == [value]:
                try:
                    self.duplicate[key] = self.duplicate[key] + 1
                except KeyError:
                    self.duplicate[key] = 1
            else:
                self.conflict.append(key)
                self[key].append(value)

    def add(self, var):
        if isinstance(var, dict):

            for key, value in var.items():
                self.detectduplicate(key, value)
        else:
            raise TypeError, 'Unsupported Type'


def progress_test(counts, lenfile, speed):
    bar_length = 20

    process = counts / float(lenfile)

    ETA = speed * (lenfile - counts) / float(60)
    hashes = '#' * int(process * bar_length)
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("""\r%d%%|%s|completed %d * projects|Speed : %.4f s/ projects|ETA: %s min""" %
                     (process * 100, hashes + spaces, counts, speed, ETA))

    sys.stdout.flush()


def dosomething(iurl):
    #globals()['count'], retry
    ids, url = iurl
    f = time.time()
    try:
        data, link = main(url)
        # print data
        dic = {"data": data.maps, "link": link.maps, "ID": ids}

        globals()['count'] = globals()['count'] + 1
        if globals()['retry'] > 5:
            globals()['retry'] = globals()['retry'] - 1
        return dic
    except IndexError, e:
        print e
        globals()['retry'] = globals()['retry'] + 1

        if globals()['retry'] > 50:
            raise IndexError, 'Max retries, Will Stop'

    else:
        time.sleep(5)
    time.sleep(1)
    progress_test(globals()['count'], globals()['lenfile'], time.time() - f)


def chunks(target, n):
    if isinstance(target, list):
        date1 = [target[i:i + n] for i in xrange(0, len(target), n)]
    else:
        date1 = []
        raise ValueError, "Wrong type,I need a list."
    return date1
if __name__ == '__main__':
    requests_cache.install_cache(
        cache_name="ChinaAidProjectInfo", backend="sqlite", expire_date=300)
    Data = DataContainer()

    initialpage = 'http://china.aiddata.org/projects?utf8=%E2%9C%93&search='

    urlpath = 'http://china.aiddata.org/projects/'
    projectid = 2521
    # testurlpath = urlpath + str(projectid)

    africa = nolsql('ChinaAidProjectDetail.db').collection('africa')
    africa.create()

    Cr = africa.filter(lambda obj: obj['ID'] != None)
    collected = [c['ID'] for c in Cr]
    # print collected

    urllist = pd.read_csv('ChinaAid_own.csv')['Url'].tolist()
    idurl = [(ur.split('/')[-1], ur) for ur in urllist]
    uncollected = []
    for i in idurl:
        if i[0] in collected:
            pass
        else:
            uncollected.append(i)

    count = 0
    retry = 0
    lenfile = len(uncollected)
    multipool = False
    # print len(idurl), lenfile
    if lenfile != 0:
        if multipool == False:
            for (ids, url) in uncollected:

                f = time.time()
                try:
                    data, link = main(url)
                    # print data
                    africa.store(
                        {"data": data.maps, "link": link.maps, "ID": ids})
                    count = count + 1
                    if retry > 5:
                        retry = retry - 1
                except IndexError, e:
                    print e
                    retry = retry + 1

                    if retry > 20:
                        raise IndexError, 'Max retries, Will Stop'

                else:
                    time.sleep(5)
                time.sleep(1)
                progress_test(count, lenfile, time.time() - f)
        else:
            chunked = chunks(uncollected, 48)
            pool = mp.Pool()

            for chunk in chunked:
                templist = pool.map(dosomething, chunk)

                africa.store(templist)
                time.sleep(5)

                # for afkey, value in africa.all():

                # print pd.DataFrame.from_dict(data.maps)
                # print link.keys()
                #--------

                # dataset = main(testurlpath)
                # print dataset[0]

                #-----------
                #-----------
                # do next

                # UrlGenerator(initialpage)

                # print ts.text
