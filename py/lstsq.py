#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 13:28:29 2020

@author: tim
"""

import numpy as np
import matplotlib.pyplot as plt

#x = np.array([0, 1, 2, 3])
#y = np.array([-1, 0.2, 0.9, 2.1])
#A = np.vstack([x, np.ones(len(x))]).T
#m, c = np.linalg.lstsq(A, y, rcond=None)[0]
#
#_ = plt.plot(x, y, 'o', label='Original data', markersize=10)
#_ = plt.plot(x, m*x + c, 'r', label='Fitted line')
#_ = plt.legend()
#plt.show()


#t = np.linspace(0,2*np.pi,200)
#t = t[:-1] #do not duplicate the first/last point



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
# return residual as well?
# Ben needs it as SNR

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

