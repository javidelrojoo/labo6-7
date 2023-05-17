# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 12:28:32 2018

@author: gsanca
"""

"""
RUN ONLY WHEN YOU TURN THE SMU ON 
"""
from send_notification import mensaje_tel
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
#%%
dia = '17-5'
# Para V= 0.4, rangeI= 5e-4
# Para V = 0.1, rangeI = 5e-8
N = 50
Vpos = 5
Vneg = 5
# if Vpos > 0.1 or Vneg > 0.1:
    # input('Este voltaje probablemente escriba el dispositivo, presione ENTER para continuar')
stepPos = Vpos/N
stepNeg = Vneg/N
rev = 0
hslV = 0.3
hslF = 1
cycles = 3
T = 2.5e-1
pw = 2.5e-2
limitI = 5e-4
rangeI = 1e-8
limitV = 0.5
rangeV = 20
nplc = 0.01
t, volt, curr = runner.iv(smu,Vpos,Vneg,stepPos,stepNeg,rev,hslV,hslF,cycles,T,pw,limitI,rangeI,limitV,rangeV,nplc)
filename = 'Al-Au(D5-D6)-bias0.3-5V-3ciclos'
save_csv(t, volt, curr, filename=filename, root=f'results/{dia}/', delimiter=',', header=f'Tiempo [s], Voltage [V], Corriente [A]\n Vpos={Vpos}, Vneg={Vneg}, stepPos={stepPos}, stepNeg={stepNeg}, rev={rev}, hslV={hslV}, hslF={hslF}, cycles={cycles}, T={T}, pw={pw}, limitI={limitI}, rangeI={rangeI}, limitV={limitV}, rangeV={rangeV}, nlpc={nplc}')

mensaje_tel(
api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
chat_id = '-1001926663084',
mensaje = 'Ya acabé'
)

plt.figure()
plt.scatter(volt[1::2], 0.4/abs(curr)[::2], c=t[::2], cmap='cool')
# plt.scatter(volt[1::2], abs(curr)[1::2], c=t[::2], cmap='cool')
# plt.scatter(volt[1:400:2], 0.4/abs(curr)[:400:2], c='C0', label='Ciclo 1')
# plt.scatter(volt[401:800:2], 0.4/abs(curr)[400:800:2], c='C1', label='Ciclo 2')
# plt.scatter(volt[801:1600:2], 0.4/abs(curr)[800:1600:2], c='C2', label='Ciclo 3')
plt.xlabel('Voltaje [V]')
plt.ylabel('Resistencia [$\Omega$]')
# plt.yscale('log')
plt.legend()
plt.colorbar(label='Tiempo [s]')
plt.grid()

plt.savefig(f'../graficos/{dia}/{filename}.png', dpi=400)
#%%
plt.close('all')

# plt.figure()
# plt.scatter(t, volt)
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

for filename in os.listdir('results/15-5/'):
    t, V, I = np.loadtxt(f'results/15-5/{filename}', delimiter=',', unpack=True, skiprows=2)
    plt.figure()
    plt.scatter(V[1::2], 0.4/abs(I)[:-1:2], c=t[:-1:2], cmap='cool')
    plt.xlabel('Voltaje [V]')
    plt.ylabel('Resistencia [$\Omega$]')
    plt.colorbar(label='Tiempo [s]')
    plt.grid()
    plt.title(filename)
    plt.show()

t, V, I = np.loadtxt('results/15-5/Al-Au(F5-F6)-bias0.3-7V.csv', delimiter=',', unpack=True, skiprows=2)
plt.figure()
plt.scatter(V[1::2], 0.4/abs(I)[:-1:2], c=t[:-1:2], cmap='cool')
plt.xlabel('Voltaje [V]')
plt.ylabel('Resistencia [$\Omega$]')
plt.colorbar(label='Tiempo [s]')
plt.grid()
plt.savefig('../graficos/(15-5)Al-Au(F5-F6)-bias0.3-7V.png', dpi=400)

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
