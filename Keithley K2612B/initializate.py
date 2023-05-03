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
import runner
import numpy as np
import os
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

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

# Para V= 0.4, rangeI= 5e-4
# Para V = 0.1, rangeI = 5e-8
N = 75
Vpos = 5
Vneg = 5
if Vpos > 0.1 or Vneg > 0.1:
    input('Este voltaje probablemente escriba el dispositivo, presione ENTER para continuar')
stepPos = Vpos/N
stepNeg = Vneg/N
rev = 0
hslV = 0.4
hslF = 1
cycles = 5
T = 2.5e-1
pw = 2.5e-2
limitI = 5e-4
rangeI = 1e-8
limitV = 0.5
rangeV = 20
nplc = 0.01
t, volt, curr = runner.iv(smu,Vpos,Vneg,stepPos,stepNeg,rev,hslV,hslF,cycles,T,pw,limitI,rangeI,limitV,rangeV,nplc)
save_csv(t, volt, curr, filename='Al-Au(E7-E8)-bias5-5V5ciclos', root='results/', delimiter=',', header=f'Tiempo [s], Voltage [V], Corriente [A]\n Vpos={Vpos}, Vneg={Vneg}, stepPos={stepPos}, stepNeg={stepNeg}, rev={rev}, hslV={hslV}, hslF={hslF}, cycles={cycles}, T={T}, pw={pw}, limitI={limitI}, rangeI={rangeI}, limitV={limitV}, rangeV={rangeV}, nlpc={nplc}')


# plt.plot(volt, abs(curr), '-o')
# plt.grid()

volt, curr = plot('d')
volt, curr = plot('bd')
volt_d, r = plot('b')
def plot(mode):
    fig, ax = plt.subplots()
    mode = mode
    if mode=='d':    
        points = np.array([volt, abs(curr)]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        # Create a continuous norm to map from data points to colors
        norm = plt.Normalize(t.min(), t.max())
        lc = LineCollection(segments, cmap='viridis', norm=norm) #, linestyles='dashed'
        # Set the values used for colormapping
        lc.set_array(t)
        lc.set_linewidth(2)
        line = ax.add_collection(lc)
        # fig.colorbar(line, ax=ax)
        ax.set_xlim(volt.min(), volt.max())
        ax.set_ylim(abs(curr).min(), abs(curr).max())
        ax.scatter(volt, abs(curr), c=t)
        ax.grid(True)
        # ax.set_yscale('log')
        return volt, abs(curr)
    elif mode=='bd':
        volt_d = volt[1::2]
        curr_d = curr[1::2]
        points = np.array([volt_d, abs(curr_d)]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        # Create a continuous norm to map from data points to colors
        norm = plt.Normalize(t.min(), t.max())
        lc = LineCollection(segments, cmap='viridis', norm=norm) #, linestyles='dashed'
        # Set the values used for colormapping
        lc.set_array(t)
        lc.set_linewidth(2)
        line = ax.add_collection(lc)
        # fig.colorbar(line, ax=ax)
        ax.set_xlim(volt_d.min(), volt_d.max())
        ax.set_ylim(abs(curr_d).min(), abs(curr_d).max())
        ax.scatter(volt_d, abs(curr_d), c=t[1::2])
        ax.grid(True)
        # ax.set_yscale('log')
        return volt, abs(curr)
    elif mode=='b':
        volt_b = volt[::2]
        volt_d = volt[1::2]
        curr_d = curr[::2]
        r = volt_b/curr_d
        points = np.array([volt_d, r]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        # Create a continuous norm to map from data points to colors
        norm = plt.Normalize(t.min(), t.max())
        lc = LineCollection(segments, cmap='viridis', norm=norm) #, linestyles='dashed'
        # Set the values used for colormapping
        lc.set_array(t)
        lc.set_linewidth(2)
        line = ax.add_collection(lc)
        # fig.colorbar(line, ax=ax)
        ax.set_xlim(volt_d.min(), volt_d.max())
        ax.set_ylim(r.min(), r.max())
        ax.scatter(volt_d, r, c=t[::2])
        ax.grid(True)
        # ax.set_yscale('log')
        return volt_d, r
    
for filename in os.listdir('./results/'):
    if filename.startswith('Al-Au(E3-F2)-ida-vuelta'):
        if filename.startswith('Al-Au(E2-F3)-ida-vuelta-bias'):
            pass
        else:
            t1, volt1, curr1 = np.loadtxt('results/' + filename, delimiter=',', unpack=True, skiprows=2)
            if volt1.max() < 0.45:
                pass
            else:
                plt.plot(volt1, abs(curr1)*1000, '-o') #NOBIAS
            # plt.plot(volt1[1::2], abs(curr1)[1::2]*1000, '-o') #BIAS
        # plt.plot(t1[::2], abs(curr1)[::2], '-o')
plt.xlabel('Tensión [V]')
plt.ylabel('|Corriente| [mA]')
plt.grid()
plt.show()
plt.savefig('../graficos/'+'Au-Au(E3-F2)-ida-vuelta'+'.png')

# Esto era para barrido en una sola direccion
# minV = 0
# maxV = 0.4
# N = 50
# pw = 5e-2
# T = 5e-1
# limitI = 5e-4
# nplc = 0.001
# remoteSense = 0
# smu.timeout = T*(N+2)*1e3
# time, voltage, current = functions.theFunction(smu, minV, maxV, N, pw, T, limitI, nplc, remoteSense)
# save_csv(time, voltage, current, filename='Al-Au(C1-D2)-ida2', root='results/', delimiter=',', header=f'Tiempo [s], Voltage [V], Corriente [A]\n minV={minV}, maxV={maxV}, N={N}, pw={pw}, T={T}, limitI={limitI}, nplc={nplc}, remoteSense={remoteSense}')
