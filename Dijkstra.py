import numpy as np
import math
'''class Dijkstra:
    def __init__(self, graph, goal):
        self.graph = graph
        self.goal = goal
        self.open_list = {}
        # open_list初始化为一个空字典，keys为节点'1''2'...,values为distance即从'1'到该点的实际代价
        self.closed_list = {}
        # closed_list初始化为一个空字典，键和值与open_list相同
        self.open_list['1'] = 0
        # 因为我们初始节点为'1'，并且'1'到'1'的值为0,将其传入open_list列表中
        self.parent = {'1': None}
        # 初始父节点为字典型，初始键为'1'值为None，其中键是子节点，值是父节点
        self.min_dis = None
        # 初始最短路径长度为None

    def shortest_path(self):

        while True:
            if self.open_list is None:
                print('搜索失败， 结束！')
                break

            distance, min_node = min(zip(self.open_list.values(), self.open_list.keys()))  # 取出距离最小的节点
            self.open_list.pop(min_node)  # 将其从 open_list 中去除

            self.closed_list[min_node] = distance  # 将节点加入 closed_list 中

            if min_node == self.goal:  # 如果节点为终点
                self.min_dis = distance
                shortest_path = [self.goal]  # 记录从终点回溯的路径
                father_node = self.parent[self.goal]
                while father_node != '1':
                    shortest_path.append(father_node)
                    father_node = self.parent[father_node]
                shortest_path.append('1')
                print(shortest_path[::-1])  # 逆序
                print('最短路径的长度为：{}'.format(self.min_dis))
                print('找到最短路径， 结束！')
                return shortest_path[::-1], self.min_dis  # 返回最短路径和最短路径长度

            for node in self.graph[min_node].keys():  # 遍历当前节点的邻接节点
                if node not in self.closed_list.keys():  # 邻接节点不在 closed_list 中
                    if node in self.open_list.keys():  # 如果节点在 open_list 中
                        if self.graph[min_node][node] + distance < self.open_list[node]:
                            self.open_list[node] = distance + self.graph[min_node][node]  # 更新节点的值
                            self.parent[node] = min_node  # 更新继承关系
                    else:  # 如果节点不在 open_list 中
                        self.open_list[node] = distance + self.graph[min_node][node]
                        # 计算节点的值，并加入 open_list 中
                        self.parent[node] = min_node  # 更新继承关系


if __name__ == '__main__':
    g = {'1': {'4': 4.5, '5': 3.1},
         '2': {'6': 3.4, '10': 2.4, '13': 3.2},
         '3': {'7': 7.5, '11': 6.2},
         '4': {'1': 4.5, '7': 2.6},
         '5': {'1': 3.1, '6': 3.2, '10': 4.3},
         '6': {'5': 3.2, '2': 3.4},
         '7': {'4': 2.6, '8': 6.4, '3': 7.5},
         '8': {'7': 6.4, '9': 2.7},
         '9': {'8': 2.7, '10': 2.5, '11': 2.8},
         '10': {'2': 2.4, '5': 4.3, '9': 2.5, '12':4.4},
         '11': {'3': 6.2, '9': 2.8, '12': 3.1},
         '12': {'10': 4.4, '11': 3.1, '13': 2.6},
         '13': {'2': 3.2, '12': 2.6},
         }
    goal = '2'
    dijk1 = Dijkstra(g, goal)
    dijk1.shortest_path()'''
# 邻接矩阵实现无向图 Dijkstra算法
inf = float("inf")

class Graph():
    def __init__(self, n):
        self.vertexn = n
        self.gType = 0
        self.vertexes = [inf]*n
        self.arcs = [self.vertexes*n]  # 邻接矩阵
        self.visited = [False]*n  # 用于深度遍历记录结点的访问情况

    def addvertex(self, v, i):
        self.vertexes[i] = v

    def addarcs(self, row, column, weight):
        self.arcs[row][column] = weight

    # 最短路径算法-Dijkstra 输入点v0，找到所有点到v0的最短距离
    def Dijkstra(self, v0):
        # 初始化操作
        D = [inf]*self.vertexn  # 用于存放从顶点v0到v的最短路径长度
        path = [None]*self.vertexn  # 用于存放从顶点v0到v的路径
        final = [None]*self.vertexn  # 表示从v0到v的最短路径是否找到最短路径
        for i in range(self.vertexn):
            final[i] = False
            D[i] = self.arcs[v0][i]
            path[i] = ""  # 路径先置空
            if D[i] < inf:
                path[i] = self.vertexes[i]  # 如果v0直接连到第i点，则路径直接改为i
        D[v0] = 0
        final[v0] = True
        ###
        for i in range(1, self.vertexn):
            min = inf  # 找到离v0最近的顶点
            for k in range(self.vertexn):
                if(not final[k]) and (D[k] < min):
                    v = k
                    min = D[k]
            final[v] = True  # 最近的点找到，加入到已得最短路径集合S中 此后的min将在处S以外的vertex中产生
            for k in range(self.vertexn):
                if(not final[k]) and (min+self.arcs[v][k] < D[k]):
                    # 如果最短的距离(v0-v)加上v到k的距离小于现存v0到k的距离
                    D[k] = min+self.arcs[v][k]
                    path[k] = path[v]+","+self.vertexes[k]
        return D, path

