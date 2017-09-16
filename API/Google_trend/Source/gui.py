# -*- coding:utf-8 -*-

#-------------------
__version__ = "0.8"
__author__ = "sn0wfree"
'''
This tool is for connecting the Google Trends Service
'''
#-------------------
import os
import platform
from Tkinter import *
import gc
import tkMessageBox
import tkFileDialog
import calendar


# import googletrends


def findoperation():
    OperationSystem = platform.system()
    if OperationSystem is 'Darwin':
        link = '/'
    elif OperationSystem is 'Windows':
        link = '\\'
    else:
        link = '/'
    return link


def get_calendar(locale, fwday):
    # instantiate proper calendar class
    if locale is None:
        return calendar.TextCalendar(fwday)
    else:
        return calendar.LocaleTextCalendar(fwday, locale)


class outputtextInfo(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.outputtextFrame()

    def outputtextFrame(self):

        self.outputText = Text(self, width=50, height=26)
        self.outputText.grid(row=6, column=6, rowspan=6)
        self.outputText.update()

        #    self, text='Tip:keywords list will be automatically detected, if not,\nNOT Found will present in the box,\n then you should tick "Browse" to manually locate keywords.txt location ', bd=1, relief=SUNKEN, anchor=W)
        # self.tipkeywordslabel.grid(row=2, column=0, columnspan=3)


class Application(Tk):

    def __init__(self, parent=None):
        Tk.__init__(self, parent)

        self.programstatus = 'Disable'

        self.Widgets()

    def Widgets(self):

        keyFrame = Frame(self)
        keyFrame.pack(side='left')

        LabelFrame(self, text="This is a LabelFrame").pack()

        menuFrame = Frame(self)
        menuFrame.pack(side='top', fill=X)

        self.KeyInfo(keyFrame)

    def KeyInfo(self, keyFrame):

        self.datelabel = Label(
            keyFrame, text='Start Year or Period/Date:')
        self.datelabel.grid(row=0, column=0)

        self.dateInput = Entry(keyFrame)
        self.dateInput.insert(END, '2004')
        self.dateInput.grid(row=0, column=1)

        # self.tiplabel = Label(
        #    keyFrame, text='Tip:Date Format: 20040101-20170101 or 2004-2017 or 2004', bd=1, relief=SUNKEN)
        #self.tiplabel.grid(row=0, column=2, columnspan=2)

        self.keylabel = Label(keyFrame, text='Keywords:')
        self.keylabel.grid(row=1, column=0)
        self.keywordsInput = Entry(keyFrame)

        self.keywordsInput.insert(END, self.detectkeywords())
        self.keywordsInput.grid(row=1, column=1)
        self.keywordsbutton = Button(
            keyFrame, text='Browse', command=self.browsefilepath)
        self.keywordsbutton.grid(row=1, column=2)

        self.categorylabel = Label(keyFrame, text='Category:')
        self.categorylabel.grid(row=2, column=0)
        self.categoryInput = Entry(keyFrame)
        self.categoryInput.insert(END, '7')
        self.categoryInput.grid(row=2, column=1)
        self.geolabel = Label(keyFrame, text='Geography:')
        self.geolabel.grid(row=3, column=0)
        self.geoInput = Entry(keyFrame)
        self.geoInput.insert(END, 'World-wide')
        self.geoInput.grid(row=3, column=1)

        self.getButton = Button(keyFrame, text='Go!', command=self.gettext)
        self.getButton.grid(row=4, column=0,  ipadx=10)

        self.stopButton = Button(
            keyFrame, text='Stop', command=self.stopprocess)
        self.stopButton.grid(row=4, column=1, ipadx=10)
        self.quitButton = Button(keyFrame, text='Quit', command=self.quit)
        self.quitButton.grid(row=4, column=2,  ipadx=10)

    def stopprocess(self):
        if self.programstatus == 'Disable':
            pass
        elif self.programstatus == 'Enable':
            self.programstatus = 'Disable'
            pass
        else:
            pass

    def gettext(self):
        if self.programstatus == 'Disable':
            self.programstatus = 'Enable'
            text = self.dateInput.get()
            keywords = self.keywordsInput.get()
            geo = self.geoInput.get()
            category = self.categoryInput.get()
            print 'text:', text
            print 'keywords:', keywords
            print 'geo:', geo
            print 'category:', category
        else:
            pass

    def detectkeywords(self):
        locals_file_path = os.path.split(os.path.realpath(__file__))[0]
        link = findoperation()
        target = locals_file_path + link + 'keywords.txt'
        if os.path.isfile(target):
            return target
        else:
            return 'Not found'

    def browsefilepath(self):

        filename = tkFileDialog.askopenfilename(
            initialdir=os.path.split(os.path.realpath(__file__))[0])
        self.keywordsInput.delete(0, END)
        self.keywordsInput.insert(END, filename)


if __name__ == '__main__':
    app = Application()
    # 设置窗口标题:
    app.title('GoogleTrendsIndex-Download APP(Simple Interface)')

    # 主消息循环:
    app.mainloop()
