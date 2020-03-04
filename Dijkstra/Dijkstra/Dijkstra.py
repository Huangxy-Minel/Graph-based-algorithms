import random
import time
from heapq import heapify, heappush, heappop
from collections import defaultdict
class Graph:
    def __init__(self,mat,unconn=0):
        vnum=len(mat)
        for x in mat:
            if len(x)!=vnum:
                raise ValueError("参数错误")
        self._mat=[mat[i][:] for i in range(vnum)]  #做拷贝
        self._unconn=unconn
        self._vnum=vnum
 
    #顶点个数
    def vertex_num(self):
        return self._vnum
 
    #顶点是否无效
    def _invalid(self,v):
        return v<0 or v>=self._vnum
 
    #添加边
    def add_edge(self,vi,vj,val=1):
        if self._invalid(vi) or self._invalid(vj):
            raise ValueError(str(vi)+" or "+str(vj)+"不是有效的顶点")
        self._mat[vi][vj]=val
 
    #获取边的值
    def get_edge(self,vi,vj):
        if self._invalid(vi) or self._invalid(vj):
            raise ValueError(str(vi)+" or "+str(vj)+"不是有效的顶点")
        return self._mat[vi][vj]
 
    #获得一个顶点的各条出边
    def out_edges(self,vi):
        if self._invalid(vi):
            raise ValueError(str(vi)+"不是有效的顶点")
        return self._out_edges(self._mat[vi],self._unconn)
 
    @staticmethod
    def _out_edges(row,unconn):
        edegs=[]
        for i in range(len(row)):
            if row[i]!=unconn:
                edegs.append((i,row[i]))
        return edegs
 
    def __str__(self):
        return "[\n"+",\n".join(map(str,self._mat))+"\n]"+"\nUnconnected: "+str(self._unconn)
class GraphAL(Graph):
    def __init__(self,mat=[],unconn=0):
        vnum = len(mat)
        for x in mat:
            if len(x) != vnum:
               raise ValueError("参数错误")
        self._mat=[Graph._out_edges(mat[i],unconn) for i in range(vnum)]
#       self._mat = mat
        self._unconn = unconn
        self._vnum = vnum
 
    #添加顶点
    #返回该顶点编号
    def add_vertex(self):
        self._mat.append([])
        self._vnum+=1
        return self._vnum-1
 
    #添加边
    def add_edge(self,vi,vj,val=1):
        if self._vnum==0:
            raise ValueError("不能向空图添加边")
        if self._invalid(vi) or self._invalid(vj):
            raise ValueError(str(vi)+" or "+str(vj)+"不是有效的顶点")
 
        row=self._mat[vi]
        i=0
        while i<len(row):
            if row[i][0]==vj:
                self._mat[vi][i]=(vj,val)   #如果原来有到vj的边，修改mat[vi][vj]的值
                return
            if row[i][0]>vj:    #原来没有到vj的边，退出循环后加入边
                break
            i+=1
        self._mat[vi].insert(i,(vj,val))
 
    #获取边的值
    def get_edge(self,vi,vj):
        if self._invalid(vi) or self._invalid(vj):
            raise ValueError(str(vi)+" or "+str(vj)+"不是有效的顶点")
        for i,val in self._mat[vi]:
            if i==vj:
                return val
        return self._unconn
 
    # 获得一个顶点的各条出边
    def out_edges(self,vi):
        if self._invalid(vi):
            raise ValueError(str(vi)+"不是有效的顶点")
        return self._mat[vi]
    # 打印所有临界链表
    def show_list(self):
        for i in range(len(self._mat)):
            for j in range(len(self._mat[i])):
                print(i,'--->',self._mat[i][j][0],'  权重为：',self._mat[i][j][1])
    #生成随机图
    def RandomGraph():
        str = input("请输入顶点个数：")
        N = int(str)
        max_edge = N*(N-1)
        array = []
        edge = []
        if N <= 0:
            print('error')
        else:
            for i in range(N):
                array.append(i)
            random.shuffle(array)
        for i in range(N-1):
            temp = []
            temp.append(array[i])
            temp.append(array[i+1])
            edge.append(temp)
        mat = []
        extra_edge = random.randint(0,max_edge-N+1)
        for i in range(extra_edge): #随机生成边
            random.shuffle(array)
            edge.append([array[0],array[1]])
        print('随机生成的边为：')
        print(edge)
        for i in range(N):            #初始化一个邻接矩阵
            temp = []
            for j in range(N):
                temp.append(0)
            mat.append(temp)
        for i in range(len(edge)):     #将随机生成边添加至矩阵中
            t = random.randint(1,5)
            mat[edge[i][0]][edge[i][1]] = t
        rGraph = GraphAL(mat,0)
        return rGraph

    def get_all_edges(self):
        edge = []
        for i in range(len(self._mat)):
            for j in range(len(self._mat[i])):
                temp = []
                temp.append(i)
                temp.append(self._mat[i][j][0])
                temp.append(self._mat[i][j][1])
                edge.append(temp)
        return edge

    def get_all_nodes(self):
        node = []
        for i in range(len(self._mat)):
            node.append(i)
        return node

    def Dijkstra_cycle(self,s):
        node = self.get_all_nodes()
        nodes = []
        for i in range(len(self._mat)):
            nodes.append([i,999,999])  #初始化链表nodes，存储[结点编号，源节点s到结点权重，最短路径上结点的前1结点]
        X = [] #存储已遍历结点
        nodes[s][1] = 0 #存储到达此结点所耗费总权重
        nodes[s][2] = 999 #存储路径下前置结点
        max_weight = 5 #边的最大权重
        bucket = Bucket(max_weight,node) #建立循环桶
        bucket.update(s,0)
        while len(X) != len(nodes):
            min_node = bucket.Findmin()
            X.append(min_node)
            for i in  range(len(self._mat[min_node])):
                neighbor_node = self._mat[min_node][i][0]
                neighbor_weight = self._mat[min_node][i][1]
                if neighbor_node not in X:
                    if nodes[min_node][1] + neighbor_weight < nodes[neighbor_node][1]:
                        nodes[neighbor_node][1] = nodes[min_node][1] + neighbor_weight
                        nodes[neighbor_node][2] = min_node
                    if nodes[neighbor_node][1] != 999:
                        temp = nodes[neighbor_node][1]%(max_weight+1)
                        bucket.update(neighbor_node,temp) #更新循环桶
        paths = []
        for i in range(len(nodes)):
            temp = []
            j = i
            while nodes[j][2] != s:
                if nodes[j][2] == 999:
                    break
                temp.append(nodes[j][2])
                j = nodes[j][2]
            temp.append(s)
            temp = list(reversed(temp))
            paths.append(temp)
        return [paths,nodes]

    def Dijkstra_heap(self,s):
        edge = self.get_all_edges()
        node = self.get_all_nodes()
        nodes = []
        for i in range(len(self._mat)):
            nodes.append([i,999,999])  #初始化列表nodes，存储[结点编号，源节点s到结点权重，最短路径上结点的前1结点]
        nodes[s][1] = 0 #存储到达此结点所耗费总权重
        nodes[s][2] = 999 #存储路径下前置结点
        usable_nodes = []
        usable_nodes.append([0,s])
        heapify(usable_nodes) #建立最小堆
        X = [] #存储已遍历结点
        while usable_nodes and len(nodes) - len(X):
            A,min_node = heappop(usable_nodes) #FindMin操作
            X.append(min_node)
            for i in  range(len(self._mat[min_node])):
                neighbor_node = self._mat[min_node][i][0]
                neighbor_weight = self._mat[min_node][i][1]
                if neighbor_node not in X:
                    if nodes[min_node][1] + neighbor_weight < nodes[neighbor_node][1]:
                        nodes[neighbor_node][1] = nodes[min_node][1] + neighbor_weight
                        nodes[neighbor_node][2] = min_node
                    if nodes[neighbor_node][1] != 999:
                        temp = [nodes[neighbor_node][1],neighbor_node]
                        idx = []
                        for j in range(len(usable_nodes)): #对堆进行删除操作
                            if usable_nodes[j][1] == temp[1]:
                                idx.append(j)
                        idx = list(reversed(idx))
                        for j in idx:
                            usable_nodes.pop(j)
                        heappush(usable_nodes,temp)       #对堆进行插入操作

        paths = []
        for i in range(len(nodes)):
            temp = []
            j = i
            while nodes[j][2] != s:
                if nodes[j][2] == 999:
                    break
                temp.append(nodes[j][2])
                j = nodes[j][2]
            temp.append(s)
            temp = list(reversed(temp))
            paths.append(temp)
        return [paths,nodes]

