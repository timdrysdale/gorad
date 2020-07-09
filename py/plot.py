#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 01:11:37 2020

@author: tim
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import RegularGridInterpolator
  
freqs = [9000000000,9600000000,9603750000,9607500000,9611250000,10001250000,11002500000,12000000000,13001250000,14002500000,15000000000]
sizes = [5000,2500,2500,2500,2500,5000,5000,5000,5000,5000,5000]

#freqs = [9600000000]
#sizes = [2500]

for freq, size in zip(freqs,sizes):

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
    plt.gcf().gca().set_aspect('equal')
    plt.savefig(basename + "near-intensity.jpg",dpi=300)
    plt.show()
    
    plt.contourf(X_n,Y_n,np.angle(Z_n))
    cbar = plt.colorbar()  
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('phase (rad)', rotation=270)
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.title("%0.2g GHz"%(freq/1e9))
    plt.gcf().gca().set_aspect('equal')
    plt.savefig(basename + "near-phase.jpg",dpi=300)
    plt.show()
    
    #FARFIELD
    basename = "../data/out/XY-%d-5000-%d-200-results"%(freq,size)
    
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
    plt.gcf().gca().set_aspect('equal')
    plt.savefig(basename + "-intensity.jpg",dpi=300)
    plt.show()
    
    phase = np.angle(Z_n)
    plt.contourf(X_n,Y_n, phase) 
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    cbar = plt.colorbar() 
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('phase (rad)', rotation=270)
    plt.gcf().gca().set_aspect('equal')
    plt.title("%0.2g GHz"%(freq/1e9))
    
    r1 = 500
    r2 = 750
    r3 = 1000
    
    draw_circle1 = plt.Circle((0,0), r1,fill=False,ls=":",color="red",lw=2)
    plt.gcf().gca().add_artist(draw_circle1)
    draw_circle2 = plt.Circle((0,0), r2,fill=False,ls="--",color="red",lw=2)
    plt.gcf().gca().add_artist(draw_circle2)   
    draw_circle3 = plt.Circle((0,0), r3,fill=False,ls="-.",color="red",lw=2)
    plt.gcf().gca().add_artist(draw_circle3)   
    
    plt.gcf().gca().set_aspect('equal')
    
    
    plt.savefig(basename + "-phase.jpg",dpi=300) 
    plt.show()
    
    
    f = RegularGridInterpolator((X_n[0,:], Y_n[:,0]), phase)
    
    Phase_c = []
    
    f2 = interpolate.RectBivariateSpline(Y_n[:,0], X_n[0,:], phase)
    
    Theta = np.arange(0,100)/100. * 2 * np.pi
    
 
    pts = np.array([])
    
    

    ph1 = []
    ph2 = []
    ph3 = []
    
    for t in Theta:
        
        X1 = r1 * np.sin(t)
        Y1 = r1 * np.cos(t)
      
        ph1.append(np.squeeze(f2(X1,Y1)))
        
        X2 = r2 * np.sin(t)
        Y2 = r2 * np.cos(t)
      
        ph2.append(np.squeeze(f2(X2,Y2)))    
        
        X3 = r3 * np.sin(t)
        Y3 = r3 * np.cos(t)
      
        ph3.append(np.squeeze(f2(X3,Y3)))  
            
        
    ph1_tidy = np.unwrap(ph1) - ph1[0]
    ph2_tidy = np.unwrap(ph2) - ph2[0]
    ph3_tidy = np.unwrap(ph3) - ph3[0]    
        
    plt.figure()
    
    plt.plot(Theta,ph1_tidy,'k:',label='r = 500mm')
    plt.plot(Theta,ph2_tidy,'k--',label = 'r = 750mm')
    plt.plot(Theta,ph3_tidy,'k-.', label = 'r = 1000mm')
    plt.plot(Theta,Theta,'k-', label = 'ideal')
    plt.legend()
    plt.xlabel("Azimuthal position (rad)")
    plt.ylabel("Phase difference (rad)")
    plt.savefig(basename + "-phase-purity-rings.jpg",dpi=300) 
    plt.show()
    
    mode1 = ph1_tidy / Theta
    mode2 = ph2_tidy / Theta
    mode3 = ph3_tidy / Theta
    
    plt.figure() 
    
    draw_band = plt.Rectangle((0,0.5),2*np.pi,1,fill=True, color="green")
    #plt.gcf().gca().add_artist(draw_band)

    draw_band = plt.Rectangle((0,-1),2*np.pi,1.5,fill=True, color="red",alpha=0.1)
    plt.gcf().gca().add_artist(draw_band)

    draw_band = plt.Rectangle((0,1.5),2*np.pi,1.5,fill=True, color="red",alpha=0.1)
    plt.gcf().gca().add_artist(draw_band)

    
    plt.plot(Theta,mode1,'k:',label='r = 500mm')
    plt.plot(Theta,mode2,'k--',label='r = 750mm')
    plt.plot(Theta,mode3,'k-.',label='r = 1000mm')
    plt.plot([0,2*np.pi],[1,1],'k-', label = 'ideal')
    plt.xlim([0,2*np.pi])
    plt.ylim([-0,2])
    plt.xlabel("Azimuthal position (rad)")
    plt.ylabel("Mode number")
    plt.legend()
    plt.savefig(basename + "-phase-purity-mode.jpg",dpi=300) 
    plt.show()
    
    
        
        
    
