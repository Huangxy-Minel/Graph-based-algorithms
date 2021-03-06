import random,time,fib_base_list
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
        print("请输入边的数目(最大为",N*(N-1)/2,"):")
        str = input()
        E = int(str)
        if E<N*(N-1):
             max_edge =E
        else:
            print('error')
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
        extra_edge = max_edge
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
            t = random.randint(1,10)
            mat[edge[i][0]][edge[i][1]] = t
            mat[edge[i][1]][edge[i][0]] = t
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

    def Prim(self):
        edge = self.get_all_edges()
        node = self.get_all_nodes()
        element = defaultdict(list)
        for start,stop,weight in edge:
            element[start].append((weight,start,stop))
            element[stop].append((weight,stop,start))
        used_nodes = []
        usable_edges = []
        all_nodes = node
        used_nodes.append(node[0])  #维护已在树上的结点
        usable_edges = element[node[0]][:] #维护树上节点所连的边
        heapify(usable_edges) #建立最小堆

        MST = []
        while usable_edges and len(all_nodes) - len(used_nodes):
            weight, start, stop = heappop(usable_edges)
            if stop not in used_nodes:
                used_nodes.append(stop)
                MST.append((start, stop, weight))
                for member in element[stop]:
                    if member[2] not in used_nodes:
                        heappush(usable_edges, member)
        return MST

    def Prim_fib(self):
        edge = self.get_all_edges()
        node = self.get_all_nodes()
        element = defaultdict(list)
        for start,stop,weight in edge:
            element[start].append([weight,start,stop])
            #element[stop].append([weight,stop,start])
        used_nodes = []
        usable_edges = []
        all_nodes = node
        used_nodes.append(node[0])  #维护已在树上的结点
        usable_edges = element[node[0]][:] #维护树上节点所连的边
        FIB = fib_base_list.FibonacciHeap()
        for i in usable_edges:
            FIB.fib_heap_insert_key(i)#建立最小堆

        MST = []
        while usable_edges and len(all_nodes) - len(used_nodes):
           # weight, start, stop = FIB.fib_heap_extract_min()
            fib_node = FIB.fib_heap_extract_min()
            temp_edge = fib_node.key
            if temp_edge[2] not in used_nodes:
                used_nodes.append(temp_edge[2])
                MST.append([temp_edge[1],temp_edge[2],temp_edge[0]])
                for member in element[temp_edge[2]]:
                    if member[2] not in used_nodes:
                        FIB.fib_heap_insert_key(member)
        return MST

    def merge_sort(list = []):
        if len(list) <= 1:
            return list
        middle = len(list)/2
        left = merge_sort(list[:middle])
        right = merge_sort(list[middle:])
        return merge(left,right)
    def merge(left,right):
        i,j = 0,0
        result = []
        while i< len(left) and j< len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    #使用unionn_find实现kruskal算法
    def find_father(self,x): #寻找每个集合的leader
        if self.k_fat[x]!=x:
            return self.find_father(self.k_fat[x])
        else:
            return x
    def unionn(self,x,y): #将y加入集合x
        self.k_fat[self.find_father(y)] = self.find_father(x)

    def Kruskal(self):
        edges = self.get_all_edges()
        nodes = self.get_all_nodes()
        self.k_fat = defaultdict(list) #记录每个集体的leader
        res = []
        edges.sort(key=lambda a:a[2]) #对边进行排序
        for i in range(len(nodes)):
            self.k_fat[i] = i
        for edge in edges:
            if self.find_father(edge[0]) != self.find_father(edge[1]):
                self.unionn(edge[0],edge[1])
                res.append(edge)
        return res

MyGraph = GraphAL.RandomGraph()
MyGraph.show_list()
start1 = time.time()
MST = MyGraph.Prim_fib()
end1 = time.time()
print('Prim算法：')
for i in MST:
    print(i[0],'<-->',i[1])
#start2 = time.time()
#MST = MyGraph.Kruskal()
#end2 = time.time()
#print('Kruskal算法：')
#for i in MST:
#    print(i[0],'<-->',i[1])
#print('Prim算法执行时间：',end1-start1)
#print('Kruskal算法执行时间：',end2-start2)
#print('Kruskal-Prim算法执行时间之差：',end2-start2-end1+start1)