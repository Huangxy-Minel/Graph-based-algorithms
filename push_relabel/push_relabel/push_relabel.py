from Graph import GraphAL
import random
import Edmonds_Karp
import time
class FlowNode(object):
    def __init__(self, excess, num, height):
        self.num = num
        self.excess = excess
        self.height = height

class PushRelabel(object):
    def __init__(self, start, des, graph):
        self._graph = graph
        self.start = start
        self.des = des
        self.N = len(self._graph._mat)
        mat = []
        for i in range(self.N):            #初始化一个邻接矩阵
            temp = []
            for j in range(self.N):
                temp.append(0)
            mat.append(temp)
        for i in range(len(self._graph._mat)):
            edges = self._graph._mat[i]
            for j in edges:
                mat[i][j[0]] = j[1]
        self.graph_L = GraphAL(mat,0) #剩余网络

        self.flow = 0 #记录最大流
        self.flow_path = [] #记录最大流路径
        self.inv_graph()  #生成反向图self._graph_inv
        self.flow_nodes = self.set_height() #反向BFS设置高度，返回流结点列表
        self.bucket = [] #初始化桶，用于选点操作
        for i in range(2*self.N):  #最多2n个桶
            self.bucket.append([]) #[]代表空桶
        self.bucket_idx = 2*self.N-1 #桶中指针
        

    def inv_graph(self):
        edges = self._graph.get_all_edges()
        edges_inv = []
        mat = []
        N = len(self._graph._mat)
        for i in edges:   #将所有边反向
            temp = [i[1],i[0],i[2]]
            edges_inv.append(temp)
        for i in range(N):            #初始化一个邻接矩阵
            temp = []
            for j in range(N):
                temp.append(0)
            mat.append(temp)
        for i in range(len(edges)):     #将反向的边添加至矩阵中
            mat[edges_inv[i][0]][edges_inv[i][1]] = edges_inv[i][2]
        self._graph_inv = GraphAL(mat,0)
    
    def BFS(self,graph):
        queue = [] #队列，存储结点编号
        queue.append(self.des)
        res = [] #存储最终结点及其高度
        res.append([self.des,0])
        looked = set() #存储已访问结点
        looked.add(self.des)
        i = 1
        while(len(queue)>0):
            temp = queue.pop(0)
            nodes = graph._mat[temp] #nodes记录当前结点的所有邻居
            for neighbor in nodes:
                if neighbor[0] not in looked:
                    queue.append(neighbor[0])
                    looked.add(neighbor[0])
                    for i in range(len(res)):
                        if res[i][0] == temp:
                            height = res[i][1]
                            break
                    res.append([neighbor[0],height+1])
        return res

    def set_height(self):
        queue = self.BFS(self._graph_inv)
        flow_nodes = []
        temp = []
        for i in range(self.N):
            flow_nodes.append(0)
        for i in queue:
            if i[0] == self.start:
                temp.append(FlowNode(999,i[0],self.N))
            else:
                temp.append(FlowNode(0,i[0],i[1]))
        for i in temp:
            idx = i.num
            flow_nodes[idx] = i
        return flow_nodes

    def push_relabel(self):
        start = self.start
        des = self.des
        neighbor_edges = self.graph_L._mat[start]
        edges = []
        flows = []
        for edge in neighbor_edges: #初始化，对源节点进行饱和推送
            if self.flow_nodes[edge[0]] == 0:
                continue
            flow = self.push(start,edge)
            edges.append(edge)
            flows.append(flow)
        self.bucket[self.N] = []  #桶的源节点位置置为空桶
        self.updata_graph_L(edges,start,flows) #更新剩余网络
        #算法正式开始，遍历桶
        while self.bucket_idx >= 0: 
            while self.bucket[self.bucket_idx] != [] and self.bucket[self.bucket_idx] != [des]:#如果扫描到非空桶
                edges = []
                flows = []
                v = self.bucket[self.bucket_idx][0]
                flow_node = self.flow_nodes[v]
                neighbor_edges = self.graph_L._mat[v]
                for edge in neighbor_edges:
                    if flow_node.height == self.flow_nodes[edge[0]].height + 1:
                        flow = self.push(v,edge)
                        edges.append(edge)
                        flows.append(flow)
                        if flow_node.excess == 0:
                            break
                self.updata_graph_L(edges,v,flows) #更新剩余网络
                if flow_node.excess != 0:
                    self.relabel(flow_node)
            self.bucket_idx -= 1

    def updata_graph_L(self,edges,start,flows): #更新剩余网络
        for j in range(len(flows)):
            edge = edges[j]
            flow = flows[j]
            end = edge[0]
            flag = 0
            for i in self.graph_L._mat[start]:
                if i[0] == end:
                    temp = i[1] - flow
                    self.graph_L._mat[start].remove(i)
                    if (temp) != 0: #如果非饱和推送，则添加边
                        self.graph_L._mat[start].insert(0,(end,temp))
                    temp_list = self.graph_L._mat[end]
                    for j in range(len(temp_list)):
                        if temp_list[j][0] == start:
                            weight = temp_list[j][1]
                            self.graph_L._mat[end][j] = (start,flow+weight)
                            flag = 1
                    if flag == 0:
                        self.graph_L._mat[end].insert(0,(start,flow)) #添加增广路
                    break

    def push(self,v,edge):
        if self.flow_nodes[v].excess >= edge[1]: #判断饱和推送还是非饱和推送
            flow = edge[1]
        else:
            flow = self.flow_nodes[v].excess
        self.flow_nodes[v].excess -= flow     #更新结点盈余
        self.flow_nodes[edge[0]].excess += flow
        self.update_bucket(v) #更新桶
        self.update_bucket(edge[0])
        return flow
    
    def relabel(self,v):
        x = v.num
        self.bucket[v.height].remove(x)
        v.height += 1
        self.bucket_idx += 1 #桶指针回溯1
        self.update_bucket(x)


    def update_bucket(self,v):
        flow_node = self.flow_nodes[v]
        excess = flow_node.excess
        if v != 0:
            if excess == 0:
                temp_list = self.bucket[flow_node.height]
                if v in temp_list:
                    self.bucket[flow_node.height].remove(v)
            else:
                temp_list = self.bucket[flow_node.height]
                if v not in temp_list:
                    self.bucket[flow_node.height].append(v)

        
MyGraph = GraphAL.RandomGraph()
MyGraph.show_list()
#mat = []
#N = 6
#edge = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [0, 5], [0, 2], [5, 4], [5, 0], [2, 1]]
#for i in range(N):            #初始化一个邻接矩阵
#    temp = []
#    for j in range(N):
#        temp.append(0)
#    mat.append(temp)
#for i in range(len(edge)):     #将随机生成边添加至矩阵中
#    t = random.randint(1,10)
#    mat[edge[i][0]][edge[i][1]] = t
#MyGraph = GraphAL(mat,0)
max_flow = 0
for i in MyGraph._mat[0]:
    max_flow += i[1]
str = input("请输入终点t，起点为0：")
des = int(str)

a = PushRelabel(0,des,MyGraph)

b = Edmonds_Karp.Edmonds_Karp(0,des,MyGraph)
start1 = time.time()
a.push_relabel()
end1 = time.time()
b.E_K()
end2 = time.time()

print('起点出边总容量为',max_flow)
print('PR最大流为',a.flow_nodes[des].excess)
print('EK最大流为',b.flow)
print('PR运行时间',end1-start1)
print('EK运行时间',end2-end1)
