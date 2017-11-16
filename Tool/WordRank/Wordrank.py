# -*- coding: utf-8 -*-
# Copyright by Lin Lu 2017
#-------------------------------------------------------------------------
import sys

import numpy as np


class SqlConnection():

    def __init__(self,  password, database, host='localhost', databasetype='sqlite'):
        self.databasetype = databasetype
        self.conn = self.connect_db(host, password, database)

    def connect_db(self,  password, database, host='localhost', port=3306, user='root'):
        '''
        1.Sqlite
        2.mysql


        '''
        if self.databasetype == 'sqlite':
            import sqlite3
            if host == 'localhost':
                target = raw_input(
                    'type in the sqlite file loaction:(default will use memory varsion)')
            elif '.' in host and len(host.split('.')[-1]) >= 2:
                target = host
            else:
                target = 'default'

            if target != 'default':
                try:
                    conn = sqlite3.connect(target)
                except Exception, e:
                    print e
                    sys.exit()
            else:
                conn = sqlite3.connect(":memory:")
            return conn

        elif self.databasetype == 'mysql':
            import pymysql
            try:
                conn = pymysql.connect(host=host,
                                       port=port,
                                       user='user',
                                       password=password,
                                       database=database,
                                       charset='utf8mb4',
                                       cursorclass=pymysql.cursors.DictCursor)
                return conn
            except Exception, e:
                print e
                sys.exit()
        elif

    def CollectedTableName(self:
        # collect the name of table
        cur = conn.cursor()
        cur.execute(
            "select name from sqlite_master where type='table' order by name")
        return [table[0].encode("utf-8") for table in cur.fetchall()]


if __name__ == '__main__':

    n = np.array([0, 0, 0])
    # 连接数据库
    host = '35.190.136.123'
    password = '19920815'
    database = 'wordrank'
    conn = SqlConnection(host, password, database)
