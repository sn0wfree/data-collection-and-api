#-*- coding:utf-8 -*-

#-------------------
__version__ = "0.2"
__author__ = "sn0wfree"
'''
This tool is for sqlite3 searching
'''
#-------------------
import sqlite3
import os
import platform


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


def FindOperation():
    OperationSystem = platform.system()
    if OperationSystem is 'Darwin':
        link = '/'
    elif OperationSystem is 'Windows':
        link = '\\'
    else:
        link = '/'
    return link
if __name__ == '__main__':
    pass
