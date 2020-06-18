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


freqs = [9000000000,10001250000,11002500000,12000000000,13001250000,14002500000]

for freq in freqs:

    # NEARFIELD
    basename = "../data/freq/%d"%freq
    
    filename = basename + "-freq.csv"
    data = np.loadtxt(filename,delimiter=",",skiprows=1)
    
    X = data[:,1]
    Y = data[:,2]
    Real = data[:,4]
    Imag = data[:,5]
    Z = Real + (1j *Imag)
    N = 28
    
    
    xyz = sorted(zip(X,Y,Z), key=lambda x: x[-2::-1])
    #xyz.sort(key=lambda x: x[-2::-1]) # sort only on the first two entries 
    
    X_n, Y_n, Z_n = [np.array(_).reshape(N, N) for _ in zip(*xyz)]
    
    intensity = 20*np.log10(np.abs(Z_n)/np.max(np.abs(Z)))
    plt.contourf(X_n, Y_n,intensity)
    cbar = plt.colorbar()
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('normalised intensity (dB)', rotation=270)
    plt.savefig(basename + "near-intensity.jpg",dpi=300)
    plt.show()
    
    plt.contourf(X_n,Y_n,np.angle(Z_n))
    plt.colorbar()
    plt.savefig(basename + "near-phase.jpg",dpi=300)
    plt.show()
    
    #FARFIELD
    basename = "../data/out/XY-%d-5000-5000-200-results"%freq
    
    filename = basename + ".csv"
    
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
    
    intensity = 20*np.log10(np.abs(Z_n)/np.max(np.abs(Z)))
    plt.contourf(X_n, Y_n,intensity)
    cbar = plt.colorbar()
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('normalised intensity (dB)', rotation=270)
    plt.savefig(basename + "-intensity.jpg",dpi=300)
    plt.show()
    
    plt.contourf(X_n,Y_n,np.angle(Z_n))
    plt.colorbar()
    plt.savefig(basename + "-phase.jpg",dpi=300)
    plt.show()
