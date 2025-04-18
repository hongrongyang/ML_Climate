


import numpy as np
import pandas as pd

def uniform_generator(a,b,c):
    u = np.random.uniform(low=a, high=b, size=c)
    return u.reshape(-1, 1)

def ev_true(n, k, nn):
    z0 = np.load("data_init/ev_true.npy")
    rand_arr = np.arange(z0.shape[0])
    np.random.shuffle(rand_arr)
    random_ev = z0[rand_arr[0:n]].tolist()
    random_ev =np.array(random_ev)
    t_s, B, soc_a, soc_d = random_ev[:, 0].reshape(-1, 1), random_ev[:, 1].reshape(-1, 1), random_ev[:, 2].reshape(-1, 1), random_ev[:, 3].reshape(-1, 1)
    t_a = uniform_generator(0+k, 1+k, n)
    soc_t = soc_a
    soc_s = soc_d - soc_t
    b = soc_s * B
    time_num = np.array([0+k]*n, dtype=int).reshape(-1, 1)
    node_num = np.array([0+nn]*n, dtype=int).reshape(-1, 1)
    t_charge = b / 15
    z = np.hstack((t_s, B, soc_t, soc_d, t_a, b, time_num, node_num, t_charge))
    np.round(z, 4)
    return z

def ev_true0(n, k, c):
    z0 = np.load("data_init/ev_true.npy")
    rand_arr = np.arange(z0.shape[0])
    np.random.shuffle(rand_arr)
    random_ev = z0[rand_arr[0:n]].tolist()
    random_ev =np.array(random_ev)
    t_s, B, soc_a, soc_d = random_ev[:, 0].reshape(-1, 1), random_ev[:, 1].reshape(-1, 1), random_ev[:, 2].reshape(-1, 1), random_ev[:, 3].reshape(-1, 1)
    t_a = uniform_generator(0+k, 1+k, n)
    soc_t = soc_a
    soc_s = soc_d - soc_t
    b = soc_s * B
    time_num = np.array([0+k]*n, dtype=int).reshape(-1, 1)
    node_num = np.array([0]*n, dtype=int).reshape(-1, 1)
    t_charge = b / 15
    z = np.hstack((t_s, B, soc_t, soc_d, t_a, b, time_num, node_num, t_charge))
    for i in range(n):
        z[:, 7][i] = c
    np.round(z, 4)
    return z
# np.save('./data_init/z31', z31)
# z31 = np.load("data/z13.npy")
# self.cs1 = np.load("data/cs1.npy")
# cs1 = ev_true0(10, 0)
# cs2 = ev_true0(15, 0)
# cs3 = ev_true0(15, 0)
# np.save('./data/cs1', cs1)
# np.save('./data/cs2', cs2)
# np.save('./data/cs3', cs3)
# cs1 = ev_true0(15, 0, 3)
# cs2 = ev_true0(15, 0, 2)

# cs1 = ev_true0(15, 0, 1)
# a = sum(cs1[:, 5])/10
# b = min(cs1[:, 5])
# np.save('./data/cs1.npy',cs1)
# print(a,b)



