# coding:utf-8
#
#-------------------
'''
this module is to automatically transform xml to csv
'''
__version__ = "0.1"
__author__ = "sn0wfree"

#-------------------


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import lxml
import sys
import pandas as pd
from linkedlist import *
import xml2csvtest

from bs4 import BeautifulSoup


def read_excel_xml_linkedlist(path):
    file = open(path).read()
    soup = BeautifulSoup(file, 'xml')
    workbook = LinkList()
    for sheet in soup.findAll('Worksheet'):
        sheet_as_Linkedlist = LinkList()

        for row in sheet.findAll('Row'):
            row_as_list = [cell.Data.text for cell in row.findAll('Cell')]
            row_node = Node(tuple(row_as_list))

            sheet_as_Linkedlist.append(row_node)
        workbook.append(Node(sheet_as_Linkedlist))
    return workbook


def read_excel_xml(path):
    file = open(path).read()
    soup = BeautifulSoup(file, 'xml')
    workbook = []
    for sheet in soup.findAll('Worksheet'):
        sheet_as_list = []
        for row in sheet.findAll('Row'):
            row_as_list = []
            for cell in row.findAll('Cell'):
                row_as_list.append(cell.Data.text)
            sheet_as_list.append(row_as_list)
        workbook.append(sheet_as_list)
    return workbook

if __name__ == '__main__':
    #sheets = read_excel_xml_linkedlist(xml_file_address)
    # print sheets

    xml_file_address = '/Users/sn0wfree/Desktop/2010_2017students.xml'
    xml_file_address = '/Users/sn0wfree/Desktop/Workbook1.xml'

    # 导入文件
    xml = lxml.etree.parse(xml_file_address)
    # 获取节点
    root = xml.getroot()
    # 获取属性

    xml2csv(xml_file_address, '/Users/sn0wfree/Desktop/Workbook1.csv')


'''
    xmlfiletree = ET.parse(xml_file_address)
    root = xmlfiletree.getroot()

    childroots = [childroot for childroot in root]



    for childroot in childroots:

        if type(childroot.attrib) is not dict:
            print type(childroot.attrib)
        else:

            # name
            if childroot.attrib.has_key('{urn:schemas-microsoft-com:office:spreadsheet}Name'):
                sheetnames.append(
                    childroot.attrib['{urn:schemas-microsoft-com:office:spreadsheet}Name'])

    print sheetnames
'''
