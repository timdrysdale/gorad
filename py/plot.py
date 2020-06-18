#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 01:11:37 2020

@author: tim
"""

import numpy as np
import matplotlib.pyplot as plt

freqs = [9000000000,10001250000,11002500000,12000000000,13001250000,14002500000,15000000000]

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
    plt.title("%0.2g GHz"%(freq/1e9))
    plt.savefig(basename + "near-intensity.jpg",dpi=300)
    plt.show()
    
    plt.contourf(X_n,Y_n,np.angle(Z_n))
    cbar = plt.colorbar()  
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('phase (rad)', rotation=270)

    plt.title("%0.2g GHz"%(freq/1e9))
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
    plt.title("%0.2g GHz"%(freq/1e9))
    plt.savefig(basename + "-intensity.jpg",dpi=300)
    plt.show()
    
    plt.contourf(X_n,Y_n,np.angle(Z_n))
    cbar = plt.colorbar() 
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('phase (rad)', rotation=270)
    plt.title("%0.2g GHz"%(freq/1e9))
    plt.savefig(basename + "-phase.jpg",dpi=300) 
    plt.show()
