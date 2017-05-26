import xmltable2csv


xml_file_address = '/Users/sn0wfree/Desktop/2010_2017students.xml'
#xml_file_address = '/Users/sn0wfree/Desktop/Workbook1.xml'


xmltable2csv.xmltable2csv(input_file=xml_file_address,
                          output_file='/Users/sn0wfree/Desktop/Workbook1.csv').convert()
