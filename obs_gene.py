import pandapower.networks as nw
import pandapower as pp
import pandas as pd
import numpy as np
import torch as T
pd.set_option('display.expand_frame_repr', False)
net = pp.networks.case33bw()
# print(net.line)
#31:CS1
#13:CS2
#19:CS3




def obs():
    net = pp.networks.case33bw()
    net1 = net
    pp.create_sgen(net1, 5, p_mw=3)
    net1.line.iloc[9, 6] = 5.6 #cs2
    net1.line.iloc[17, 6] = 4.9 #cs3
    net1.line.iloc[27, 6] = 15.2 #cs1
    obs = []

    origin_p31 = net1.load.iloc[30, 6]
    origin_p13 = net1.load.iloc[12, 6]
    origin_p19 = net1.load.iloc[18, 6]
    for i in range(0, 32):
        net1.load.iloc[i, 6] = net1.load.iloc[i, 6] * 0.9
    net1.load.iloc[30, 6] += 0.225
    net1.load.iloc[12, 6] += 0.225
    net1.load.iloc[18, 6] += 0.225
    pp.runpp(net1)
    
    p31 = net1.load.iloc[30, 6]
    p13 = net1.load.iloc[12, 6]
    p19 = net1.load.iloc[18, 6]
    
    # u = []
    # for i in range(33):
    #    u.append(net1.res_bus.iloc[i, 0])
    # net2 = net1
    # p31 = net1.load.iloc[30, 6] * 500
    # q31 = net1.load.iloc[30, 7] * 5000
    # v31 = net1.res_bus.loc[31, "vm_pu"]
    # p13 = net1.load.iloc[12, 6] * 500
    # q13 = net1.load.iloc[12, 7] * 5000
    # v13 = net1.res_bus.loc[13, "vm_pu"]
    # p19 = net1.load.iloc[18, 6] * 500
    # q19 = net1.load.iloc[18, 7] * 5000
    # v19 = net1.res_bus.loc[19, "vm_pu"]
    load_percentage9 = net1.res_line.iloc[9, 13]
    load_percentage17 = net1.res_line.iloc[17, 13]
    load_percentage27 = net1.res_line.iloc[27, 13]

    obs.append(load_percentage9 * 100)
    obs.append(load_percentage17 * 100)
    obs.append(load_percentage27 * 100)


    obs.append(15)
    obs.append(15)
    obs.append(15)
    obs.append(67.5)
    # obs.append(p31)
    # obs.append(p13)
    # obs.append(p19)
    # obs.append(v31 * 100)
    # obs.append(v13 * 100)
    # obs.append(v19 * 100)
    return obs, net1, origin_p31, origin_p13, origin_p19, p31, p13, p19