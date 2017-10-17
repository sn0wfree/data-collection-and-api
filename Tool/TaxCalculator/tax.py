# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
"""
This code is for personal use.

"""
# Copyright by Lin Lu 2017
# version control


__author__ = 'sn0wfree'
__version__ = '0.02'


import datetime

import pandas as pd
import xlrd

# -------------------------------------------------------------------------


class TaxCal():

    def __init__(self,  TaxTable):
        # self.salary = salary
        self.salarydiv = 3
        # self.bonus = bonus

        self.TaxTable = TaxTable
        self.Taxindex = list(set(TaxTable['index']))
        self.Taxindex.sort()

    def CalTax(self, totalwage):
        for num in totalwage:
            pass


if __name__ == '__main__':
    Salary_file = pd.ExcelFile("Salary.xlsx")

    taxtable = Salary_file.parse('TaxTable')
    tt = TaxCal(taxtable)
    print tt.Taxindex
