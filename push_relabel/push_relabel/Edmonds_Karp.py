from Graph import GraphAL

class Edmonds_Karp(object):
    def __init__(self, start, des, graph):
        self._graph = graph
        self.graph_L = graph #剩余网络
        self.start = start
        self.des = des
        self.N = len(self._graph._mat)
        self.flow = 0 #记录最大流
        

    def BFS(self,start,end,graph):
        visited = [] #记录已访问结点
        queue = []
        looked = [] #记录每个结点的先驱结点
        path = [] #记录路径
        queue.append(start)
        visited.append(start)
        looked.append([start,-1])
        while queue:
            v = queue.pop(0)
            for i in self.graph_L._mat[v]:
                if i[0] not in visited:
                    visited.append(i[0])
                    queue.append(i[0])
                    looked.insert(0,[i[0],v])
                if i[0] == end:
                    break
        for i in looked:
            if i[0] == end:
                path.insert(0,end)
                path.insert(0,i[1])
                break
        if path == []:
            return None
        front = i[1]
        while front != start:
            for i in looked:
                if i[0] == front:
                    path.insert(0,i[1])
                    front = i[1]
                    break
        return path

    def E_K(self):
        path = []
        path = self.BFS(self.start,self.des,self.graph_L) #找到s到t的路径(BFS)
        while path != None:
            min_weight = 999
            for i in range(len(path)-1):
                v = path[i]
                w = path[i+1]
                weight = self.graph_L.get_edge(v,w)
                if weight < min_weight: #寻找该路径上最小权重
                    min_weight = weight
                #更新剩余网络
            self.flow += min_weight
            for i in range(len(path)-1):
                v = v = path[i]
                w = path[i+1]
                self.updata_graph_L(w,v,min_weight)
            path = self.BFS(self.start,self.des,self.graph_L) #找到s到t的路径(BFS)


    def updata_graph_L(self,end,start,flow): #更新剩余网络
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
