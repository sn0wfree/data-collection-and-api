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


class DateInfo(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.DateFrame()

    def DateFrame(self):

        self.datelabel = Label(
            self, text='Start Year or Period/Date:')
        self.datelabel.grid(row=1, column=0, sticky=N + S)

        self.dateInput = Entry(self)
        self.dateInput.insert(END, '2004')
        self.dateInput.grid(row=1, column=1, sticky=N + S)

        self.tiplabel = Label(
            self, text='Tip:Date Format: 20040101-20170101 or 2004-2017 or 2004', bd=1, relief=SUNKEN, anchor=W)
        self.tiplabel.grid(row=2, column=0, columnspan=2)


class outputtextInfo(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.outputtextFrame()

    def outputtextFrame(self):

        self.outputText = Text(self, width=50, height=26)
        self.outputText.grid(row=6, column=6, rowspan=6)
        self.outputText.update()


class keywordsInfo(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.keywordsFrame()

    def keywordsFrame(self):
        self.label = Label(self, text='Keywords File path:')
        self.label.grid(row=1, column=0, sticky=N + S)
        self.keywordsInput = Entry(self)

        self.keywordsInput.insert(END, self.detectkeywords())
        self.keywordsInput.grid(row=1, column=1, sticky=N + S)
        self.keywordsbutton = Button(
            self, text='Browse', command=self.browsefilepath)
        self.keywordsbutton.grid(row=1, column=2, sticky=N + S)
        # self.tipkeywordslabel = Label(
        #    self, text='Tip:keywords list will be automatically detected, if not,\nNOT Found will present in the box,\n then you should tick "Browse" to manually locate keywords.txt location ', bd=1, relief=SUNKEN, anchor=W)
        # self.tipkeywordslabel.grid(row=2, column=0, columnspan=3)

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


class OtherInfo(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.OtherFrame()

    def OtherFrame(self):
        self.categorylabel = Label(self, text='Category:')
        self.categorylabel.grid(row=4, column=0, sticky=N + S)
        self.categoryInput = Entry(self)
        self.categoryInput.insert(END, '7')
        self.categoryInput.grid(row=4, column=1, sticky=N + S)

        self.geolabel = Label(self, text='Geography:')
        self.geolabel.grid(row=5, column=0, sticky=N + S)
        self.geoInput = Entry(self)
        self.geoInput.insert(END, 'World-Wide')
        self.geoInput.grid(row=5, column=1, sticky=N + S)


class QuitButtonInfo(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.programstatus = 'Disable'
        self.pack()
        self.QuitButton()

    def QuitButton(self):
        self.getButton = Button(self, text='Go!', command=self.gettext)
        self.getButton.grid(row=6, column=1, ipadx=10, padx=50)
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=6, column=2, ipadx=10, padx=100)

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


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.programstatus = 'Disable'
        self.createWidgets()

    def createWidgets(self):

        self.DateFrame = DateInfo(self)

        self.keywordsFrame = keywordsInfo(self)

        self.other = OtherInfo(self)

        self.goquitbotton = QuitButtonInfo(self)

        self.status = StatusInfo(self)
        self.status.pack(side=BOTTOM, fill=X)

        #self.textBox = outputtextInfo()
        # print self.keywordsFrame.keywordsInput.get()

    def createWidgets2(self):
        self.label = Label(self, text='Start Year or Period/Date:')
        self.label.grid(row=1, column=0, sticky=N + S)

        self.dateInput = Entry(self)
        self.dateInput.insert(END, '2004')
        self.dateInput.grid(row=1, column=1, sticky=N + S)

        self.tiplabel = Label(
            self, text='Tip:Date Format: 20040101-20170101 or 2004-2017 or 2004')
        self.tiplabel.grid(row=2, column=0, columnspan=2)

        # self.tiptext = Text(self, height=2, width=100)
        # self.tiptext.insert(INSERT, "Tip:Date Format: 20040101-20170101")
        # self.tiptext.grid(row=2)

        self.label = Label(self, text='Keywords:')
        self.label.grid(row=3, column=0, sticky=N + S)
        self.keywordsInput = Entry(self)

        self.keywordsInput.insert(END, self.detectkeywords())
        self.keywordsInput.grid(row=3, column=1, sticky=N + S)
        self.keywordsbutton = Button(
            self, text='Browse', command=self.browsefilepath)
        self.keywordsbutton.grid(row=3, column=2, sticky=N + S)

        self.categorylabel = Label(self, text='Category:')
        self.categorylabel.grid(row=4, column=0, sticky=N + S)
        self.categoryInput = Entry(self)
        self.categoryInput.insert(END, '7')
        self.categoryInput.grid(row=4, column=1, sticky=N + S)

        self.geolabel = Label(self, text='Geography:')
        self.geolabel.grid(row=5, column=0, sticky=N + S)
        self.geoInput = Entry(self)
        self.geoInput.insert(END, 'World-Wide')
        self.geoInput.grid(row=5, column=1, sticky=N + S)

        self.getButton = Button(self, text='Go!', command=self.gettext)
        self.getButton.grid(row=6, column=1, ipadx=10, padx=50)
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=6, column=2, ipadx=10, padx=100)

        #print(self.outputText.winfo_width(), self.outputText.winfo_height())

    def gettext(self):
        if self.programstatus == 'Disable':
            self.programstatus = 'Enable'
            text = self.dateInput.get()
            keywords = self.keywordsInput.get()
            geo = self.geoInput.get()
            category = self.categoryInput.get()
            print 'Year:', text
            print 'keywords:', keywords
            print 'Geo:', geo
            print 'Category:', category
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
        self.keywordsInput.delete(0, END)
        filename = tkFileDialog.askopenfilename(
            initialdir=os.path.split(os.path.realpath(__file__))[0])
        self.keywordsInput.insert(END, filename)


class StatusInfo(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.programstatus = 'Disable'
        self.statusinfo()

    def statusinfo(self):
        self.status = Label(self, text='Status:',
                            bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=LEFT)

        self.status1 = Label(self, text='%s' % self.programstatus,
                             bd=1, relief=SUNKEN, anchor=W)
        self.status1.pack(side=LEFT, fill=Y)


if __name__ == '__main__':
    app = Application()
    # 设置窗口标题:
    app.master.title('GoogleTrendsIndex-Download APP(Simple Interface)')

    # 主消息循环:
    app.mainloop()
