#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 14:45:15 2021

@author: kirchnerj
"""
#     return time_vec_list, W_vec_v1, W_vec_s1 , prms , mats , vec_v1 , vec_s1 , vec_rl

import numpy as np
import pylab as plt
from tools.runSimulation import runSimulation
from sklearn.linear_model import LinearRegression

time_vec_list, W_vec_v1, W_vec_s1 , prms , mats , vec_v1 , vec_s1 , vec_rl = np.load('simulations/mature_s1/2021-08-23 15:30:55.260155_0.82783/simOutput_0.24039.npy',allow_pickle=True)
##
plt.figure()
plt.subplot(1,2,1)
plt.imshow(W_vec_v1[-1])
plt.subplot(1,2,2)
plt.imshow(W_vec_s1[-1])
plt.show()
##
mats = dict()
mats['W_v1'] = W_vec_v1[-1]
mats['W_s1'] = W_vec_s1[-1]
##
prms["Hebbflag"] = 0
prms["total_ms"] = 6000
prms['store_points'] = prms["total_ms"]
##
time_vec_list, W_vec_v1, W_vec_s1 , prms , mats , vec_v1 , vec_s1 , vec_rl = runSimulation(prms , mats)
##
X , y = np.array(vec_rl).squeeze(), np.array(vec_v1).squeeze()
delID = np.where(X.sum(axis=1) == 0)[0]
X = np.delete(X , delID , 0)
y = np.delete(y , delID , 0)
reg = LinearRegression().fit(X,y)
print(reg.score(X,y))

