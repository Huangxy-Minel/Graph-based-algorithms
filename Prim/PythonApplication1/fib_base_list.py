import math
class FibonacciNode(object):
    def __init__(self, key):
        self.key=key #关键字
        self.degree=0 #元素在堆中的度
        self.parent=0 #指向双亲节点
        self.child=0 #指向第一个孩子节点
        self.left=0 #左向循环指针
        self.right=0 #右向循环指针
        self.marked=False #标记
    

class FibonacciHeap(object):
    def __init__(self):
        self.keyNum = 0 #堆中结点总数
        self.maxDegree = 0 #最大度
        self.minNode = None #最小结点指针

    def fib_node_add(self,node,root):  #将结点添加至根结点左边
        node.left = root.left
        root.left.right = node
        node.right = root
        root.left = node

    def fib_node_remove(self,node): #删除结点
        node.left.right = node.right
        node.right.left = node.left

    def fib_node_cat(self,node_a,node_b): #将双向链表b接到双向链表a的后面
        temp = node_a.right
        node_a.right = node_b.right
        node_b.right.left = node_a
        node_b.right = temp
        temp.left = node_b

    def fib_node_make(self,key): #新建fib_node
        node = FibonacciNode(key)
        node.left = node
        node.right = node
        return node

    def fib_heap_insert_key(self,key): #新建键值为key的节点，并将其插入到斐波那契堆中
        node = self.fib_node_make(key)
        self.fib_heap_insert_node(node)

    def fib_heap_insert_node(self,new_node): #向fib中插入一个结点
        if self.minNode == None:
            self.minNode = new_node
        else:
            self.fib_node_add(new_node,self.minNode)
            if new_node.key[0] < self.minNode.key[0]:
                self.minNode = new_node
        self.keyNum =self.keyNum + 1


    def fib_heap_union(self,h1,h2): #将h1和h2合并成一个堆
        if h1 == None:
            return h2
        if h2 == None:
            return h1 
        if h2.maxDegree > h1.maxDegree: #保证h1的度数大，这样可以尽可能减少操作
            temp = h1
            h1 = h2
            h2 = temp
        if h1.min == None:
            h1.min = h2.min
            h1.keyNum = h2.keyNum

        else:
            self.fib_node_cat(h1.minNode,h2.minNode)
            if h1.minNode.key[0] > h2.minNode.key[0]:
                h1.minNode = h2.minNode
            h1.keyNum += h2.keyNum

        return h1

    def fib_heap_remove_min(self):
        min = self.minNode
        if self.minNode == min.right:
            self.minNode = None
        else:
            self.fib_node_remove(min)
            self.minNode = min.right
        min.left = min.right = min

        return min

    def fib_heap_extract_min(self): #取出最小结点
        if self == None or self.minNode ==None:
            return None
        min = self.minNode
        #将min每一个儿子(儿子和儿子的兄弟)都添加到"斐波那契堆的根链表"中
        while min.child != 0:
            child = min.child
            self.fib_node_remove(child)
            if child.right == child:
                min.child = 0
            else:
                min.child = child.right
            self.fib_node_add(child,self.minNode)
            child.parent = 0
        self.fib_node_remove(min) #将min从根链表移除
        if min.right == min: #如果min是唯一结点，则设置堆的最小结点为None；否则，设置为min.right再调节
            self.minNode = None
        else:
            self.minNode = min.right
            self.fib_heap_consolidate() #合并fib中相同度数的树 
        self.keyNum -= 1

        return min

    def fib_heap_link(self,node,root): #将node链接到root根节点
        if root.child == 0:
            root.child = node
        else:
            self.fib_node_add(node,root.child)

        node.parent = root
        root.degree += 1
        node.marked = 0

    def fib_heap_search(self,key): #在斐波那契堆heap中查找键值为key的节点
        if self == None or self.minNode == None:
            return 0
        return self.fib_node_search(self.minNode,key)

    def fib_node_search(self,root,key): #在最小堆root中查找键值为key的节点
        t = root
        if root == None:
            return root
        while True:
            if t.key[0] == key:
                p = t
                break
            else:
                p = self.fib_node_search(t.child, key)
                if p != 0:
                    break
            t = t.right
            if t != root:
                break
        return p

    def fib_heap_consolidate(self):
        cons = []
        self.maxDegree = int(math.log(self.keyNum,2) + 1)
        D = self.maxDegree
        for i in range(0,self.maxDegree): #分配空间
            cons.append(0)
        while self.minNode != None:
            x = self.fib_heap_remove_min();
            d = x.degree
            while cons[d] != 0:
                y = cons[d]
                if x.key[0] > y.key[0]: #保证x的值比y小
                    temp = x
                    x = y
                    y = temp
                self.fib_heap_link(y,x) #将y链接到x中
                cons[d] = 0
                d+=1

            cons[d] = x
        self.minNode = None
        i=0
        #将cons堆中的结点重新加入根表中
        for i in range(0,D):
            if cons[i] != 0:
                if self.minNode == None:
                    self.minNode = cons[i]
                else:
                    self.fib_node_add(cons[i],self.minNode)
                    if cons[i].key[0] < self.minNode.key[0]:
                        self.minNode = cons[i]
        return 1

    

if __name__ == '__main__':    
    FIB = FibonacciHeap()
    a = [[12,1,2],  [7,2,3], [25,3,4], [15,4,3], [28,3,2], [33,2,1], [41,1,0], [1,0,1]]
    for i in a:
        FIB.fib_heap_insert_key(i)

    for i in range(len(a)):
        node = FIB.fib_heap_extract_min()
        print(node.key)

