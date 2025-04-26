import numpy as np
import math

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

