# -*- coding:utf-8 -*-

#-------------------
__version__ = "0.8"
__author__ = "sn0wfree"
'''
This tool is for connecting the Google Trends Service
'''
#-------------------
import os
import Tkinter
import gc
import googletrends


class GUItest(Tkinter.Tk):

    def __init__(self, parent):
        self.parent = Tkinter.Tk()

        self.initialize()


class GUI(Tkinter.Tk):

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        menubar = Tkinter.Menu(self)
        menubar.add_command(label="Quit!", command=self.quit)
        self.config(menu=self.menubar)

    def menubar(self):
        menubar = Tkinter.Menu(self)

        # Acount
        #username = str()
        #self.entry_account_username = Tkinter.Entry(self, textvariable=username)
        #self.entry_account_username.grid(column=0, row=1, sticky='EW')
        # self.entry_account_username.setCollectionBehavior

        # Password
        #self.entry_account_passwords = Tkinter.Entry(self)
        #self.entry_account_passwords.grid(column=0, row=2, sticky='EW')
        #self.entry_account_passwords.bind("<Return>", self.OnPressEnter)

        #bottom_account_passwords = Tkinter.Button(self, text=u'done', command=self.OnButtonClick)
        #bottom_account_passwords.grid(column=0, row=3)

        #self.grid_columnconfigure(0, weight=1)
        #self.resizable(True, False)

    def OnButtonClick(self):
        self.OnPressEnter('<Return>')

    def OnPressEnter(self, event):
        print "You clicked the button !"

    #label = Tkinter.Label(self, anchor="w", fg="white", bg="red")
    #label.grid(column=0, row=1, columnspan=2, sticky='EW')

if __name__ == '__main__':
    app = GUI(None)
    app.title('GoogleTrendsSearch APP')

    app.mainloop()
