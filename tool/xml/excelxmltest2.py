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
import sys
import pandas as pd
from linkedlist import *

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

    xml_file_address = '/Users/sn0wfree/Desktop/2010_2017students.xml'
    'Workbook1.xml'

    xmlfiletree = ET.ElementTree(file=xml_file_address)
    root = xmlfiletree.getroot()

    xmlconstruc = [childroot for childroot in root]
    sheetnames = []

    sheets = read_excel_xml_linkedlist(xml_file_address)

    print sheets

    for sheets in xmlconstruc:

        if type(sheets.attrib) is not dict:
            print type(sheets.attrib)
        else:
            if sheets.attrib.has_key('{urn:schemas-microsoft-com:office:spreadsheet}Name'):
                sheetnames.append(
                    sheets.attrib['{urn:schemas-microsoft-com:office:spreadsheet}Name'])

    print sheetnames
