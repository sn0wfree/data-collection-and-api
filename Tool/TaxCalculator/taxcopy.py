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
import multiprocessing as mp

import pandas as pd
import xlrd


class TaxCal():

    def __init__(self,  TaxTable, memberdict):
        # initial the class
        # set up the dataset
        self.salaryandbonus = memberdict
        self.salarydiv = 3
        self.initlevel = 0
        self.taxlevel = 0
        self.top = 0

        self.TaxTable = TaxTable
        self.Taxindex = zip(
            list(TaxTable['index_bottom']), list(TaxTable['index_top']))

    def mappingtax(self, salary, bonus, jd=100):
        a = 100 - salary % 100
        tax = self.CalTax(salary + bonus / 3) * 2 + \
            self.CalTax(salary + bonus - bonus / 3 - bonus / 3)
        temp=(bonus / 3, bonus - bonus / 3 - bonus / 3)
        mini = min(temp)
        maxi = max(temp)
        comp = (maxi + salary, salary + bonus - mini - maxi, salary + mini)

        t = int(bonus / 3)
        while a <= t:
            for b in xrange(t, int(bonus - a), jd):
                temp = self.CalTax(a + salary) + self.CalTax(b +
                                                             salary) + self.CalTax(bonus - a - b + salary)
                if temp <= tax:
                    mini = min(a, b, bonus - a - b)
                    maxi = max(a, b, bonus - a - b)
                    if temp < tax:
                        print temp
                        tax = temp
                        comp = (maxi + salary, bonus - maxi -
                                mini + salary, mini + salary)
                    elif temp == tax and mini + salary <= comp[2] and maxi + salary > comp[0]:
                        comp = (maxi + salary, bonus - maxi -
                                mini + salary, mini + salary)
                else:
                    pass
            a += jd
        return [tax, comp[0], comp[1], comp[2]]

    def CalTax(self, wage):
        temp = 'empty'
        taxabelewage = wage - self.initlevel
        for i in xrange(len(self.Taxindex)):
            if self.Taxindex[i][0] <= taxabelewage < self.Taxindex[i][1]:
                # self.taxlevel=list(self.TaxTable[self.TaxTable.index_bottom==self.Taxindex[i][0]]['level'])[0]
                # self.top=list(self.TaxTable[self.TaxTable.index_bottom==self.Taxindex[i][0]]['index_top'])[0]
                TaxRate = list(
                    self.TaxTable[self.TaxTable.index_bottom == self.Taxindex[i][0]]['TaxRate'])[0]
                QuickCalculationDeduction = list(self.TaxTable[
                                                 self.TaxTable.index_bottom == self.Taxindex[i][0]]['QuickCalculationDeduction'])[0]
                # trqcd=self.TaxTable[self.TaxTable.index==self.Taxindex[i]][['TaxRate','QuickCalculationDeduction']]
                temp = 'found taxlevel'
                tax = taxabelewage * TaxRate - QuickCalculationDeduction

                return tax

        if temp == 'empty' and taxabelewage > 80000:
            TaxRate = 0.45
            QuickCalculationDeduction = 13505
            tax = taxabelewage * TaxRate - QuickCalculationDeduction
            temp = 'found taxlevel 7'
            # self.top=100000000
            #self.taxlevel = 7
            return tax
        elif taxabelewage < 0:
            #self.taxlevel = 1
            #self.top = 1500
            return 0
        else:
            print taxabelewage
            raise ValueError, 'UnKnown Value'


def wwe(we):
    temp = list(we)
    temp.extend(tt.mappingtax(we[0], we[1]))
    return temp
if __name__ == '__main__':
    Salary_file = pd.ExcelFile("Salary.xlsx")
    SalaryBonus = Salary_file.parse('Salary+Bonus')
    tt = TaxCal(Salary_file.parse('TaxTable'), 96000)
    print tt.TaxTable

    #salary = 30854.55
    #bonus = 20000
    #tax, (a, b, c) = tt.mappingtax(salary, bonus, 100)
    # print tax, (a, b, c)
    # print tt.CalTax(salary + bonus / 3) * 2 + tt.CalTax(salary + bonus -
    # bonus / 3 - bonus / 3)
    SalaryBonus = Salary_file.parse('Salary+Bonus').set_index('index')
    taxlist = []
    taxdist1 = []
    taxdist2 = []
    taxdist3 = []
    we = [(round(SalaryBonus.iloc[i]['Salary'], 2), round(SalaryBonus.iloc[i]['BonusAmount'], 2))
          for i in xrange(SalaryBonus.shape[0])]

    pool = mp.Pool()
    tabc = pool.map(wwe, set(we))

    pd.DataFrame(tabc).to_csv('output.csv')
