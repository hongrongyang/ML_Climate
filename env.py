import math
import numpy as np
from decimal import Decimal
import pandapower as pp
from data_gen import ev_true
from obs_gene import obs
import torch as T

inf = float("inf")
CO2_INTENSITY = {
    'coal': 900,
    'gas': 450,
    'nuclear': 12,
    'wind': 0
}


class Graph():
    def __init__(self, n):
        self.vertexn = n
        self.gType = 0
        self.vertexes = [inf] * n
        self.arcs = [self.vertexes * n]  # 邻接矩阵
        self.visited = [False] * n  # 用于深度遍历记录结点的访问情况

    def addvertex(self, v, i):
        self.vertexes[i] = v

    def addarcs(self, row, column, weight):
        self.arcs[row][column] = weight

    # 最短路径算法-Dijkstra 输入点v0，找到所有点到v0的最短距离
    def Dijkstra(self, v0):
        # 初始化操作
        D = [inf] * self.vertexn  # 用于存放从顶点v0到v的最短路径长度
        final = [None] * self.vertexn  # 表示从v0到v的最短路径是否找到最短路径
        for i in range(self.vertexn):
            final[i] = False
            D[i] = self.arcs[v0][i]
        D[v0] = 0
        final[v0] = True
        ###
        for i in range(1, self.vertexn):
            min = inf  # 找到离v0最近的顶点
            for k in range(self.vertexn):
                if (not final[k]) and (D[k] < min):
                    v = k
                    min = D[k]
            final[v] = True  # 最近的点找到，加入到已得最短路径集合S中 此后的min将在处S以外的vertex中产生
            for k in range(self.vertexn):
                if (not final[k]) and (min + self.arcs[v][k] < D[k]):
                    # 如果最短的距离(v0-v)加上v到k的距离小于现存v0到k的距离
                    D[k] = min + self.arcs[v][k]
        return D


