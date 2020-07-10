#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:51:44 2020

@author: tim
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt 

if __name__ == "__main__":
    
    N = 360
    
    twopi = 2*np.pi
    
    theta = np.linspace(0,2*np.pi,N) 
    
    m0 = np.mod(theta * 1e-99, twopi)
    mp1 = np.mod(theta * 1, twopi)
    mp2 = np.mod(theta * 2, twopi)
    mm1 = np.mod(theta * -1, twopi)
    mm2 = np.mod(theta * -2, twopi)
        
    modes = [mm2,mm1,m0,mp1,mp2]
    names = ["-2","-1","0","1","2"]

    
    plt.figure()
    for m,n in zip(modes,names):
        plt.plot(theta, m, label = "mode = " + n)  
    plt.legend()
    plt.xlabel("Mode number")
    plt.ylabel("Phase (rad)")
    plt.title("Ideal modes")
    plt.savefig("mode-phase-ideal.png",dpi=300)
    
    plt.figure()
    for m,n in zip(modes,names):

        Y = np.fft.fftshift(np.fft.fft(np.exp(1j * m)))
        YdB = np.log10(Y**2/np.max(Y**2))
        freq = np.fft.fftshift(np.fft.fftfreq(m.shape[-1])) * N
        plt.plot(freq,YdB, label = "mode = " + n)    

        window = 10
        lower = int(N/2) - int(window/2)
        upper = int(N/2) + int(window/2)
        plt.xlim([freq[lower],freq[upper]])    
        plt.ylim([-30,10])  
        
    plt.legend()
    plt.xlabel("Mode number")
    plt.ylabel("Normalised power (dB)")
    plt.title("Ideal modes - FFT (power)")
    plt.savefig("mode-spectra-fft-ideal.png",dpi=300)
    
    plt.figure()
    for m,n in zip(modes,names):

        Y = np.fft.fftshift(np.fft.fft(np.exp(1j * m)))
        freq = np.fft.fftshift(np.fft.fftfreq(m.shape[-1])) * N
        plt.plot(freq,np.angle(Y), label = "mode = " + n)    

        window = 10
        lower = int(N/2) - int(window/2)
        upper = int(N/2) + int(window/2)
        plt.xlim([freq[lower],freq[upper]])    
        plt.ylim([-10,10])  
        
    plt.legend()
    plt.xlabel("Mode number")
    plt.ylabel("Angle (rad)")
    plt.title("Ideal modes - FFT (angle)")
    plt.savefig("mode-spectra-fft-ideal-phase.png",dpi=300)
    
    
    
       
