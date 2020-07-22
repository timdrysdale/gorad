#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:51:44 2020

@author: tim
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt 
from scipy import stats

def get_ideal():
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
    return modes, names    


def show_modes():
    modes, names = get_ideal()
    plt.figure()
    for m,n in zip(modes,names):
        plt.plot(theta, m, label = "mode = " + n)  
    plt.legend()
    plt.xlabel("Mode number")
    plt.ylabel("Phase (rad)")
    plt.title("Ideal modes")
    plt.savefig("mode-phase-ideal.png",dpi=300)
    
    
def show_fft():
    modes, names = get_ideal()
    plt.figure()
    
    N = len(modes[0])
    for m,n in zip(modes,names):

        Y = np.fft.fftshift(np.fft.fft(np.exp(1j * m)))
        YdB = np.log10(Y**2/np.max(Y**2))
        freq = np.fft.fftshift(np.fft.fftfreq(m.shape[-1])) * N
        plt.plot(freq,YdB, ':o',label = "mode = " + n)    

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


def get_basis(biggest_mode, mode_steps, theta_steps):
    modes = []
   
    theta = np.linspace(0,2*np.pi,num=theta_steps)
    
    number = np.linspace(-biggest_mode,biggest_mode,num=mode_steps)
   
    for n in number:
        
        if n == 0:
            m = theta * 0 + 1e-999  #avoid divide by zero
        else:
            m = theta * n
            
        m = np.mod(m, 2 * np.pi)
        
        modes.append(m)
        
    return theta, modes, number     
    
def demo_basis():

    th, bm, bn = get_basis(2,50,360)

    for m,n in zip(bm,bn):
        plt.plot(th, m, label = 'mode = %g'%n)
    
    plt.title("Basis functions example")
    plt.xlabel("Azimuthal angle (rad)")    
    plt.ylabel("Phase (rad)")
    plt.savefig("basis-functions-example.png", dpi = 300)
    
def try_basis():
    modes, names = get_ideal()

    th, bm, bn = get_basis(2,50,360)
    
    
    coeffs = []
    plt.figure()
    for m in modes:
        mc = []
        for b in bm:
            mc.append(np.dot(m,b)/len(th))
        plt.plot(bn,mc)
        coeffs.append(mc)    

    plt.savefig("fractional_basis.png",dpi=300)
         
        
if __name__ == "__main__":

    #show_modes()
    #show_fft()    
    #demo_basis()
    #try_basis()
    #modes, names = get_ideal()
    
    #    modes = [ph1_tidy, ph2_tidy, ph3_tidy]
    #    names = ["500","750","1000"]
    #    
    #    dms = []
    #    
    #    
    #    mode_factor = len(modes[0]) / (2 * np.pi )
    #    
    #    hbins = np.linspace(-10,10,num=100)
    #    
    #    plt.figure(figsize=(6, 4))
    #        
    #    for m,n  in zip(modes, names):
    #        print(n)
    #        dm = np.diff(m) * mode_factor
    #        dms.append(dm)  
    #        #plt.hist(dm,bins=bins,density=True)
    #        #plt.show()
    #        #https://scipy-lectures.org/intro/scipy/auto_examples/plot_normal_distribution.html
    #        histogram, bins = np.histogram(dm, bins=hbins, density=True) 
    #        bin_centers = 0.5*(bins[1:] + bins[:-1])
    #
    # 
    #        plt.plot(bin_centers, histogram, label="mode =" + n)
    #        plt.legend()
    #    
    #    plt.show()

    def make_data(N, f=0.3, rseed=1):
        rand = np.random.RandomState(rseed)
        x = rand.randn(N)
        x[int(f * N):] += 5
        return x
    
    x = make_data(1000)

    hbins = np.linspace(-10,10,num=1000)

    from sklearn.neighbors import KernelDensity
    x_d = np.linspace(-4, 8, 1000)
    # instantiate and fit the KDE model
    kde = KernelDensity(bandwidth=1.0, kernel='gaussian')
    kde.fit(x[:, None])
    
    # score_samples returns the log of the probability density
    logprob = kde.score_samples(x_d[:, None])
    
    plt.fill_between(x_d, np.exp(logprob), alpha=0.5)
    plt.plot(x, np.full_like(x, -0.01), '|k', markeredgewidth=1)
    plt.ylim(-0.02, 0.22)
    
    plt.figure()
    
    x = ph1_tidy

    x_d = hbins
    # instantiate and fit the KDE model
    kde = KernelDensity(bandwidth=0.5, kernel='gaussian')
    kde.fit(x[:, None])
    
    # score_samples returns the log of the probability density
    logprob = kde.score_samples(x_d[:, None])
    
    plt.fill_between(x_d, np.exp(logprob), alpha=0.5)
    plt.plot(x, np.full_like(x, -0.01), '|k', markeredgewidth=1)
    plt.ylim(-0.02, 0.22)
 
    plt.figure()
    
    x = np.diff(modes[0])*mode_factor

    x_d = hbins
    # instantiate and fit the KDE model
    kde = KernelDensity(bandwidth=0.01, kernel='gaussian')
    kde.fit(x[:, None])
    
    # score_samples returns the log of the probability density
    logprob = kde.score_samples(x_d[:, None])
    
    plt.fill_between(x_d, np.exp(logprob), alpha=0.5)
    plt.plot(x, np.full_like(x, -0.01), '|k', markeredgewidth=1)
    
    x = np.diff(modes[1])*mode_factor

    x_d = hbins
    # instantiate and fit the KDE model
    kde = KernelDensity(bandwidth=0.01, kernel='gaussian')
    kde.fit(x[:, None])
    
    # score_samples returns the log of the probability density
    logprob = kde.score_samples(x_d[:, None])
    
    plt.fill_between(x_d, np.exp(logprob), alpha=0.5)
    plt.plot(x, np.full_like(x, -0.01), '|k', markeredgewidth=1)
    
    x = np.diff(modes[2])*mode_factor

    x_d = hbins
    # instantiate and fit the KDE model
    kde = KernelDensity(bandwidth=0.01, kernel='gaussian')
    kde.fit(x[:, None])
    
    # score_samples returns the log of the probability density
    logprob = kde.score_samples(x_d[:, None])
    
    plt.fill_between(x_d, np.exp(logprob), alpha=0.5)
    plt.plot(x, np.full_like(x, -0.01), '|k', markeredgewidth=1)
    plt.xlim([-5,5])
    
    x = np.diff(mi[4])*len(mi[3])/2/(2*np.pi)

    x_d = hbins
    # instantiate and fit the KDE model
    kde = KernelDensity(bandwidth=0.01, kernel='gaussian')
    kde.fit(x[:, None])
    
    # score_samples returns the log of the probability density
    logprob = kde.score_samples(x_d[:, None])
    
    plt.fill_between(x_d, np.exp(logprob), alpha=0.5)
    plt.plot(x, np.full_like(x, -0.01), '|k', markeredgewidth=1)
    plt.xlim([-5,5])   
    
    #plt.ylim(-0.02, 0.22)    
    

    

    

    
    
    
    
    
    
       
