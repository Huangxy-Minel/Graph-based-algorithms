import random
import time
import numpy as np
import team3 as team    #此处修改被试
class Packge:
    def __init__(self,id = 0,inday = 0,outday = 0):
        self.Id = id            #快递号
        self.Local = ''         #取货号
        self.Inday = inday      #上货日期
        self.Outday = outday    #取货日期
        if self.Outday >= self.Inday + 7:   #注意，在第七天即会被清货
            self.Clearflag = 1  #会被清货
        else:
            self.Clearflag = 0  #会被取货

    def getId(self):
        return self.Id
    def getLocal(self):
        return self.Local
    def getInday(self):
        return self.Inday
    def getOutday(self):
        return self.Outday
    def getflag(self):
        return self.Clearflag
    def addLocal(self,local):
        self.Local = local

class testPackge:
    def __init__(self):
        self.Daymax =0
        self.Packgenum = 0
        self.Allpackge = []
        self.Errpackge = 0  #记录错误的包裹数
        self.Packgesize = 0 #记录最多同时存在的包裹数

    def addPackge(self,id,inday,outday):
        newpackge = Packge(id,inday,outday)
        self.Packgenum = self.Packgenum + 1
        self.Allpackge.append(newpackge)

    def addError(self):
        self.Errpackge = self.Errpackge + 1

    def findPackgesize(self):
        maxsize = size = len(self.getdayin(1))
        for day in self.getDays()[1:]:
            size = size - len(self.getdayout(day -1)) - len(self.getdayclr(day)) + len(self.getdayin(day))
            if maxsize < size:
                maxsize = size
        self.Packgesize = maxsize


    def newPackges(self,maxday = 30,packgenum = 1000):
        np.random.seed(int(time.time()))
        self.Daymax = maxday
        #Ids = np.arange(packgenum)
        Ids = list(range(packgenum))  #0 - num-1的列表
        np.random.shuffle(Ids)
        p = np.array([0.5,0.1,0.1,0.05,0.05,0.05,0.05,0.1])   #快递每天被取走的概率，最后为被清仓的概率
        for i in range(packgenum):
            inday = random.randint(1,maxday)
            outday = np.random.choice([0,1,2,3,4,5,6,7],p = p.ravel()) + inday
            if outday >= maxday:
                outday = maxday
            self.addPackge(Ids[i],inday,outday)
        self.findPackgesize()

    def adddayLocals(self,day,locals):
        i = 0
        try:
            for p in self.Allpackge:
                if p.getInday() == day:
                    p.addLocal(locals[i])
                    i = i + 1
        except:
            print("第%2d天，上件时取件码数量偏少" % (day))
        if len(locals) != i:
            print("第%2d天，上件时取件码数量偏多" % (day))

    def checkclrIds(self,day,Ids):
        i = 0
        clrpas = self.getdayclr(day)
        clrIds = []
        for p in clrpas:
            if p.getId() not in Ids:
                self.addError()
                print("第%2d天，Id为%04d的包裹未被清理" % (day,p.getId()))
            clrIds.append(p.getId())
        for id in Ids:
            if id not in clrIds:
                print("第%2d天，Id为%04d的包裹被误清理" % (day,id))

    def checkoutId(self,day,Id,realId):
        if Id != realId:
            self.addError()
            print("第%2d天，Id为%04d的包裹被误取成Id为%04d的包裹" % (day,Id,realId))

    def getAllpackge(self):
        return self.Allpackge
    def getPackgesize(self):
        return self.Packgesize
    def getdayin(self,day):
        return [p for p in self.Allpackge if p.getInday() == day]
    def getdayinIds(self,day):
        return [p.getId() for p in self.Allpackge if p.getInday() == day]
    def getdayout(self,day):
        return [p for p in self.Allpackge if p.getOutday() == day and p.getflag() == 0]
    def getdayoutIds(self,day):
        return [p.getId() for p in self.Allpackge if p.getOutday() == day and p.getflag() == 0]
    def getdayoutLocals(self,day):
        return [p.getLocal() for p in self.Allpackge if p.getOutday() == day and p.getflag() == 0]
    def getdayclr(self,day):
        return [p for p in self.Allpackge if p.getInday() ==  day - 7 and p.getflag() == 1]
    def getDays(self):
        return list(range(1,self.Daymax + 1))
    def getPackgenum(self):
        return self.Packgenum
    def showPackge(self,pa):
        for i in range(len(pa)):
            print("第%3d个包裹的id为%04d,取货号为%4s,进入日期为%2d,领取日期为%2d,flag为%2d" % (i+1,pa[i].getId(),pa[i].getLocal(),pa[i].getInday(),pa[i].getOutday(),pa[i].getflag()))
    def showresult(self,clrtime,intime,outtime):
        print("共使用%d个包裹在%d天内进行测试，%d个包裹出现异常，异常率为%2.2f%%\n清货用时%.4f秒，上货用时%.4f秒，取货用时%.4f秒，共用时%.4f秒"  %  (self.Packgenum,self.Daymax,self.Errpackge,self.Errpackge/self.Packgenum*100,clrtime,intime,outtime,clrtime+intime+outtime))


if __name__ == '__main__':
    test = testPackge()
    test.newPackges(30,3000)     #总天数，总包裹数
    team = team.Testee(test.getPackgesize())    #被试实例化
    print("已生成测试集，开始仿真")
    allclrtime = allintime = allouttime = 0
    for day in test.getDays():
        starttime = time.time()
        #清货
        dayIds = team.clearPackge(day)  #清货接口
        test.checkclrIds(day,dayIds)
        clrtime = time.time()
        #上货
        dayIds = test.getdayinIds(day)       
        dayLocals = team.inPackges(day,dayIds)  #上货接口
        test.adddayLocals(day,dayLocals)
        #test.showPackge(test.getdayin(day))
        intime = time.time()
        #取货
        dayIds = test.getdayoutIds(day)     
        dayLocals = test.getdayoutLocals(day)
        for i in range(len(dayIds)):
            id = team.outPackge(dayLocals[i])   #取货接口
            test.checkoutId(day,dayIds[i],id)
        outtime = time.time()
        allclrtime = allclrtime + clrtime - starttime
        allintime = allintime + intime - clrtime
        allouttime = allouttime + outtime - intime
    test.showresult(allclrtime,allintime,allouttime)
    team.PrintAlltime()                         #此处额外显示仿真总时间

'''
版本1.0
在第4行修改被试
在第60行修改每日被领取的概率
在第128行修改总天数和总包裹数
在第129行实例化被试，初始化参数为系统内最多同时存在的包裹数，默认类名为Testee
仿真中每日流程为 清货 -> 上货 -> 取货
清货时若没有包裹需要清理，请返回空列表
提供team4.py作为对测试程序的测试
欢迎反馈bug
dd杜雨衡拼错了package，请大家将错就错好了QAQ
'''