# 31:CS1
# 13:CS2
# 19:CS3
class Env():
    def __init__(self):
        # setting parameters
        self.obs, self.net, self.origin_p31, self.origin_p13, self.origin_p19, p31, p13, p19, weighted_system_carbon_intensity = obs()
        self.carbon_intensity = []
        self.carbon_intensity.append(weighted_system_carbon_intensity)
        self.scale = 1000  # 10*1000
        self.t = 1
        self.vc = 0.5
        self.charging_power = 45
        self.electricity_purchase_CS = 0.7
        self.electricity_purchase_MG = 0.5
        self.electricity_purchase_DG = 0.3
        # self.ratio = [0.9, 0.93, 0.95, 0.97, 0.985, 1, 1.05, 1.06, 1.07, 1.03, 1.02, 1, 0.98]  # 长度和self.u一致
        self.ratio = [0.85, 0.87, 0.9, 0.92, 0.94, 0.98, 1, 1.1, 1.05, 1, 0.97, 0.95, 0.92]
        # self.ratio3 = [0.85, 0.87, 0.9, 0.92, 0.94, 0.98, 1, 1.1, 1.05, 1, 0.97, 0.95, 0.92]
        self.u = np.array([0.515, 0.46, 0.625, 0.465, 0.525, 0.425, 0.5, 0.435, 0.48, 0.47, 0.38, 0.465])
        self.m = np.array([0.6, 0.625, 0.49, 0.6, 0.565, 0.47, 0.59, 0.535, 0.425, 0.515, 0.5, 0.4])
        self.s = np.array([0.715, 0.66, 0.825, 0.715, 0.675, 0.525, 0.63, 0.57, 0.595, 0.535, 0.48, 0.465])
        # demand = np.array([8.0, 7.0, 6.0, 5.0, 6.0, 5.0, 6.0, 6.0, 7.0, 6.0, 10.0, 13.0])
        # self.demand = np.array([6, 5, 4, 4, 5, 3, 4, 4, 5, 5, 8, 8]) * 2
        self.demand1 = np.load("./data_init/demand1.npy")
        self.demand2 = np.load("./data_init/demand2.npy")
        self.demand3 = np.load("./data_init/demand3.npy")
        self.demand4 = np.load("./data_init/demand4.npy")
        self.demand5 = np.load("./data_init/demand5.npy")
        self.demand6 = np.load("./data_init/demand6.npy")
        self.demand7 = np.load("./data_init/demand7.npy")
        self.demand8 = np.load("./data_init/demand8.npy")
        self.demand9 = np.load("./data_init/demand9.npy")
        self.demand10 = np.load("./data_init/demand10.npy")
        self.demand11 = np.load("./data_init/demand11.npy")
        self.demand12 = np.load("./data_init/demand12.npy")
        self.demand13 = np.load("./data_init/demand13.npy")
        self.cn1 = 1000
        self.cn2 = 1000
        self.cn3 = 1000
        self.n1 = 15
        self.cs1 = np.load("data_init/cs1.npy")
        self.cs1 = self.cs1.tolist()
        self.n2 = 15
        self.cs2 = np.load("data_init/cs2.npy")
        self.cs2 = self.cs2.tolist()
        self.n3 = 15
        self.cs3 = np.load("data_init/cs3.npy")
        self.cs3 = self.cs3.tolist()

        # output parameters
        self.price1 = [1.25]
        self.price2 = [1.4]
        self.price3 = [1.25]
        self.n_arrival1 = []
        self.n_arrival2 = []
        self.n_arrival3 = []
        self.load_percentage9 = [self.obs[0] / 100]
        self.load_percentage17 = [self.obs[1] / 100]
        self.load_percentage27 = [self.obs[2] / 100]
        self.p31 = [p31]
        self.p13 = [p13]
        self.p19 = [p19]
        # self.v31 = []
        # self.v13 = []
        # self.v19 = []
        self.p_cs1 = [0.225]
        self.p_cs2 = [0.225]
        self.p_cs3 = [0.225]
        self.cs1_profits = [123.75]
        self.cs2_profits = [157.5]
        self.cs3_profits = [123.75]
        self.social_welfare = [675]
        self.reward = 0
        self.cost = 0
        self.congestion_error = 0
        self.voltage_error = 0
        self.total_profits = [337.5]
        self.cs1_total_profits = 0
        self.cs2_total_profits = 0
        self.cs3_total_profits = 0
        self.total_social_welfare = 0
        self.total_n1 = [15]
        self.total_n2 = [15]
        self.total_n3 = [15]
        self.maximize_output = 900  # KW

    def step(self, action):
        done1 = False
        # action
        price1 = action[0]
        price2 = action[1]
        price3 = action[2]
        # price1 = 1.4
        # price2 = 1.4
        # price3 = 1.4

        self.price1.append(price1)
        self.price2.append(price2)
        self.price3.append(price3)

        # EV data_init importing

        z = ev_true(self.demand1[self.t - 1], self.t, 1)
        z = np.vstack((z, ev_true(self.demand2[self.t - 1], self.t, 2)))
        z = np.vstack((z, ev_true(self.demand3[self.t - 1], self.t, 3)))
        z = np.vstack((z, ev_true(self.demand4[self.t - 1], self.t, 4)))
        z = np.vstack((z, ev_true(self.demand5[self.t - 1], self.t, 5)))
        z = np.vstack((z, ev_true(self.demand6[self.t - 1], self.t, 6)))
        z = np.vstack((z, ev_true(self.demand7[self.t - 1], self.t, 7)))
        z = np.vstack((z, ev_true(self.demand8[self.t - 1], self.t, 8)))
        z = np.vstack((z, ev_true(self.demand9[self.t - 1], self.t, 9)))
        z = np.vstack((z, ev_true(self.demand10[self.t - 1], self.t, 10)))
        z = np.vstack((z, ev_true(self.demand11[self.t - 1], self.t, 11)))
        z = np.vstack((z, ev_true(self.demand12[self.t - 1], self.t, 12)))
        z = np.vstack((z, ev_true(self.demand13[self.t - 1], self.t, 13)))
        # charging time: because the rated power of charging pile in each CS is equal, we don't need to considerate the charging time

        demand_number = self.demand1[self.t - 1] + self.demand2[self.t - 1] + self.demand3[self.t - 1] + self.demand4[
            self.t - 1] \
                        + self.demand5[self.t - 1] + self.demand6[self.t - 1] + self.demand7[self.t - 1] + self.demand8[
                            self.t - 1] \
                        + self.demand9[self.t - 1] + self.demand10[self.t - 1] + self.demand11[self.t - 1] + \
                        self.demand12[self.t - 1] + self.demand13[self.t - 1]

        # waiting time
        if self.t == 1:
            t_waiting1 = 0
            t_waiting2 = 0
            t_waiting3 = 0
        else:
            lamda_t = Decimal(demand_number / 3)
            average_S = Decimal(0.806)
            variance_S = Decimal(7.208)
            average_S2 = variance_S + average_S
            a = Decimal(0)
            for i in range(0, self.cn1):
                # print((Decimal(math.factorial(k-1))*Decimal((k-lamda_t*average_S))))
                b = (lamda_t * average_S) ** i / math.factorial(i) + (lamda_t * average_S) ** self.cn1 / (
                            math.factorial(self.cn1 - 1) * (self.cn1 - lamda_t * average_S))
                a = a + b
            t_waiting1 = float((lamda_t ** self.cn1) * (average_S ** (self.cn1 - 1)) * average_S2 / (
                        2 * math.factorial(self.cn1 - 1) * ((self.cn1 - lamda_t * average_S) ** 2) * a))
            if t_waiting1 < 0:
                t_waiting1 = min(self.cs1[:, 8])

            a = Decimal(0)
            for i in range(0, self.cn2):
                # print((Decimal(math.factorial(k-1))*Decimal((k-lamda_t*average_S))))
                b = (lamda_t * average_S) ** i / math.factorial(i) + (lamda_t * average_S) ** self.cn2 / (
                            math.factorial(self.cn2 - 1) * (self.cn2 - lamda_t * average_S))
                a = a + b
            t_waiting2 = float((lamda_t ** self.cn2) * (average_S ** (self.cn2 - 1)) * average_S2 / (
                        2 * math.factorial(self.cn2 - 1) * ((self.cn2 - lamda_t * average_S) ** 2) * a))
            if t_waiting2 < 0:
                t_waiting2 = min(self.cs2[:, 8])

            a = Decimal(0)
            for i in range(0, self.cn3):
                # print((Decimal(math.factorial(k-1))*Decimal((k-lamda_t*average_S))))
                b = (lamda_t * average_S) ** i / math.factorial(i) + (lamda_t * average_S) ** self.cn3 / (
                            math.factorial(self.cn3 - 1) * (self.cn3 - lamda_t * average_S))
                a = a + b
            t_waiting3 = float((lamda_t ** self.cn3) * (average_S ** (self.cn3 - 1)) * average_S2 / (
                        2 * math.factorial(self.cn3 - 1) * ((self.cn3 - lamda_t * average_S) ** 2) * a))
            if t_waiting3 < 0:
                t_waiting3 = min(self.cs3[:, 8])

        # travling time
        v_u0 = 70
        beita_u = 1.726 + 3.15 * (self.u[self.t - 1] ** 3)
        v_u = v_u0 / (1 + self.u[self.t - 1] ** beita_u)

        v_m0 = 50
        beita_m = 1.726 + 3.15 * (self.m[self.t - 1] ** 3)
        v_m = v_m0 / (1 + self.m[self.t - 1] ** beita_m)

        v_s0 = 40
        beita_s = 2.076 + 2.87 * (self.s[self.t - 1] ** 3)
        v_s = v_s0 / (1 + self.s[self.t - 1] ** beita_s)
        t14 = 4.5 / v_u
        t15 = 3.1 / v_u
        t26 = 3.4 / v_u
        t210 = 2.4 / v_s
        t213 = 3.2 / v_u
        t37 = 7.5 / v_u
        t311 = 6.2 / v_m
        t47 = 2.6 / v_u
        t56 = 3.2 / v_u
        t510 = 4.3 / v_s
        t78 = 6.4 / v_m
        t89 = 2.7 / v_m
        t910 = 2.5 / v_s
        t911 = 2.8 / v_m
        t1012 = 4.4 / v_s
        t1112 = 3.1 / v_m
        t1213 = 2.6 / v_m

        g = Graph(13)
        # g.vertexes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]
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
        t_travel1 = []
        t_travel2 = []
        t_travel3 = []

        # for i in range(13):
        #     D = np.array(g.Dijkstra(i))
        #     for h in range(self.demand[self.t-1]):
        #         t_travel1.append(D[0])
        #         t_travel2.append(D[1])
        #         t_travel3.append(D[2])

        D = np.array(g.Dijkstra(0))
        for h in range(self.demand1[self.t - 1]):
            t_travel1.append(D[0])
            t_travel2.append(D[1])
            t_travel3.append(D[2])
        D = np.array(g.Dijkstra(1))
        for h in range(self.demand2[self.t - 1]):
            t_travel1.append(D[0])
            t_travel2.append(D[1])
            t_travel3.append(D[2])
        D = np.array(g.Dijkstra(2))
        for h in range(self.demand3[self.t - 1]):
            t_travel1.append(D[0])
            t_travel2.append(D[1])
            t_travel3.append(D[2])
        D = np.array(g.Dijkstra(3))
        for h in range(self.demand4[self.t - 1]):
            t_travel1.append(D[0])
            t_travel2.append(D[1])
            t_travel3.append(D[2])
        D = np.array(g.Dijkstra(4))
        for h in range(self.demand5[self.t - 1]):
            t_travel1.append(D[0])
            t_travel2.append(D[1])
            t_travel3.append(D[2])
        D = np.array(g.Dijkstra(5))
        for h in range(self.demand6[self.t - 1]):
            t_travel1.append(D[0])
            t_travel2.append(D[1])
            t_travel3.append(D[2])
        D = np.array(g.Dijkstra(6))
        for h in range(self.demand7[self.t - 1]):
            t_travel1.append(D[0])
            t_travel2.append(D[1])
            t_travel3.append(D[2])
        D = np.array(g.Dijkstra(7))
        for h in range(self.demand8[self.t - 1]):
            t_travel1.append(D[0])
            t_travel2.append(D[1])
            t_travel3.append(D[2])
        D = np.array(g.Dijkstra(8))
        for h in range(self.demand9[self.t - 1]):
            t_travel1.append(D[0])
            t_travel2.append(D[1])
            t_travel3.append(D[2])
        D = np.array(g.Dijkstra(9))
        for h in range(self.demand10[self.t - 1]):
            t_travel1.append(D[0])
            t_travel2.append(D[1])
            t_travel3.append(D[2])
        D = np.array(g.Dijkstra(10))
        for h in range(self.demand11[self.t - 1]):
            t_travel1.append(D[0])
            t_travel2.append(D[1])
            t_travel3.append(D[2])
        D = np.array(g.Dijkstra(11))
        for h in range(self.demand12[self.t - 1]):
            t_travel1.append(D[0])
            t_travel2.append(D[1])
            t_travel3.append(D[2])
        D = np.array(g.Dijkstra(12))
        for h in range(self.demand13[self.t - 1]):
            t_travel1.append(D[0])
            t_travel2.append(D[1])
            t_travel3.append(D[2])

        t_total1 = (np.array(t_travel1) * 4 + t_waiting1)
        t_total2 = (np.array(t_travel2) * 4 + t_waiting2)
        t_total3 = (np.array(t_travel3) * 4 + t_waiting3)
        t_min = []
        for i in range(len(t_total1)):
            t_min.append(min(t_total1[i], t_total2[i], t_total3[i]))
        z = np.column_stack((z, t_min, t_total1, t_total2, t_total3, t_travel1, t_travel2, t_travel3))
        z = z[np.argsort(z[:, 9], ), :]
        t_total1 = z[:, 10]
        t_total2 = z[:, 11]
        t_total3 = z[:, 12]
        t_travel1 = z[:, 13]
        t_travel2 = z[:, 14]
        t_travel3 = z[:, 15]
        z = z[:, 0:9]

        # financial cost
        e_m = 0.004 * v_m + 5.492 / v_m - 0.179
        e_travel1 = np.array(t_travel1) * e_m
        e_travel2 = np.array(t_travel2) * e_m
        e_travel3 = np.array(t_travel3) * e_m

        fc1 = (z[:, 5] + e_travel1) * price1
        fc2 = (z[:, 5] + e_travel2) * price2
        fc3 = (z[:, 5] + e_travel3) * price3

        # EV user decision
        c_total1 = self.vc * fc1 + (1 - self.vc) * t_total1 * 15
        c_total2 = self.vc * fc2 + (1 - self.vc) * t_total2 * 15
        c_total3 = self.vc * fc3 + (1 - self.vc) * t_total3 * 15

        # elastic demand
        h = 0

        for k in range(demand_number):
            if min(e_travel1[k], e_travel2[k], e_travel3[k]) > z[k, 1] * z[k, 2]:
                t_total1 = np.delete(t_total1, k - h, axis=0)
                t_total2 = np.delete(t_total2, k - h, axis=0)
                t_total3 = np.delete(t_total3, k - h, axis=0)
                h = h + 1

        c_total = []
        for i in range(demand_number):
            c_total.append(np.argmin([c_total1[i], c_total2[i], c_total3[i]]))
        c_total = np.array(c_total)

        n_arrival1 = 0
        n_arrival2 = 0
        n_arrival3 = 0

        for i in range(len(c_total)):
            if c_total[i] == 0:
                if len(self.cs1) < self.cn1:
                    # print(np.shape(z),np.shape(self.cs1))
                    self.cs1 = np.row_stack((self.cs1, z[i, :]))
                    n_arrival1 = n_arrival1 + 1
            if c_total[i] == 1:
                if len(self.cs2) < self.cn2:
                    self.cs2 = np.row_stack((self.cs2, z[i, :]))
                    n_arrival2 = n_arrival2 + 1
            if c_total[i] == 2:
                if len(self.cs3) < self.cn3:
                    self.cs3 = np.row_stack((self.cs3, z[i, :]))
                    n_arrival3 = n_arrival3 + 1

        self.n_arrival1.append(n_arrival1)
        self.n_arrival2.append(n_arrival2)
        self.n_arrival3.append(n_arrival3)
        self.n1 = self.n1 + n_arrival1
        self.n2 = self.n2 + n_arrival2
        self.n3 = self.n3 + n_arrival3

        # charging process
        # 1.soc_t
        self.cs1[:, 2] = 15 / self.cs1[:, 1] + self.cs1[:, 2]
        self.cs2[:, 2] = 15 / self.cs2[:, 1] + self.cs2[:, 2]
        self.cs3[:, 2] = 15 / self.cs3[:, 1] + self.cs3[:, 2]
        # 2.energy to be charged
        self.cs1[:, 5] = (self.cs1[:, 3] - self.cs1[:, 2]) * self.cs1[:, 1]
        self.cs2[:, 5] = (self.cs2[:, 3] - self.cs2[:, 2]) * self.cs2[:, 1]
        self.cs3[:, 5] = (self.cs3[:, 3] - self.cs3[:, 2]) * self.cs3[:, 1]
        # 3.expected charging time
        self.cs1[:, 8] = self.cs1[:, 5] / 15
        self.cs2[:, 8] = self.cs2[:, 5] / 15
        self.cs3[:, 8] = self.cs3[:, 5] / 15
        # 4.user's estimated pick-up time
        self.cs1[:, 0] = self.cs1[:, 0] + self.cs1[:, 4] - 1
        self.cs2[:, 0] = self.cs2[:, 0] + self.cs2[:, 4] - 1
        self.cs3[:, 0] = self.cs3[:, 0] + self.cs3[:, 4] - 1

        # delete leave car
        leave_CS1 = []
        for i in range(self.n1):
            if self.cs1[:, 2][i] > self.cs1[:, 3][i] or self.cs1[:, 0][i] <= 0:
                leave_CS1.append(i)
        if len(leave_CS1) != 0:
            c = 0
            for i in range(len(leave_CS1)):
                self.cs1 = np.delete(self.cs1, leave_CS1[i] - c, axis=0)
                c = c + 1
        self.n1 = self.n1 - len(leave_CS1)

        leave_CS2 = []
        for i in range(self.n2):
            if self.cs2[:, 2][i] > self.cs2[:, 3][i] or self.cs2[:, 0][i] <= 0:
                leave_CS2.append(i)
        if len(leave_CS2) != 0:
            c = 0
            for i in range(len(leave_CS2)):
                self.cs2 = np.delete(self.cs2, leave_CS2[i] - c, axis=0)
                c = c + 1
        self.n2 = self.n2 - len(leave_CS2)

        leave_CS3 = []
        for i in range(self.n3):
            if self.cs3[:, 2][i] > self.cs3[:, 3][i] or self.cs3[:, 0][i] <= 0:
                leave_CS3.append(i)
        if len(leave_CS3) != 0:
            c = 0
            for i in range(len(leave_CS3)):
                self.cs3 = np.delete(self.cs3, leave_CS3[i] - c, axis=0)
                c = c + 1
        self.n3 = self.n3 - len(leave_CS3)

        # influence on power grid
        if self.t > 1:
            for i in range(0, 12):
                self.net.load.iloc[i, 2] = self.net.load.iloc[i, 2] / self.ratio[self.t - 2] * self.ratio[self.t - 1]
            for i in range(13, 18):
                self.net.load.iloc[i, 2] = self.net.load.iloc[i, 2] / self.ratio[self.t - 2] * self.ratio[self.t - 1]
            for i in range(19, 30):
                self.net.load.iloc[i, 2] = self.net.load.iloc[i, 2] / self.ratio[self.t - 2] * self.ratio[self.t - 1]
            self.net.load.iloc[31, 2] = self.net.load.iloc[31, 2] / self.ratio[self.t - 2] * self.ratio[self.t - 1]

        p_cs1 = 0
        for i in range(self.n1):
            if self.cs1[:, 5][i] < self.charging_power / 4:
                # p_cs1 += self.cs1[:, 5][i] * 4
                p_cs1 += self.cs1[:, 5][i]
            else:
                p_cs1 += self.charging_power
        p_cs1 = p_cs1 / self.scale
        self.p_cs1.append(p_cs1 * self.scale / 1000)
        self.net.load.iloc[30, 2] = self.origin_p31 * self.ratio[self.t - 1] + p_cs1

        p_cs2 = 0
        for i in range(self.n2):
            if self.cs2[:, 5][i] < self.charging_power / 4:
                # p_cs2 += self.cs2[:, 5][i] * 4
                p_cs2 += self.cs2[:, 5][i]
            else:
                p_cs2 += self.charging_power
        p_cs2 = p_cs2 / self.scale
        self.p_cs2.append(p_cs2 * self.scale / 1000)
        self.net.load.iloc[12, 2] = self.origin_p13 * self.ratio[self.t - 1] + p_cs2

        p_cs3 = 0
        for i in range(self.n3):
            if self.cs3[:, 5][i] < self.charging_power / 4:
                # p_cs3 += self.cs3[:, 5][i] * 4
                p_cs3 += self.cs3[:, 5][i]
            else:
                p_cs3 += self.charging_power
        p_cs3 = p_cs3 / self.scale
        self.p_cs3.append(p_cs3 * self.scale / 1000)
        self.net.load.iloc[18, 2] = self.origin_p19 * self.ratio[self.t - 1] + p_cs3

        # Run power flow
        pp.runpp(self.net)

        # Initialize list to store carbon intensities for all nodes
        carbon_intensities = []

        # Get power output from generators, external grid, and static generators
        gen_power = self.net.res_gen.p_mw.values  # Generator active power output
        ext_grid_power = self.net.res_ext_grid.p_mw.values  # External grid active power output
        sgen_power = self.net.res_sgen.p_mw.values if not self.net.res_sgen.empty else [0]  # Static generator output

        # Calculate total injected power
        total_injection = sum(gen_power) + sum(ext_grid_power) + sum(sgen_power)

        # Calculate power contribution ratios for each source (system-wide, for other nodes)
        gen_ratio = np.array(gen_power) / total_injection if sum(gen_power) > 0 else np.array([0])
        ext_grid_ratio = np.array(ext_grid_power) / total_injection if sum(ext_grid_power) > 0 else np.array([0])
        sgen_ratio = np.array(sgen_power) / total_injection if sum(sgen_power) > 0 else np.array([0])

        # Get carbon intensity factors for each source
        gen_carbon = np.array(self.net.gen.co2_intensity.values) if not self.net.gen.empty else np.array([0])
        ext_grid_carbon = np.array(self.net.ext_grid.co2_intensity.values) if not self.net.ext_grid.empty else np.array(
            [0])
        sgen_carbon = np.array([CO2_INTENSITY['coal']]) if not self.net.res_sgen.empty else np.array(
            [0])  # Assume sgen is coal-based

        # Define assumed alpha values for nodes 31, 13, 19 (0-based indices 30, 12, 18)
        # Sources: gen (G), sgen (S), ext_grid (E)
        alpha = np.zeros((len(self.net.bus), 3))  # [alpha_gen, alpha_sgen, alpha_ext_grid] for each node
        # Default: use system-wide ratios for all nodes
        for bus_idx in range(len(self.net.bus)):
            alpha[bus_idx, 0] = gen_ratio[0] if len(gen_ratio) > 0 else 0  # gen
            alpha[bus_idx, 1] = sgen_ratio[0] if len(sgen_ratio) > 0 else 0  # sgen
            alpha[bus_idx, 2] = ext_grid_ratio[0] if len(ext_grid_ratio) > 0 else 0  # ext_grid

        # Override alpha for target nodes (assumed values)
        alpha[30, 1] = 0.7  # Node 31: more from sgen (bus 5, 900 kg CO2/MWh)
        alpha[30, 2] = 0.3  # Node 31: less from ext_grid (bus 0, 700 kg CO2/MWh)
        alpha[12, 1] = 0.2  # Node 13: less from sgen
        alpha[12, 2] = 0.8  # Node 13: more from ext_grid
        alpha[18, 1] = 0.5  # Node 19: balanced
        alpha[18, 2] = 0.5  # Node 19: balanced

        # Compute carbon intensities for all nodes
        source_carbon = np.array([gen_carbon[0] if len(gen_carbon) > 0 else 0,
                                  sgen_carbon[0] if len(sgen_carbon) > 0 else 0,
                                  ext_grid_carbon[0] if len(ext_grid_carbon) > 0 else 0])

        for bus_idx in range(len(self.net.bus)):
            # Explicitly handle bus 0, which has no load (slack bus connected to main grid)
            if bus_idx == 0:
                carbon_intensities.append(0)  # Set to 0 since bus 0 has no load; won't affect weighted CI
                continue
            node_carbon = np.sum(alpha[bus_idx] * source_carbon)
            carbon_intensities.append(node_carbon)

        # Compute weighted system carbon intensity using alpha (via node-specific CI)
        total_load = sum(self.net.load.p_mw.values)
        weighted_system_carbon_intensity = 0

        for load_idx, load_row in self.net.load.iterrows():
            bus_idx = load_row['bus']  # Get the bus number from the load row
            # Map bus number to 0-based index (bus 1 -> index 0 in carbon_intensities)
            carbon_idx = bus_idx  # Since carbon_intensities is indexed by bus number (0 to 32)
            load_fraction = load_row['p_mw'] / total_load if total_load > 0 else 0
            weighted_system_carbon_intensity += load_fraction * carbon_intensities[carbon_idx]

        self.carbon_intensity.append(weighted_system_carbon_intensity)

        load_percentage9 = self.net.res_line.iloc[9, 13]
        load_percentage17 = self.net.res_line.iloc[17, 13]
        load_percentage27 = self.net.res_line.iloc[27, 13]

        p31 = self.net.load.iloc[30, 2] * self.scale / 1000
        p13 = self.net.load.iloc[12, 2] * self.scale / 1000
        p19 = self.net.load.iloc[18, 2] * self.scale / 1000

        self.p31.append(p31)
        self.p13.append(p13)
        self.p19.append(p19)

        self.load_percentage9.append(load_percentage9)
        self.load_percentage17.append(load_percentage17)
        self.load_percentage27.append(load_percentage27)

        # profits calculation
        cs1_profits = 0
        cs2_profits = 0
        cs3_profits = 0
        cs1_revenue = 0
        cs2_revenue = 0
        cs3_revenue = 0

        for i in range(self.n1):
            if self.cs1[:, 5][i] < self.charging_power / 4:
                cs1_revenue += self.cs1[:, 5][i] * self.price1[int(self.cs1[:, 2][i])]
                cs1_profits += self.cs1[:, 5][i] * (self.price1[int(self.cs1[:, 2][i])] - self.electricity_purchase_CS)
            else:
                cs1_revenue += 15 * self.price1[int(self.cs1[:, 2][i])]
                cs1_profits += 15 * (self.price1[int(self.cs1[:, 2][i])] - self.electricity_purchase_CS)
        self.cs1_profits.append(cs1_profits)

        for i in range(self.n2):
            if self.cs2[:, 5][i] < self.charging_power / 4:
                cs2_revenue += self.cs2[:, 5][i] * self.price2[int(self.cs2[:, 2][i])]
                cs2_profits += self.cs2[:, 5][i] * (self.price2[int(self.cs2[:, 2][i])] - self.electricity_purchase_CS)
            else:
                cs2_revenue += 15 * self.price2[int(self.cs2[:, 2][i])]
                cs2_profits += 15 * (self.price2[int(self.cs2[:, 2][i])] - self.electricity_purchase_CS)
        self.cs2_profits.append(cs2_profits)

        for i in range(self.n3):
            if self.cs3[:, 5][i] < self.charging_power / 4:
                cs3_revenue += self.cs3[:, 5][i] * self.price3[int(self.cs3[:, 2][i])]
                cs3_profits += self.cs3[:, 5][i] * (self.price3[int(self.cs3[:, 2][i])] - self.electricity_purchase_CS)
            else:
                cs3_revenue += 15 * self.price3[int(self.cs3[:, 2][i])]
                cs3_profits += 15 * (self.price3[int(self.cs3[:, 2][i])] - self.electricity_purchase_CS)
        self.cs3_profits.append(cs3_profits)

        # social_welfare
        if (p_cs1 + p_cs2 + p_cs3) * self.scale <= self.maximize_output:
            total_cost = (p_cs1 + p_cs2 + p_cs3) * self.scale * self.electricity_purchase_DG
        else:
            total_cost = ((p_cs1 + p_cs2 + p_cs3) * self.scale - self.maximize_output) * self.electricity_purchase_MG \
                         + self.maximize_output * self.electricity_purchase_DG

        social_welfare = cs1_revenue + cs2_revenue + cs3_revenue - total_cost
        self.social_welfare.append(social_welfare)
        # print('r1', cs1_revenue, 'r2', cs2_revenue, 'r3', cs3_revenue, 'tc', total_cost)

        # state
        self.obs = list()
        self.obs.append(load_percentage9 * 100)
        self.obs.append(load_percentage17 * 100)
        self.obs.append(load_percentage27 * 100)

        # self.obs.append(n_arrival1)
        # self.obs.append(n_arrival2)
        # self.obs.append(n_arrival3)
        self.obs.append(self.n1)
        self.obs.append(self.n2)
        self.obs.append(self.n3)
        self.obs.append(social_welfare / 300)
        self.obs.append(weighted_system_carbon_intensity / 300)

        # self.obs.append(p31)
        # self.obs.append(p13)
        # self.obs.append(p19)
        # self.obs.append(v31 * 100)
        # self.obs.append(v13 * 100)
        # self.obs.append(v19 * 100)
        self.obs = np.array(self.obs)

        # reward
        # 1.ongestion cost
        cost1 = 0
        if load_percentage9 >= 0.9:
            cost1 += load_percentage9 - 0.9
        elif load_percentage17 >= 0.9:
            cost1 += load_percentage17 - 0.9
        elif load_percentage27 >= 0.9:
            cost1 += load_percentage27 - 0.9

        if weighted_system_carbon_intensity  > 785:
            cost2 = weighted_system_carbon_intensity - 785
        else:
            cost2 = 0

        reward3 = social_welfare

        self.reward = reward3 / 600

        self.cost = cost1  + cost2/10

        # self.cost =  cost2

        # print("reward", self.reward/600)
        # print("cost1", cost1)
        # print("cost2", cost2)
        # print(weighted_system_carbon_intensity)


        # self.reward = self.rewalrd - self.cost
        self.total_n1.append(self.n1)
        self.total_n2.append(self.n2)
        self.total_n3.append(self.n3)
        self.total_profits.append(cs1_profits + cs2_profits + cs3_profits)

        # finishing condition
        self.t = self.t + 1
        if self.t == 13:
            # self.cs1_total_profits = sum(self.cs1_profits)
            # self.cs2_total_profits = sum(self.cs2_profits)
            # self.cs3_total_profits = sum(self.cs3_profits)
            # self.total_social_welfare = sum(self.social_welfare)

            # np.save('./picture_data/price1', self.price1)
            # np.save('./picture_data/price2', self.price2)
            # np.save('./picture_data/price3', self.price3)
            # np.save('./picture_data/n_arrival1', self.n_arrival1)
            # np.save('./picture_data/n_arrival2', self.n_arrival2)
            # np.save('./picture_data/n_arrival3', self.n_arrival3)
            # np.save('./picture_data/line_per9', self.load_percentage9)
            # np.save('./picture_data/line_per17', self.load_percentage17)
            # np.save('./picture_data/line_per27', self.load_percentage27)
            # np.save('./picture_data/p31', self.p31)
            # np.save('./picture_data/p13', self.p13)
            # np.save('./picture_data/p19', self.p19)
            # np.save('./picture_data/p_cs1', self.p_cs1)
            # np.save('./picture_data/p_cs2', self.p_cs2)
            # np.save('./picture_data/p_cs3', self.p_cs3)
            # np.save('./picture_data/cs1_profits', self.cs1_profits)
            # np.save('./picture_data/cs2_profits', self.cs2_profits)
            # np.save('./picture_data/cs3_profits', self.cs3_profits)
            # np.save('./picture_data/cs_profits', self.total_profits)
            # np.save('./picture_data/social_welfare', self.social_welfare)
            # np.save('./picture_data/total_n1', self.total_n1)
            # np.save('./picture_data/total_n2', self.total_n2)
            # np.save('./picture_data/total_n3', self.total_n3)

            done1 = True
            # print('price1', self.price1)
            # print('price2', self.price2)
            # print('price3', self.price3)
            # print('na1', self.n_arrival1)
            # print('na2', self.n_arrival2)
            # print('na3', self.n_arrival3)
            # print('tn1', self.total_n1)
            # print('tn2', self.total_n2)
            # print('tn3', self.total_n3)
            # print('l9', self.load_percentage9)
            # print('l17', self.load_percentage17)
            # print('l27', self.load_percentage27)
            # print('p31', self.p31)
            # print('p13', self.p13)
            # print('p19', self.p19)
            # print('p_cs1', self.p_cs1)
            # print('p_cs2', self.p_cs2)
            # print('p_cs3', self.p_cs3)
            # print('cs1_profits', self.cs1_profits)
            # print('cs2_profits', self.cs2_profits)
            # print('cs3_profits', self.cs3_profits)
            # print('cs_profits', self.total_profits)
            # print('social_welfare', self.social_welfare)
            # print("carbon_intensities", self.carbon_intensity)

        return self.obs, self.reward, self.cost, done1 \
            # , self.price1, self.price2, self.price3, self.n_arrival1, self.n_arrival2, \
        # self.n_arrival3, self.load_percentage9, self.load_percentage17, self.load_percentage27, self.p31, self.p13,\
        # self.p19, self.p_cs1, self.p_cs2, self.p_cs3, self.cs1_profits, self.cs2_profits, \
        # self.cs3_profits, self.total_profits, self.social_welfare, self.total_n1,\
        # self.total_n2, self.total_n3

    def reset(self):
        # setting parameters
        self.obs, self.net, self.origin_p31, self.origin_p13, self.origin_p19, p31, p13, p19, system_carbon_intensity = obs()
        self.carbon_intensity = []
        self.carbon_intensity.append(system_carbon_intensity)
        self.scale = 1000  # 500*1000
        self.t = 1
        self.vc = 0.5
        self.charging_power = 45
        self.electricity_purchase_CS = 0.7
        self.electricity_purchase_MG = 0.5
        self.electricity_purchase_DG = 0.3
        # self.ratio = [0.9, 0.93, 0.95, 0.97, 0.985, 1, 1.05, 1.06, 1.07, 1.03, 1.02, 1, 0.98]  # 长度和self.u一致
        self.ratio = [0.85, 0.87, 0.9, 0.92, 0.94, 0.98, 1, 1.1, 1.05, 1, 0.97, 0.95, 0.92]
        # self.ratio3 = [0.85, 0.87, 0.9, 0.92, 0.94, 0.98, 1, 1.1, 1.05, 1, 0.97, 0.95, 0.92]
        self.u = np.array([0.515, 0.46, 0.625, 0.465, 0.525, 0.425, 0.5, 0.435, 0.48, 0.47, 0.38, 0.465])
        self.m = np.array([0.6, 0.625, 0.49, 0.6, 0.565, 0.47, 0.59, 0.535, 0.425, 0.515, 0.5, 0.4])
        self.s = np.array([0.715, 0.66, 0.825, 0.715, 0.675, 0.525, 0.63, 0.57, 0.595, 0.535, 0.48, 0.465])
        # demand = np.array([8.0, 7.0, 6.0, 5.0, 6.0, 5.0, 6.0, 6.0, 7.0, 6.0, 10.0, 13.0])
        self.demand1 = np.load("./data_init/demand1.npy")
        self.demand2 = np.load("./data_init/demand2.npy")
        self.demand3 = np.load("./data_init/demand3.npy")
        self.demand4 = np.load("./data_init/demand4.npy")
        self.demand5 = np.load("./data_init/demand5.npy")
        self.demand6 = np.load("./data_init/demand6.npy")
        self.demand7 = np.load("./data_init/demand7.npy")
        self.demand8 = np.load("./data_init/demand8.npy")
        self.demand9 = np.load("./data_init/demand9.npy")
        self.demand10 = np.load("./data_init/demand10.npy")
        self.demand11 = np.load("./data_init/demand11.npy")
        self.demand12 = np.load("./data_init/demand12.npy")
        self.demand13 = np.load("./data_init/demand13.npy")
        self.cn1 = 1000
        self.cn2 = 1000
        self.cn3 = 1000
        self.n1 = 15
        self.cs1 = np.load("data_init/cs1.npy")
        self.cs1 = self.cs1.tolist()
        self.n2 = 15
        self.cs2 = np.load("data_init/cs2.npy")
        self.cs2 = self.cs2.tolist()
        self.n3 = 15
        self.cs3 = np.load("data_init/cs3.npy")
        self.cs3 = self.cs3.tolist()

        # output parameters
        self.price1 = [1.25]
        self.price2 = [1.4]
        self.price3 = [1.25]
        self.n_arrival1 = []
        self.n_arrival2 = []
        self.n_arrival3 = []
        self.load_percentage9 = [self.obs[0] / 100]
        self.load_percentage17 = [self.obs[1] / 100]
        self.load_percentage27 = [self.obs[2] / 100]
        self.p31 = [p31]
        self.p13 = [p13]
        self.p19 = [p19]
        # self.v31 = []
        # self.v13 = []
        # self.v19 = []
        self.p_cs1 = [0.225]
        self.p_cs2 = [0.225]
        self.p_cs3 = [0.225]
        self.cs1_profits = [123.75]
        self.cs2_profits = [157.5]
        self.cs3_profits = [123.75]
        self.social_welfare = [675]
        self.reward = 0
        self.cost = 0
        self.congestion_error = 0
        self.voltage_error = 0
        self.total_profits = [337.5]
        self.cs1_total_profits = 0
        self.cs2_total_profits = 0
        self.cs3_total_profits = 0
        self.total_social_welfare = 0
        self.total_n1 = [15]
        self.total_n2 = [15]
        self.total_n3 = [15]
        self.maximize_output = 900
        return np.array(self.obs)

    def action_sample(self):
        random_action = np.random.random((1, 3)) * 0.6 + 0.9
        return random_action.reshape(-1)

