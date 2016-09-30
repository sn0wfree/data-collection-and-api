#coding=utf-8
import os,platform,sys



class get_terminal_bound:

    def __init__(self):
        self.width = None
        self.height = None
    def capture_rowsandcolumns(self):
        rows,columns=os.popen('stty size', 'r').read().split()
        self.width = int(columns)
        self.height = int(rows)
        return (int(rows),int(columns))

class TestPlatform:
    def __init__(self):
        self.python_version = platform.python_version() # Python version
        self.platform_architecture = platform.architecture()#programme structure(’32bit’, ‘WindowsPE’)
        self.node = platform.node() # name
        self.platform_version=platform.version()#  获取操作系统的core版本
        self.platform_name_version = platform.platform()#获取操作系统名称及版本号，Windows-7-6.1.7601-SP1
        self.processor = platform.processor()#计算机处理器信息，’Intel64 Family 6 Model 42 Stepping 7, GenuineIntel’
        self.python_compiler=platform.python_compiler()#  获取系统中python解释器的信息
        self.otherinfo=platform.uname()#  other
        self.platform_system=platform.system()#system
    def UsePlatform(self, returnornot=False):
        sysstr = self.platform_system
        if returnornot:
            return sysstr
        else:
            pass
        #if(sysstr =="Windows"):
        #    return ("Call Windows tasks")
        #elif(sysstr == "Linux"):
        #    print ("Call Linux tasks")
        #elif(sysstr == "Darwin"):
        #     print ("Call Darwin or Mac tasks")
        #else:
        #    print ("Other System tasks")




    #print

    #print platform.system_alias()

    #print












        #return (rows,columns)
    #def get_terminal_width_resize():
    #    c = commands.getoutput('resize').split('\n')
    #    c = [x for x in c if x.startswith('COLUMNS=')]
    #    if c:
    #        c = c[0]
    #        dummy, c = c.split('=', 1)
    #        if c[-1] == ';':
    #            c = c[:-1]
    #    if c:
    #        return int(c)
    #    else:
    #        return None

    #def get_terminal_height():
    #    c = commands.getoutput('resize').split('\n')
    #    c = [x for x in c if x.startswith('LINES=')]

    #    if c:
    #        c = c[0]
    #        dummy, c = c.split('=', 1)
    #        if c[-1] == ';':
    #            c = c[:-1]
    #    if c:
    #        return int(c)
    #    else:
    #        return None

class demo:
    def __init__(self):
        self.name='demo_video'
        rows,columns=os.popen('stty size', 'r').read().split()
        #self.width = 20
        #self.height = 50
        self.width = int(columns)
        self.height = int(rows)
        self.system='Darwin'

    def capture_rowsandcolumns(self, returnout=False):
        rows,columns=os.popen('stty size', 'r').read().split()
        self.width = int(columns)
        self.height = int(rows)
        if returnout:
            return (int(rows),int(columns))
        else:
            pass
    def checkOS(self,returnout=False):
        self.system=platform.system()#system
        if returnout:
            return self.system
        else:
            pass
    def printdash(self):
        length= self.width
        h=self.height
        for x in xrange(h):
            sys.stdout.write ('*'*length)
            sys.stdout.flush()






if __name__=='__main__':
    v=demo()
    a=TestPlatform()
    #print a.platform_system
    v.printdash()
    #print g.height
