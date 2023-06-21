import pyvisa
import numpy as np
import matplotlib.pyplot as plt
from save_csv import save_csv
from tqdm import tqdm
import time
import math
import os
from send_notification import mensaje_tel, foto_tel
#%%
##################################################################
# CAMBIARLO EN CADA DIA Y EN CADA MEDICION
##################################################################

dia = '6-21'
filename = 'Al-Au(C5-C6)'
#%%
##################################################################
# CORRERLO UNA VEZ POR DIA
##################################################################

# os.mkdir(f'./results/Tonghui/{dia}')
os.mkdir(f'./results/Keithley/{dia}')
os.mkdir(f'./graficos/{dia}')
#%%
##################################################################
# IMPORTS PARA KEITHLEY
##################################################################

import Keithley_K2612B.functions as functions
import Keithley_K2612B.runner as runner
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
#%%
##################################################################
# INICIALIZAR (PARA NUESTRO CODIGO A PROBAR)
##################################################################
from Keithley_K2612B.keithleyK2612B import K2612B
from keithley2600 import Keithley2600

smu = K2612B('USB0::0x05E6::0x2614::4103593::INSTR')
# smu = Keithley2600('USB0::0x05E6::0x2614::4103593::INSTR')
#%%
##################################################################
# STRESS CON KEITHLEY
##################################################################

num_med = ' '
V = 5 #V
time_interval = 1 #s
total_time = 600 #s

t, curr, volt = smu.DC_volt(V, time_interval, total_time)
# save_csv(t, volt, curr, filename=f'{filename}{num_med}', root=f'./results/Keithley/{dia}/', delimiter=',', header=f'{time.ctime()}\n Tiempo [s], Voltage [V], Corriente [A]\n V={V},time_interval={time_interval},total_time={total_time}')

plt.figure()
plt.plot(t, V/curr, 'o', label=f'{V}V')
plt.xlabel('Tiempo [s]')
plt.ylabel('Resistencia [$\Omega$]')
# plt.yscale('log')
plt.legend()
plt.grid()
# plt.savefig(f'./graficos/{dia}/{filename}-{V}V{num_med}.png', dpi=400)

mensaje_tel(
    api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
    chat_id = '-1001926663084',
    mensaje = f'Ya acabé con {V}V'
    )
    
foto_tel(api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
         chat_id = '-1001926663084',
         file_opened = open(f'./graficos/{dia}/{filename}-{V}V{num_med}.png', 'rb'))
#%%
##################################################################
# INICIALIZAR (PARA EL CODIGO DE LA UNSAM)
##################################################################

functions.clear_all()
gpibAdress = '0x05E6::0x2614::4103593'
[smu,rm]   = functions.gpib(gpibAdress)
smu.write("errorqueue.clear()")
functions.startSMU(smu)
functions.loadScripts(smu)
#%%
##################################################################
# CICLO DE PULSOS CON KEITHLEY
##################################################################
filename = 'Al-Au(D5-D6)-hsl'

num_med = ''
N = 50
Vpos = 5
Vneg = 0.001
stepPos = Vpos/N
stepNeg = 10
rev = 0
hslV = 0.4
hslF = 1
cycles = 1
# T = 1
# pw = 2.5e-3
limitI = 5e-4
rangeI = 1e-8
limitV = 0.5
rangeV = 20
nplc = 0.001

for i,T in enumerate([4, 8]):
    pw = T/2
    t, volt, curr = runner.iv(smu,Vpos,Vneg,stepPos,stepNeg,rev,hslV,hslF,cycles,T,pw,limitI,rangeI,limitV,rangeV,nplc, gpibAdress)
    # filename = 'Al-Au(C5-c6)-bias0.4-7V-2ciclos'
    save_csv(t, volt, curr, filename=f'{filename}-{T}s-{num_med}', root=f'./results/Keithley/{dia}/', delimiter=',', header=f'{time.ctime()}\n Tiempo [s], Voltage [V], Corriente [A]\n Vpos={Vpos}, Vneg={Vneg}, stepPos={stepPos}, stepNeg={stepNeg}, rev={rev}, hslV={hslV}, hslF={hslF}, cycles={cycles}, T={T}, pw={pw}, limitI={limitI}, rangeI={rangeI}, limitV={limitV}, rangeV={rangeV}, nlpc={nplc}')

    plt.figure()
    plt.scatter(volt[1::2], hslV/abs(curr[::2]), c=t[::2], cmap='cool')
    # plt.scatter(volt[1::2], abs(curr)[1::2], c=t[:-1:2], cmap='cool')
    # plt.scatter(t[800:1595:2], volt[800:1595:2])
    # plt.plot(t, volt, 'o')
    # plt.scatter(volt[1:799:2], 0.4/abs(curr)[:798:2], c='C0', label='Ciclo 1')
    # plt.scatter(volt[800:1595:2], 0.4/abs(curr)[801:1597:2], c='C1', label='Ciclo 2')
    # plt.scatter(volt[801:1600:2], 0.4/abs(curr)[800:1600:2], c='C2', label='Ciclo 3')
    plt.xlabel('Voltaje [V]')
    plt.ylabel('Resistencia [$\Omega$]')
    # plt.yscale('log')
    plt.legend()
    plt.colorbar(label='Tiempo [s]')
    plt.grid()
    plt.savefig(f'./graficos/{dia}/{filename}-{T}s-{num_med}.png', dpi=400)
    
    mensaje_tel(
    api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
    chat_id = '-1001926663084',
    mensaje = f'{filename}{num_med}\n Ya acabé con {T}s'
    )
    foto_tel(api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
             chat_id = '-1001926663084',
             file_opened = open(f'./graficos/{dia}/{filename}-{T}s-{num_med}.png', 'rb'))
    time.sleep(60)
