# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 12:28:32 2018

@author: gsanca
"""

"""
RUN ONLY WHEN YOU TURN THE SMU ON 
"""

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import functions
import numpy as np
import os

def save_csv(*data, filename, root='.\\', delimiter=',', header='', rewrite=False):
    isfile = os.path.isfile(root+filename+'.csv')
    if not rewrite and isfile:
        print('Este archivo ya existe, para sobreescribirlo usar el argumento rewrite')
        return
    if isfile:
        print('ATENCIÓN: SE SOBREESCRIBIRÁ EL ARCHIVO')
    np.savetxt(root+filename+'.csv', np.transpose(np.array([*data])), header=header, delimiter=delimiter)
    return



functions.clear_all()
gpibAdress = '0x05E6::0x2614::4103593'
[smu,rm]   = functions.gpib(gpibAdress)
smu.write("errorqueue.clear()")
functions.startSMU(smu)
functions.loadScripts(smu)


minV = 0
maxV = 0.4
N = 50
pw = 5e-2
T = 5e-1
limitI = 5e-4
nplc = 0.001
remoteSense = 0
smu.timeout = T*(N+2)*1e3

time, voltage, current = functions.theFunction(smu, minV, maxV, N, pw, T, limitI, nplc, remoteSense)
save_csv(time, voltage, current, filename='Al-Au(C1-D2)-ida2', root='results/', delimiter=',', header=f'Tiempo [s], Voltage [V], Corriente [A]\n minV={minV}, maxV={maxV}, N={N}, pw={pw}, T={T}, limitI={limitI}, nplc={nplc}, remoteSense={remoteSense}')

plt.plot(voltage, abs(current), '-o')
plt.grid()
plt.show()

# smu.write("PulsedSweepVDual(0,2,10,0.01,0.1,0.01,0.01,0)")

# smu.write("list(3,1,0.5,0.1,0,0.1,0,1,0.1,0.01,0.01,5,0.001)")


#list(Vpos,Vneg,stepPos,stepNeg,rev,hslV,hslF,cycles,T,pw,limitI,limitV,nplc)


#smu.write("TR_list(3,1,0.5,0.1,0,0.1,0,1,0.1,0.01,0.01,5,0.001,0,3,1)")