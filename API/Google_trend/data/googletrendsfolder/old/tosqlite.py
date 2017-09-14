import pandas as pd
import os
import sqlite3

if __name__ == '__main__':
	

	conn= sqlite3.connect("googlesearch.db")


	locals_file_path = os.path.split(os.path.realpath(__file__))[0]
	csvfile =[ file for file in os.listdir(locals_file_path) if '.csv' in file]
	print csvfile

	googlesearch = pd.read_csv('AAALDRALRALEXALX.csv').T
	names= googlesearch.iloc[0].tolist()
	googlesearch.columns =names
	df =googlesearch.drop(googlesearch.index[:1])
	df.index.name='Date'
	'''
	for name in names:
		daf=df.pop(name)
		daf =daf.reset_index()
		daf.columns=['Date','GoogleSeaerch']
		daf.to_sql(name, conn, if_exists='append', index=False)
	conn.commit()
	'''
