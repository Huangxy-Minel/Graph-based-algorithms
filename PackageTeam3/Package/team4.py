#此代码仅用于测试 测试程序 用  效率很低
class Packge:
    def __init__(self,id = 0,local='',inday = 0):
        self.Id = id
        self.Local = local
        self.Inday = inday
        self.flag = 0

    def getId(self):
        return self.Id

    def getLocal(self):
        return self.Local

    def getInday(self):
        return self.Inday

    def getflag(self):
        return self.flag

    def addflag(self):
        self.flag = 1

class Testee:
    def __init__(self,size):
        self.size = size
        self.panum = 0
        self.allpa = []
        
    def addpa(self,id,day):
        local = "%04d" % id
        newpa = Packge(id,local,day)
        self.allpa.append(newpa)
        self.panum = self.panum + 1
        return local

    def inPackges(self,day,Ids):
        locals = []
        for id in Ids:
            locals.append(self.addpa(id,day))
        #self.countPackge(day)
        return locals

    def outPackge(self,local):
        id = 0
        for i in range(len(self.allpa)):
            if self.allpa[i].getLocal() == local and self.allpa[i].getflag() == 0:
                id = self.allpa[i].getId()
                self.allpa[i].addflag()
                break
        return id

    def clearPackge(self,day):
        ids = []
        for i in range(len(self.allpa)):            
            if self.allpa[i].getInday() + 7 == day and self.allpa[i].getflag() == 0:
                ids.append(self.allpa[i].getId())
                self.allpa[i].addflag()
        return ids

    def countPackge(self,day):
        count = 0
        for i in range(len(self.allpa)):            
            if self.allpa[i].getflag() == 0:
                count = count + 1
        print("在第%d天有最大包裹数为%d" % (day,count))