class Bucket(object):#循环桶
    def __init__(init,len,V):
        init.bucket = [[] for i in range(len + 1)]    #建立C+1个桶
        init.bucket_recorder = {i:None for i in V}   #记录每个点所在哪个桶，以便减少查询
        init.bucket_point = 0    #遍历指针，以防每次都需从头遍历
        init.min = []   #记录返回最小路径点
    def update(init,i,j):
        if init.bucket_recorder[i] == None:
            init.bucket[j].append(i)    #更新，点是如果不在桶中，加入桶
        else:
            local = init.bucket_recorder[i]      #如果在，则将原来已存在的点弹出，并进行相应的更新
            init.bucket[j].append(i)
            init.bucket[local].remove(i)
        init.bucket_recorder[i] = j
    def Findmin(init):
        if len(init.min) >=1:
            return init.min.pop(0)
        else:
            Local = init.bucket_point
            while init.bucket[init.bucket_point] == []:
                init.bucket_point += 1
                if init.bucket_point == len(init.bucket):
                    init.bucket_point = 0
                if Local == init.bucket_point:
                    return 1
            init.min = init.bucket[init.bucket_point]
            if init.bucket_point == len(init.bucket) - 1:
                init.bucket_point = 0
            else:
                init.bucket_point += 1
            return init.min.pop(0)

if __name__ == '__main__':
    MyGraph = GraphAL.RandomGraph()
    MyGraph.show_list()
    str = input("请输入起点")
    s = int(str)
    start1 = time.time()
    paths1 = MyGraph.Dijkstra_cycle(s)
    end1 = time.time()
    print('循环桶方法得到的路径为：')
    for i in range(len(paths1[0])):
        for j in paths1[0][i]:
            print(j,end='-->')
        print(i,end='   总权重为：')
        print(paths1[1][i][1])
    print('-----------------------------')
    print('堆方法得到的路径为：')
    start2 = time.time()
    paths2 = MyGraph.Dijkstra_heap(s)
    end2 = time.time()
    for i in range(len(paths2[0])):
        for j in paths2[0][i]:
            print(j,end='-->')
        print(i,end='   总权重为：')
        print(paths2[1][i][1])
    temp = 0
    for i in range(len(paths1[0])):
        if paths1[1][i][1] != paths2[1][i][1]:
            print(i,'不相同')
            temp += 1
    print('基于循环桶Dijkstra算法执行时间：',end1-start1)
    print('基于堆Dijkstra算法执行时间：',end2-start2)