#%%
##################################################################
# STRESS CON KEITHLEY (CODIGO RECICLADO DEL PULSO)
##################################################################
filename = 'Al-Au(F1-F2)-stress'

N = 200
cycles = 1
T = 1
pw = 0.999
limitI = 5e-4
rangeI = 1e-8
limitV = 0.5
rangeV = 20
nplc = 0.01

for V, num_med in zip([5], [' 2']):
    t, volt, curr = runner.stress(smu, V, N, cycles, T, pw, limitI, rangeI, limitV, rangeV, nplc, gpibAdress)
    save_csv(t, volt, curr, filename=f'{filename}-{V}V{num_med}', root=f'./results/Keithley/{dia}/', delimiter=',', header=f'{time.ctime()}\n Tiempo [s], Voltage [V], Corriente [A]\n V={V}, N={N}, cycles={cycles}, T={T}, pw={pw}, limitI={limitI}, rangeI={rangeI}, limitV={limitV}, rangeV={rangeV}, nlpc={nplc}')
    
    plt.figure()
    plt.plot(t, V/curr, 'o', label=f'{V}V')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Resistencia [$\Omega$]')
    # plt.yscale('log')
    plt.legend()
    # plt.colorbar(label='Tiempo [s]')
    plt.grid()
    plt.savefig(f'./graficos/{dia}/{filename}-{V}V{num_med}.png', dpi=400)
    
    mensaje_tel(
    api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
    chat_id = '-1001926663084',
    mensaje = f'{filename}{num_med}\n Ya acabé con {V}V'
    )
    
    foto_tel(api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
             chat_id = '-1001926663084',
             file_opened = open(f'./graficos/{dia}/{filename}-{V}V{num_med}.png', 'rb'))
    # time.sleep(120)
#%%
##################################################################
# IMPORTS PARA TONGHUI
##################################################################

from Tonghui_TH283X.TonghuiTH283X import TH283X

lcr = TH283X('USB0::0x0471::0x2827::QF40900001::INSTR')
#%%
##################################################################
# CICLO DE BIAS CON EL TONGHUI
##################################################################

lcr.set_volt(0.4)
bias_list = [0.3, 0.4, 0.5]


frecs = np.unique(np.loadtxt('Tonghui_TH283X/results/Caracterización/frecuencia-LCR.csv', delimiter=',', unpack=True, skiprows=2)[1])
frecs = frecs[::2]
# frecs = frecs[87:]

for i,bias in enumerate(bias_list):
    lcr.set_DC_bias_volt(bias)
    f, Z, phase = lcr.make_EI(frecs, 'ZTD', fast=False)
    save_csv(f, Z, phase, filename = filename+f'-{i}-bias{bias}', root=f'./results/Tonghui/{dia}/', delimiter=',', header=f'{time.ctime()}\n Frecuencia [Hz], Z [Ohm], Fase [°]')
    
    plt.savefig(f'./graficos/{dia}/{filename}-{i}-bias{bias}.png', dpi=400)
    
    mensaje_tel(
    api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
    chat_id = '-1001926663084',
    mensaje = f'{i+1}/{len(bias_list)} - Ya acabé con {bias}V de bias'
    )
    
    foto_tel(api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
             chat_id = '-1001926663084',
             file_opened = open(f'./graficos/{dia}/{filename}-{i}-bias{bias}.png', 'rb'))
    
    plt.figure()

lcr.set_DC_bias_volt(0)