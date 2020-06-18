#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 01:11:37 2020

@author: tim
"""

import numpy as np
import matplotlib.pyplot as plt



#data/out/XY-10001250000-5000-10000-200-results.csv
#data/out/XY-11002500000-5000-10000-200-results.csv
#data/out/XY-12000000000-5000-10000-200-results.csv
#data/out/XY-13001250000-5000-10000-200-results.csv
#data/out/XY-14002500000-5000-10000-200-results.csv




near = "../data/freq/12000000000-freq.csv"

data = np.loadtxt(near,delimiter=",",skiprows=1)

X = data[:,1]
Y = data[:,2]
Real = data[:,4]
Imag = data[:,5]
Z = Real + (1j *Imag)
N = 28


xyz = sorted(zip(X,Y,Z), key=lambda x: x[-2::-1])
#xyz.sort(key=lambda x: x[-2::-1]) # sort only on the first two entries 

X_n, Y_n, Z_n = [np.array(_).reshape(N, N) for _ in zip(*xyz)]


plt.contourf(X_n, Y_n,20*np.log10(np.abs(Z_n)))
plt.colorbar()
plt.show()

plt.contourf(X_n,Y_n,np.angle(Z_n))
plt.colorbar()
plt.show()


filename1 = "../data/out/XY-9000000000-5000-10000-200-results.csv"
filename2 = "../data/out/XY-10001250000-5000-10000-200-results.csv"
filename3 = "../data/out/XY-11002500000-5000-10000-200-results.csv"
filename4 = "../data/out/XY-12000000000-5000-10000-200-results.csv"
filename5 = "../data/out/XY-13001250000-5000-10000-200-results.csv"
filename6 = "../data/out/XY-14002500000-5000-10000-200-results.csv"

filename = filename2

data = np.loadtxt(filename,delimiter=",",skiprows=1)

X = data[:,1]
Y = data[:,2]
Real = data[:,4]
Imag = data[:,5]
Z = Real + (1j *Imag)
N = 200

xyz = sorted(zip(X,Y,Z), key=lambda x: x[-2::-1])
#xyz.sort(key=lambda x: x[-2::-1]) # sort only on the first two entries 

X_n, Y_n, Z_n = [np.array(_).reshape(N, N) for _ in zip(*xyz)]
plt.contourf(X_n, Y_n,20*np.log10(np.abs(Z_n)))
plt.colorbar()
plt.show()

plt.contourf(X_n,Y_n,np.angle(Z_n))
plt.colorbar()
plt.savefig("test.jpg",dpi=300)
plt.show()
