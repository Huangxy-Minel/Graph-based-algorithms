#此代码仅用于测试 测试程序 用  效率很低
#from Graph import GraphAL
class Packge:
    def __init__(self,id = 0,i = 0,j = 0,N = 0,inday = 0):
        self.Id = id
        self.i = i                  #i,j代表包裹在第i行第j列
        self.j = j
        self.Local = "%04d" % (i*N+j)
        self.Inday = inday
        self.flag = 0               #0代表货柜为空

    def getId(self):
        return self.Id

    def getI(self):
        return int(self.i)

    def getJ(self):
        return int(self.j)

    def getLocal(self):
        return self.Local

    def getInday(self):
        return self.Inday

    def getflag(self):
        return self.flag

    def addflag(self):
        self.flag = 1

    def setflag(self):
        self.flag = 0

class Testee:
    def __init__(self,size):
        self.size = size
        self.panum = 0
        self.allpa = []
        self.N = int(size ** 0.5)+1
        if self.N < 10:
            self.N = 10
        for i in range(self.N):
            temp = []
            for j in range(self.N):
                temppa = Packge(0,0,0,0,0)
                temp.append(temppa)
            self.allpa.append(temp)             #初始化存储空间

        self.idx = [0,0]
        self.start = [0,0]         #定义入口
        self.inpackage_t = 0
        self.outpackage_t = 0
        self.clepackage_t = 0  #初始化放件、取件、清柜时间
        self.day = 0
        self.tag = [0,0]
        #mat = []
        #for i in range(self.N):         #建立N*N的图结构
        #    for j in range(self.N):
        #        temp = []
        #        if j-1 >= 0:
        #            temp.append((i*self.N+j-1,1))
        #        if j+1 < self.N:
        #            temp.append((i*self.N+j+1,1))
        #        if i < self.N-1:
        #            temp.append((i*self.N+j+self.N,1))
        #        if i > 0:
        #            temp.append((i*self.N-self.N+j,1))
        #        mat.append(temp)
        #self.MyGraph = GraphAL(mat,0)

        #self.matrix = [[0 for i in range(self.N)] for i in range(self.N)] #建立二维数组用于遍历/标记存储位置是否已满
    def addpa(self,id,day):
        self.idx = self.FindEmptynode()        
        self.inpackage_t += self.pathweight() 
        self.start = self.idx
        newpa = Packge(id,self.idx[0],self.idx[1],self.N,day)
        local = newpa.getLocal()
        newpa.addflag()
        self.allpa[self.idx[0]][self.idx[1]] = newpa
        self.panum = self.panum + 1
        return local

    def inPackges(self,day,Ids):
        locals = []
        for id in Ids:
            locals.append(self.addpa(id,day))
        #self.countPackge(day)
        self.start = [0,0]
        return locals

    def outPackge(self,local):
        id = 0
        temp = int(local)
        self.idx[0] = int(temp / self.N)
        self.idx[1] = int(temp % self.N)
        self.outpackage_t += self.pathweight() #取一次件所用权重和
        temppa = self.allpa[self.idx[0]][self.idx[1]]
        if temppa.getLocal() == local and temppa.getflag() == 1:
            id = temppa.getId()
            temppa.setflag()
            self.panum = self.panum - 1
        return id

    def clearPackge(self,day):
        ids = []
        for i in range(self.N):
            for j in range(self.N):
                if self.allpa[i][j].getInday() + 7 == day and self.allpa[i][j].getflag() == 1:
                    temppa = self.allpa[i][j] 
                    self.idx[0] = temppa.getI()
                    self.idx[1] = temppa.getJ()
                    self.clepackage_t += self.pathweight()
                    temppa.setflag()
                    self.start = self.idx
                    ids.append(temppa.getId())
        self.start = [0,0]
        return ids


    def countPackge(self,day):
        count = 0
        for i in range(len(self.allpa)):            
            if self.allpa[i].getflag() == 0:
                count = count + 1
        print("在第%d天有最大包裹数为%d" % (day,count))

    def FindEmptynode(self):
        i = self.tag[0]
        j = self.tag[1]
        if self.allpa[i][j].getflag() == 0:
            if j+1 == self.N and i+1 == self.N:
                self.tag[1] = 0
                self.tag[0] = 0
            elif j+1 == self.N:
                self.tag[1] = 0
                self.tag[0] += 1
            else:
                self.tag[1] += 1
            return [i,j]
        else:
            for j1 in range(j,self.N):
                if self.allpa[i][j1].getflag() == 0:
                    if j1+1 == self.N and i+1 == self.N:
                        self.tag[1] = 0
                        self.tag[0] = 0
                    elif j1+1 == self.N:
                        self.tag[1] = 0
                        self.tag[0] += 1
                    else:
                        self.tag[1] = j1+1
                    return [i,j1]
            if i+1 == self.N:
                i=0
            else:
                i += 1
            for i1 in range(i,self.N):
                for j1 in range(self.N):
                    if self.allpa[i1][j1].getflag() == 0:
                        if j1+1 == self.N and i1+1 == self.N:
                            self.tag[1] = 0
                            self.tag[0] = 0
                        elif j1+1 == self.N:
                            self.tag[1] = 0
                            self.tag[0] = i1+1
                        else:
                            self.tag[1] = j1+1
                            self.tag[0] = i1
                        return [i1,j1]
            for i1 in range(i):
                for j1 in range(self.N):
                    if self.allpa[i1][j1].getflag() == 0:
                        if j1+1 == self.N and i1+1 == self.N:
                            self.tag[1] = 0
                            self.tag[0] = 0
                        elif j1+1 == self.N:
                            self.tag[1] = 0
                            self.tag[0] = i1+1
                        else:
                            self.tag[1] = j1+1
                            self.tag[0] = i1
                        return [i1,j1]

                


    def pathweight(self): 
        i1 = int(self.idx[0])
        i2 = int(self.start[0])
        j1 = int(self.idx[1])
        j2 = int(self.start[1])
        weight = abs(i1-i2)+abs(j1-j2)
        return weight

    def PrintAlltime(self):
        print('上货仿真总时间：',self.inpackage_t)
        print('取货仿真总时间：',self.outpackage_t)
        print('清货仿真总时间：',self.clepackage_t)