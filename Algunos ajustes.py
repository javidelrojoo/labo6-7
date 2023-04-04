# -*- coding: utf-8 -*-


import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


#Z_mod = R + 1j/(2*np.pi*f*C)

def cp(f, R, C):
    return 1/(np.sqrt(C**2*f**2+1/R**2))
def cs(f, R, C):
    return (R*2*np.pi*f*C)/np.sqrt(1+(R*2*np.pi*f*C)**2)
def RLC(f, R, L, C):
    # R = R*np.sqrt(f)
    return 1/np.sqrt(1/R**2+(1/(2*np.pi*f*L)-(2*np.pi*f*L))**2)


a = np.loadtxt('resistencia_10mOhm_sincorrecciones.csv',skiprows=1, delimiter=',')

f, Z, t = np.transpose(a)
#%%
plt.figure()
plt.plot(f,Z)
plt.xscale('log')

#%%
popt, pcov = curve_fit(cp, f, Z, p0=[1e7,1e-11])

plt.figure()
plt.plot(f,Z)
plt.plot(f,cp(f,*popt))
plt.xscale('log')

#%%
sopt, scov = curve_fit(cs, f, Z)

plt.figure()
plt.plot(f,cs(f,*sopt))
plt.xscale('log')

#%%
plt.figure()
# plt.plot(f,Z)
for i in np.linspace(1e-9,1,100):
    plt.plot(f,cs(f,1e7,i))
plt.xscale('log')