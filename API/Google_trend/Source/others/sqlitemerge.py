
#-*- coding:utf-8 -*-

#-------------------
__version__ = "0.2"
__author__ = "sn0wfree"
'''
This tool is for download the shares
'''
#-------------------
#-------------------
#-------------------
#-------------------

import os,sqlite3,gc,platform
import pandas as pd


def list2dict(keys,values):
	a_dict = {}
	junk = map(lambda k, v: a_dict.update({k: v}), keys, values)
	return junk

def InitalSqliteConnection(target):
	
    if target != 0:
    	conn = sqlite3.connect(target)
    else:
    	conn = sqlite3.connect(":memory:")
        
    return conn

def CollectedTableName(conn):
    cur = conn.cursor()
    cur.execute(
        "select name from sqlite_master where type='table' order by name")
    return [table[0].encode("utf-8") for table in cur.fetchall()]
    
def FindOperation():
    OperationSystem = platform.system()
    if OperationSystem is 'Darwin':
        link = '/'
    elif OperationSystem is 'Windows':
        link = '\\'
    else:
        link = '/'
    return link

def DetectFileName(filepath):
	link = FindOperation()
	if '.' in filepath:
		if link in filepath:
			filename = filepath.split(link)[-1].split('.')[0]

		else:
			filename = filepath.split('.')[0]
	else:
		raise 'Unknown File Name'

	return filename

if __name__ == '__main__':
	DB_File='shareWRDS.db'
	File_Name = DetectFileName(filepath)

	#connection

	

	conn=InitalSqliteConnection(DB_File)
	#locals['%s_Table_List_Ticker'%File_Name]() = CollectedTableName(conn)
	Table_List_Ticker= CollectedTableName(conn)
	
	#for tablename in locals['%s_Table_List_Ticker'%File_Name]():
	for tablename in Table_List_Ticker:
		if 'Equity' in tablename:
			tablename =tablename.split(' ')[0]
		
		elif tablename.find(' ') <5：
			tablename = tablename[0:tablename.find(' ')]
		
		else:
			tablename =tablename[0:3]


