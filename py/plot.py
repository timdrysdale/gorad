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
  
#freqs = [9000000000,9600000000,9603750000,9607500000,9611250000,10001250000,11002500000,12000000000,13001250000,14002500000,15000000000]
#sizes = [5000,2500,2500,2500,2500,5000,5000,5000,5000,5000,5000]

freqs = [9600000000]
sizes = [2500]

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
    plt.gcf().gca().set_aspect('equal')
    plt.savefig(basename + "-phase.jpg",dpi=300)  
    r1 = 500
    r2 = 750
    r3 = 1000
    
    draw_circle1 = plt.Circle((0,0), r1,fill=False,ls=":",color="red",lw=2)
    plt.gcf().gca().add_artist(draw_circle1)
    draw_circle2 = plt.Circle((0,0), r2,fill=False,ls="--",color="red",lw=2)
    plt.gcf().gca().add_artist(draw_circle2)   
    draw_circle3 = plt.Circle((0,0), r3,fill=False,ls="-.",color="red",lw=2)
    plt.gcf().gca().add_artist(draw_circle3)   
    

    
    
    plt.savefig(basename + "-phase-rings.jpg",dpi=300) 
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
    plt.savefig(basename + "-phase-linear.jpg",dpi=300) 
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
    
    
    
    
    t = Theta
    
    p0 = np.mod(t * 0, 2 * np.pi)
    pp1 =  np.mod(t * 1, 2 * np.pi)
    pp2 =  np.mod(t * 2, 2 * np.pi)
    pp3 =  np.mod(t * 3, 2 * np.pi)
    pp4 =  np.mod(t * 4, 2 * np.pi)
    pp5 =  np.mod(t * 5, 2 * np.pi)
    pp6 =  np.mod(t * 6, 2 * np.pi)
    
    
    
    pm1 =  np.mod(t * -1, 2 * np.pi)
    pm2 =  np.mod(t * -2, 2 * np.pi)
    pm3 =  np.mod(t * -3, 2 * np.pi)
    pm4 =  np.mod(t * -4, 2 * np.pi)
    pm5 =  np.mod(t * -5, 2 * np.pi)
    pm6 =  np.mod(t * -6, 2 * np.pi)
    
    
    plt.figure()
    plt.plot(t,p0,'o')
    plt.plot(t,pm1,'o')
    plt.plot(t,pm2,'o') 
    plt.plot(t,pp1,'o')
    plt.plot(t,pp2,'o') 
    
    
    m0 = np.exp(1j*p0)
    mp1 = np.exp(1j*pp1)
    mp2 = np.exp(1j*pp2)
    mp3 = np.exp(1j*pp3)
    mp4 = np.exp(1j*pp4)
    mp5 = np.exp(1j*pp5)
    mp6 = np.exp(1j*pp6)
    mm1 = np.exp(1j*pm1)
    mm2 = np.exp(1j*pm2)
    mm3 = np.exp(1j*pm3)
    mm4 = np.exp(1j*pm4)
    mm5 = np.exp(1j*pm5)
    mm6 = np.exp(1j*pm6)
    
    
    
    # calculate the coefficients for each of the modes
    
    ideals = [pm2,pm1,p0,pp1,pp2]
    names = ["-2","-1","0","1","2"]
    
    plt.figure()
    
    for the_phase, n  in zip(ideals,names):
    
        cm6 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm6))/len(t))
        cm5 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm5))/len(t))
        cm4 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm4))/len(t))
        cm3 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm3))/len(t))
        cm2 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm2))/len(t))
        cm1 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm1))/len(t))
        c0 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(m0))/len(t))
        cp1 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp1))/len(t))
        cp2 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp2))/len(t))
        cp3 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp3))/len(t))
        cp4 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp4))/len(t))
        cp5 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp5))/len(t))
        cp6 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp6))/len(t))
        
        
        plt.plot([-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6],20*np.log10([cm6,cm5,cm4,cm3,cm2,cm1,c0,cp1,cp2,cp3,cp4,cp5,cp6]),':o',label='mode =' + n)
    
    plt.legend()
    plt.title('Ideal modes - basis spectrum (power)')
    plt.ylabel('Normalised power (dB)')
    plt.savefig("ideal_modes_basis_spectrum.png",dpi=300)
    plt.show()
    
    plt.figure()
    the_phase = ph1_tidy
    
    cm6 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm6))/len(t))
    cm5 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm5))/len(t))
    cm4 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm4))/len(t))
    cm3 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm3))/len(t))
    cm2 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm2))/len(t))
    cm1 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm1))/len(t))
    c0 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(m0))/len(t))
    cp1 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp1))/len(t))
    cp2 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp2))/len(t))
    cp3 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp3))/len(t))
    cp4 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp4))/len(t))
    cp5 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp5))/len(t))
    cp6 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp6))/len(t))
    
    plt.plot([-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6],[cm6,cm5,cm4,cm3,cm2,cm1,c0,cp1,cp2,cp3,cp4,cp5,cp6],'o')
    plt.ylim([0,1])
    plt.show()
    
    plt.figure()
    plt.plot([-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6],20*np.log10([cm6,cm5,cm4,cm3,cm2,cm1,c0,cp1,cp2,cp3,cp4,cp5,cp6]),':o')
    plt.xlabel('Mode number')
    plt.ylabel('Normalised power (dB)')
    plt.ylim([-35,0])
    plt.savefig("mode-spectra-basis-farfield.png",dpi=300)
    plt.show()
    
    N = len(t)
    plt.figure() 
    Y = np.fft.fftshift(np.fft.fft(np.exp(1j*the_phase)))
    YdB = np.log10(Y**2/np.max(Y**2))
    freq = np.fft.fftshift(np.fft.fftfreq(the_phase.shape[-1])) * N
    plt.plot(freq,YdB,':o')    

    window = 12
    lower = int(N/2) - int(window/2)
    upper = int(N/2) + int(window/2)
    plt.xlim([freq[lower],freq[upper]])    
    plt.ylim([-35,0])  
        
    plt.legend()
    plt.xlabel("Mode number")
    plt.ylabel("Normalised Power (dB)")
    plt.title("Farfield mode spectra - FFT (dB)")
    plt.savefig("mode-spectra-fft-farfield.png",dpi=300)
    
    
    plt.figure()
    the_phase = ph1_tidy
    
    cm6 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm6))/len(t))
    cm5 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm5))/len(t))
    cm4 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm4))/len(t))
    cm3 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm3))/len(t))
    cm2 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm2))/len(t))
    cm1 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm1))/len(t))
    c0 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(m0))/len(t))
    cp1 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp1))/len(t))
    cp2 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp2))/len(t))
    cp3 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp3))/len(t))
    cp4 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp4))/len(t))
    cp5 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp5))/len(t))
    cp6 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp6))/len(t))
    
    
    plt.plot([-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6],[cm6,cm5,cm4,cm3,cm2,cm1,c0,cp1,cp2,cp3,cp4,cp5,cp6],'o')
    plt.ylim([0,1])
    plt.show()
    plt.figure()
    plt.plot([-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6],20*np.log10([cm6,cm5,cm4,cm3,cm2,cm1,c0,cp1,cp2,cp3,cp4,cp5,cp6]),':o')
    plt.show()
    
    plt.figure()
    the_phase = ph2_tidy
    
    cm6 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm6))/len(t))
    cm5 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm5))/len(t))
    cm4 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm4))/len(t))
    cm3 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm3))/len(t))
    cm2 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm2))/len(t))
    cm1 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm1))/len(t))
    c0 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(m0))/len(t))
    cp1 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp1))/len(t))
    cp2 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp2))/len(t))
    cp3 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp3))/len(t))
    cp4 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp4))/len(t))
    cp5 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp5))/len(t))
    cp6 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp6))/len(t))
    
    
    plt.plot([-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6],[cm6,cm5,cm4,cm3,cm2,cm1,c0,cp1,cp2,cp3,cp4,cp5,cp6],'o')
    plt.ylim([0,1])
    plt.show()
    plt.figure()
    plt.plot([-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6],20*np.log10([cm6,cm5,cm4,cm3,cm2,cm1,c0,cp1,cp2,cp3,cp4,cp5,cp6]),':o')
    plt.show()
    
    plt.figure()
    the_phase = ph3_tidy
    
    cm6 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm6))/len(t))
    cm5 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm5))/len(t))
    cm4 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm4))/len(t))
    cm3 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm3))/len(t))
    cm2 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm2))/len(t))
    cm1 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mm1))/len(t))
    c0 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(m0))/len(t))
    cp1 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp1))/len(t))
    cp2 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp2))/len(t))
    cp3 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp3))/len(t))
    cp4 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp4))/len(t))
    cp5 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp5))/len(t))
    cp6 = np.abs(np.sum(np.exp(1j*the_phase)*np.conj(mp6))/len(t))
    
    
    plt.plot([-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6],[cm6,cm5,cm4,cm3,cm2,cm1,c0,cp1,cp2,cp3,cp4,cp5,cp6],'o')
    plt.ylim([0,1])
    plt.show()
    plt.figure()
    plt.plot([-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6],20*np.log10([cm6,cm5,cm4,cm3,cm2,cm1,c0,cp1,cp2,cp3,cp4,cp5,cp6]),':o')
    plt.show()
    
        
    
        
        
    