#(48.37,432.5)
u = np.array([0.515, 0.46, 0.625, 0.465, 0.525, 0.425, 0.5, 0.435, 0.48, 0.47, 0.38, 0.465])
m = np.array([0.6, 0.625, 0.49, 0.6, 0.565, 0.47, 0.59, 0.535, 0.425, 0.515, 0.5, 0.4])
s = np.array([0.715, 0.66, 0.825, 0.715, 0.675, 0.525, 0.63, 0.57, 0.595, 0.535, 0.48, 0.465])
# demand = np.array([8.0, 7.0, 6.0, 5.0, 6.0, 5.0, 6.0, 6.0, 7.0, 6.0, 10.0, 13.0])
demand = np.array([6, 5, 4, 4, 5, 3, 4, 4, 5, 5, 8, 10])
#service_time

i = 0

v_u0 = 70
beita_u = 1.726+3.15*(u[i]**3)
v_u = v_u0 / (1+u[i]**beita_u)

v_m0 = 50
beita_m = 1.726+3.15*(m[i]**3)
v_m = v_m0 / (1+m[i]**beita_m)

v_s0 = 40
beita_s = 2.076+2.87*(s[i]**3)
v_s = v_s0 / (1+s[i]**beita_s)

t14 = 4.5/v_u
t15 = 3.1/v_u
t26 = 3.4/v_u
t210 = 2.4/v_s
t213 = 3.2/v_u
t37 = 7.5/v_u
t311 = 6.2/v_m
t47 = 2.6/v_u
t56 = 3.2/v_u
t510 = 4.3/v_s
t78 = 6.4/v_m
t89 = 2.7/v_m
t910 = 2.5/v_s
t911 = 2.8/v_m
t1012 = 4.4/v_s
t1112 = 3.1/v_m
t1213 = 2.6/v_m

if __name__ == "__main__":
    g = Graph(13)
    g.vertexes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]
    g.arcs = [[0, inf, inf, t14, t15, inf, inf, inf, inf, inf, inf, inf, inf],
              [inf, 0, inf, inf, inf, t26, inf, inf, inf, t210, inf, inf, t213],
              [inf, inf, 0, inf, inf, inf, t37, inf, inf, inf, t311, inf, inf],
              [t14, inf, inf, 0, inf, inf, t47, inf, inf, inf, inf, inf, inf],
              [t15, inf, inf, inf, 0, t56, inf, inf, inf, t510, inf, inf, inf],
              [inf, t26, inf, inf, t56, 0, inf, inf, inf, inf, inf, inf, inf],
              [inf, inf, t37, t47, inf, inf, 0, t78, inf, inf, inf, inf, inf],
              [inf, inf, inf, inf, inf, inf, t78, 0, t89, inf, inf, inf, inf],
              [inf, inf, inf, inf, inf, inf, inf, t89, 0, t910, t911, inf, inf],
              [inf, t210, inf, inf, t510, inf, inf, inf, t910, 0, inf, t1012, inf],
              [inf, inf, t311, inf, inf, inf, inf, inf, t911, inf, 0, t1112, inf],
              [inf, inf, inf, inf, inf, inf, inf, inf, inf, t1012, t1112, 0, t1213],
              [inf, t213, inf, inf, inf, inf, inf, inf, inf, inf, inf, t1213, 0]]

    print("Dijkstra搜索点到图中各点的最短路径:")
    D, path = g.Dijkstra(1)
    D = np.array(D)*60
    print(D)
    print(path)
    print(D[0])

