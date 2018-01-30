# coding==utf-8
#
import numpy as np
import pandas as pd


class Rule():

    def __init__(self):
        self.rulebox = []
        self.variables = []
        pass

    def addvariable(self, variablename):
        if isinstance(variablename, list):
            self.variables.extend(variablename)
        elif isinstance(variablename, str):
            self.variables.append(variablename)
        else:
            print 'Wrong Variable Name Format! ingore!'
        self.variables = list(set(self.variables))

    def create(self, rulelist):
        if isinstance(rulelist, list):
            for rule in rulelist:
                print rule
        elif


class Cleaner():

    def __init__(self):
        self.Rule = Rule()
        self.Container = Container()
        pass

    def Rule(self):
        pass


class Container():

    def __init__(self, filetype='database'):
        self.c = 0

    def importer(self, filepath, filetype='csv', **kwarg):
        if filetype == 'csv':
            try:
                data = pd.read_csv(filepath)
            except Exception as e:
                print e
                data = pd.read_csv(filepath, encoding='utf-8')
        else:
            raise IOError('Unknow file')


if __name__ == '__main__':
    # dataset
    gender_submission = 'Titanic/Data/gender_submission.csv'
    test = 'Titanic/Data/test.csv'
    train = 'Titanic/Data/train.csv'
    gs = pd.read_csv(gender_submission)
    testdf = pd.read_csv(test)
    traindf = pd.read_csv(train)
    print traindf
