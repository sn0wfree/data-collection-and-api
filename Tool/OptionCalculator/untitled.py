# -*- coding: utf-8 -*-
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')
headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'use rsurvey=1; v=AQehqnGOEZp69pUfZQxnXGF8kLDUDNvuNeBfYtn0Ixa9SClk4dxrPkWw77Pp',
        'DNT':'1',
        'Host':'basic.10jqka.com.cn',
        'Upgrade-Insecure-Requests':'1'}
def check_contain_chinese(check_str):
        for ch in check_str.decode('utf-8'):
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False
class CollectAndSearchFromSqlite():
    def __init__(self):
        pass
        
    def Import2Sqlite(self,sqlitename,dataframe,tablename):
        conn=self.InitialSqliteConnection(sqlitename)
        conn.text_factory = str
        #dataframe=dataframe.append(pd.read_sql('SELECT DISTINCT * FROM %s'%tablename,conn).drop(['index'],axis=1)).drop_duplicates()
        dataframe.to_sql(tablename, conn, if_exists='append')
        conn.commit()
        conn.close()
    def Vacuum(self,sqlitename,tablename): 
        conn=self.InitialSqliteConnection(sqlitename)
        conn.text_factory = str
        dataframe=pd.read_sql('SELECT DISTINCT * FROM %s'%tablename,conn).drop(['index'],axis=1)
        dataframe.to_sql(tablename, conn, if_exists='replace')
        conn.commit()
        conn.close()

    def InitialSqliteConnection(self,target):
        import sqlite3
        if target != 0:
            conn = sqlite3.connect(target,timeout=10)
        else:
            conn = sqlite3.connect(":memory:")
        return conn
    def CollectWarrant(self,response,titles,replacelist,targetstockinfo,code,filetype='web',marketcode='HK'):
        import pandas as pd
        from lxml import etree
        if filetype=='file':
            w=etree.parse(response,)
        elif filetype == 'web':
            w=etree.HTML(response.text)
        if w.xpath('//*[@id="warrant"]/div[2]/table') ==[]:
            raise Exception('Unknown Code:%s'%code)
        else:
            table=w.xpath('//*[@id="warrant"]/div[2]/table')[0]
        #tbody=w.xpath('//*[@id="warrant"]/div[2]/table/tbody')[0]
        #title=table.getchildren()[0]
        tbody=table.getchildren()[1]
        collection=[[j.text for j in item_cont.getchildren()] for item_cont in tbody.getchildren()] 
        #titles=['代码','名称','类别','结算方式','行使价','行权期起始','行权期截止','最后交易日','到期日' ]   
        option=pd.DataFrame(collection,columns=titles)
        if '.' not in list(option['代码'])[2]:
            option['代码']=option['代码']+['.%s'%marketcode]*option.shape[0]
        else:
            pass
        titles_en= [replacelist[title] if title in replacelist.keys() else title for title in titles ]
        name=self.GetName(w).decode('utf-8')
        option.columns=titles_en
        option['StockCode']=[targetstockinfo[0]]*option.shape[0]
        option['StockName']=[name]*option.shape[0]
        option['RecordingTime']=[datetime.datetime.now()]*option.shape[0]
        return option
    
    def GetName(self,we):
        if len(we.xpath('/html/body/div[1]/div[1]/div[2]/div[1]/h1')[0].getchildren())>1:
            return we.xpath('/html/body/div[1]/div[1]/div[2]/div[1]/h1')[0][0].text.strip()
        else:
            return we.xpath('/html/body/div[1]/div[1]/div[2]/div[1]/h1')[0].text.strip()
        

    def main(self,code,name,marketcode='HK',tosql=True):
        
        import requests
        if not check_contain_chinese(code):
            pass
        else:
            raise Exception("Unknown Code")
        
        
        if '.'  in code:
            code=marketcode+code.split('.')[0]
        elif code[:2] == marketcode:
            pass
        else:
            raise Exception("unknown type of securities code:%s"%code)
        responseurl='http://basic.10jqka.com.cn/%s/warrant.html'%code
        response=requests.get(responseurl,headers=headers)
        targetstockinfo=(code,name)
        titles=['代码','名称','类别','结算方式','行使价','行权期起始','行权期截止','最后交易日','到期日' ]
        replacelist={'代码':'WarrantCode','名称':'WarrantName','行权期起始':'StartofExercisePeriod','行权期截止':'EndofExercisePeriod','最后交易日':'LastTradingDay','结算方式':'SettlementMethod','类别':'Type','行使价':'ExercisePrice','到期日':'ExpirationDate'}

        option=self.CollectWarrant(response,titles,replacelist,targetstockinfo,code=code,filetype='web',marketcode=marketcode)
        if tosql:
            self.Import2Sqlite('WarrantsFromWeb.sqlite',option,code)
        else:
            return option

if __name__ == '__main__':
    carrier=CollectAndSearchFromSqlite()
    print carrier.main('0700.HK','腾讯')
