#-*- coding:utf-8 -*-

#-------------------
__version__ = "0.2"
__author__ = "sn0wfree"
'''
This tool is for importing the stock
'''
#-------------------
#-------------------
#-------------------
#-------------------

import pandas as pd

import os,gc
import sqlite3


def write_txt(a,filename):
	with open(filename,'w') as f:
		for ff in a:
			f.write(ff + '\n')

def collectedtablename(conn):
    cur = conn.cursor()
    cur.execute(
        "select name from sqlite_master where type='table' order by name")
    tablename = [table[0].encode("utf-8") for table in cur.fetchall()]
    return tablename

def DetectTableOrTickerName(Table_List_Ticker):
    table =[]
    for tablename in Table_List_Ticker:
        if 'Equity' in tablename:
            table.append(tablename.split(' ')[0])
        
        elif tablename.find(' ') <5:
            table.append(tablename[0:tablename.find(' ')])

        else:
            table.append(tablename)
    return table


if __name__ == '__main__':
	
	gc.enable()
	csvfile = 'shares.csv'
	shares =pd.read_csv(csvfile)

	s =set(shares['TICKER'].tolist())

	s.remove(list(s)[0])

	ColumnsName=shares.columns.tolist()

	ColumnsName[1]='Date'
	
	

	shares.columns=ColumnsName
	matched_list =zip(s,DetectTableOrTickerName(s))


	conn= sqlite3.connect("sharesWRDS.db")


	for tcker_equity,tcker in matched_list[0:5]:
	    #pd_temp =shares[shares.TICKER==tcker_equity].reset_index()
	    #del pd_temp['index']
	    print tcker_equity,tcker
	    #pd_temp.to_sql(tcker, conn, if_exists='append', index=False)


# In[34]:




# In[ ]:



