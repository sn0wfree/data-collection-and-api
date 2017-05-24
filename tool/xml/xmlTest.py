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


import xml.sax as SC


#----------------------------

class HandlerXMLFile:

    def __init__(self, xml_file_address):
        self.filename = xml_file_address
        self.root = []
        self.xml_file = []

    def find_nodes(self,  path):
        '''查找某个路径匹配的所有节点
        tree: xml树
        path: 节点路径'''

        return self.xml_file.findall(path)

    def HanderXMLElementTree(self):
        try:
            xml_file = ET.parse(self.filename)  # 打开xml文档
            root = xml_file.getroot()  # 获得root节点
            # root = ET.fromstring(xml_file_address)
        except Exception, e:
            print "Error:cannot parse file: %s (ElementTree)." % self.filename
            sys.exit(1)
        return (root, xml_file)

    def HanderXMLSAX(self):
        try:
            xml_file = SC.make_parser(self.filename)  # 打开xml文档
            root = xml_file.getroot()  # 获得root节点
            # root = ET.fromstring(xml_file_address)
        except Exception, e:
            print "Error:cannot parse file: %s (sax/default)." % self.filename
            sys.exit(1)
        return (root, xml_file)

    def load_XML_file(self, method='pandas'):
        if method == 'ElementTree':
            (self.root, self.xml_file) = self.HanderXMLElementTree()

        elif method == "pandas":
            excelhandler = ExcelXMLHandler()
            SC.parse(self.filename, excelhandler)
            dataframe = pd.DataFrame(excelHandler.tables[0][
                                     4:], colums=excelHandler.tables[0][3])

            return dataframe

        elif method == 'sax' or method == 'default':

            (self.root, self.xml_file) = self.HanderXMLSAX()
        else:
            print "Error:unknown method."
            sys.exit(1)


class ExcelXMLHandler(SC.ContentHandler):

    def __init__(self):
        self.chars = []
        self.cells = []
        self.rows = []
        self.tables = []

    def characters(self, content):
        self.chars.append(content)

    def startElement(self, name, atts):
        if name == "Cell":
            self.chars = []
        elif name == "Row":
            self.cells = []
        elif name == "Table":
            self.rows = []

    def endElement(self, name):
        if name == "Cell":
            self.chars.append(self.chars)
        elif name == "Row":
            self.cells.append(self.cells)
        elif name == "Table":
            self.rows.append(self.rows)


if __name__ == '__main__':

    xml_file_address = '/Users/sn0wfree/Desktop/2010_2017students.xml'

    xmlfiletree = ET.ElementTree(file=xml_file_address)
    root = xmlfiletree.getroot()
    print [childroot.tag, childroot.tag for childroot in root]


'''

    xmls = HandlerXMLFile(xml_file_address)
    xmls.load_XML_file(method='ElementTree')
    (root, xml_file) = (xmls.root, xmls.xml_file)

    fileinfomration = [(childroot.tag, childroot.attrib) for childroot in root]
    Worksheets = [info[-1]
                  for info in fileinfomration if "{urn:schemas-microsoft-com:office:spreadsheet}Worksheet" in info[0]]

    Worksheet_name = [Worksheet['{urn:schemas-microsoft-com:office:spreadsheet}Name']
                      for Worksheet in Worksheets if '{urn:schemas-microsoft-com:office:spreadsheet}Name' in Worksheet.keys()]

    print Worksheet_name
    print xmls.find_nodes('Worksheet ss: Name="2010_2017students"')
'''
