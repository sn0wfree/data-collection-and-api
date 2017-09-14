#-*- coding:utf-8 -*-

#-------------------
__version__ = "0.2"
__author__ = "sn0wfree"
'''
This tool is for importing the googlesearch
'''
#-------------------
#-------------------
#-------------------
#-------------------

import pandas as pd
import os
import sqlite3

if __name__ == '__main__':
	

	conn= sqlite3.connect("googlesearch.db")

	locals_file_path = os.path.split(os.path.realpath(__file__))[0]
	csvfiles =[ file for file in os.listdir(locals_file_path) if '.csv' in file]
	for csvfile in csvfiles:
		googlesearch = pd.read_csv(csvfile).T
		names= googlesearch.iloc[0].tolist()
		googlesearch.columns =names
		df =googlesearch.drop(googlesearch.index[:1])
		df.index.name='Date'
		
		for name in names:
			daf=df.pop(name)
			daf =daf.reset_index()
			daf.columns=['Date','GoogleSeaerch']
			
			
        	for datenumber in xrange(len(daf['Date'])):
            	temp =daf['Date'][datenumber].split('-')
            	date_replace = temp[0]+temp[1]+temp[2]
            	daf.set_value(datenumber,'Date',date_replace)
        	try:
				daf.to_sql(name, conn, if_exists='append', index=False)
			except Exception as e:
				pass
				

		conn.commit()
		
