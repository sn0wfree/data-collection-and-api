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
	

	#conn= sqlite3.connect("googlesearch.db")
	t_file=''

	locals_file_path = os.path.split(os.path.realpath(t_file))[0]
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
			daf.columns=['Date','%s'%name]
			
			
				

		conn.commit()