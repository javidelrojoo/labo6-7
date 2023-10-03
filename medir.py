import pyvisa
import numpy as np
import matplotlib.pyplot as plt
from save_csv import save_csv
from tqdm import tqdm
import time
import math
import os
from send_notification import mensaje_tel, foto_tel
from matplotlib.colors import LogNorm
#%%
##################################################################
# CAMBIARLO EN CADA DIA Y EN CADA MEDICION
##################################################################

dia = '9-29'
#%%
##################################################################
# CORRERLO UNA VEZ POR DIA
##################################################################

os.mkdir(f'./results/Tonghui/{dia}')
os.mkdir(f'./results/Keithley/{dia}')
os.mkdir(f'./graficos/{dia}')
#%%
from TektronixTDS1002B import TDS1002B

osci = TDS1002B('USB0::0x0699::0x0413::C012302::INSTR')

t1, ch1 = osci.read_data(1)
t2, ch2 = osci.read_data(2)


plt.plot(t1, ch1)
plt.plot(t2, ch2)

save_csv(data, filename)

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
# Curva IV con nuestro codigo
##################################################################
filename = '80-Al-Au(C3-C4)'

Vmax = 5
Vmin = -5
hslV = 0.4
pw = 0.1
Npos = 50
Nneg = 50
rangei = 1e-3 #[1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 1.5]
limiti = 0.5
rangev = 2
cycles = 2
T1 = 0.01
T2 = 0.01
nplc = 0.5

t_din, volt_din, curr_din, t_rem, volt_rem, curr_rem = smu.hsl(Vmax, Vmin, pw, Npos, Nneg, rangei, limiti, rangev, cycles, T1, T2, nplc, hslV)
# print(volt_rem/curr_rem)


# n = 1

# ciclos = []
# for i in range(30):
#     ciclos.append(curr_rem[n:n+147])
#     # plt.plot(t_din[n:n+147], volt_din[n:n+147], '-o')
#     # plt.plot(t_rem[n:n+147], volt_rem[n:n+147], '-o')
#     # print(i)
#     # plt.scatter(volt_din[n:n+147], abs(volt_rem[n:n+147]/curr_rem[n:n+147]), c=t_rem[n:n+147], cmap='cool')
#     # plt.show()
#     n += 148
# # plt.grid()
# # plt.show()
# #17, 18
# curr_mean = np.mean(np.array(ciclos), axis=0)
# curr_std = np.std(np.array(ciclos), axis=0)


hora = time.strftime("%H %M %S", time.localtime())
save_csv(t_din, volt_din, curr_din, t_rem, volt_rem, curr_rem, filename=f'{filename}-({Vmin},{Vmax})-({hora})', root=f'./results/Keithley/{dia}/', delimiter=',', header=f'{time.ctime()}\n Tiempo dinamica [s], Voltaje dinamica [V], Corriente dinamica [A], Tiempo remanente [s], Voltaje remanente [V], Corriente remanente [A]\n Vmax={Vmax}, Vmin={Vmin}, Npos={Npos}, Nneg={Nneg}, pw={pw}, cycles={cycles}, hslV={hslV}, T1 = {T1}, T2 = {T2}, nplc={nplc}')

plt.figure()
plt.scatter(volt_din, volt_rem/abs(curr_rem), c=t_rem, cmap='cool')
# plt.scatter(volt_rem, volt_din/abs(curr_din), c=t_rem, cmap='cool')
# plt.errorbar(volt_din[1:148], 0.4/np.abs(curr_mean), yerr=0.4*curr_std/curr_mean**2, fmt='-ok', capsize=3, errorevery=2, label='Promedio de ciclos')
plt.xlabel('Voltaje [V]')
plt.ylabel('Resistencia [$\Omega$]')
# plt.ylabel('Corriente [A]')
plt.yscale('log')
plt.colorbar(label='Tiempo [s]')
plt.grid()
plt.show()

plt.savefig(f'./graficos/{dia}/{filename}-({Vmin},{Vmax})-({hora}).png', dpi=400)

mensaje_tel(
api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
chat_id = '-1001926663084',
mensaje = f'{filename} Ya acabé'
)
foto_tel(api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
          chat_id = '-1001926663084',
          file_opened = open(f'./graficos/{dia}/{filename}-({Vmin},{Vmax})-({hora}).png', 'rb'))

#%%
##################################################################
# Pulsos hasta R de umbral y despues lectura
##################################################################
filename = '80-Al-Au(C3-C4)'

V = 4
Rth1 = 4e6
Rth2 = 12e6
hslV = 0.4
pw = 0.1
rangei = 1e-3 #[1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 1.5]
limiti = 0.5
rangev = 2
T1 = 0.01*4
T2 = 0.01*4
nplc = 0.5

t_din, volt_din, curr_din, t_rem, volt_rem, curr_rem = smu.autoR(V, Rth1, Rth2, rangei, limiti, rangev, cycles, pw, T1, T2, nplc, hslV)

hora = time.strftime("%H %M %S", time.localtime())
save_csv(t_rem, volt_rem, curr_rem, filename=f'{filename}-(autoR)-({V}V)-({hora})', root=f'./results/Keithley/{dia}/', delimiter=',', header=f'{time.ctime()}\n Tiempo remanente [s], Voltaje remanente [V], Corriente remanente [A]\n V={V}, Rht1={Rth1}, Rth2={Rth2}, pw={pw}, hslV={hslV}, T1 = {T1}, T2 = {T2}, nplc={nplc}, pulsos hasta umbral={len(volt_din)}')

# plt.figure()
# plt.scatter(volt_din, (volt_rem/abs(curr_rem))[:len(volt_din)], c=t_rem[:len(volt_din)], cmap='cool')
# plt.xlabel('Voltaje [V]')
# plt.ylabel('Resistencia [$\Omega$]')
# plt.yscale('log')
# plt.colorbar(label='Tiempo [s]')
# plt.grid()
# plt.show()

# plt.savefig(f'./graficos/{dia}/{filename}-(autoR)-({V},{Rth1},{Rth2})-IV-({hora}).png', dpi=400)

plt.figure()
plt.plot(t_rem, (volt_rem/abs(curr_rem)))
plt.xlabel('Tiempo [s]')
plt.ylabel('Resistencia [$\Omega$]')
plt.yscale('log')
plt.grid()
plt.show()

plt.savefig(f'./graficos/{dia}/{filename}-(autoR)-({V}V)-({hora}).png', dpi=400)

mensaje_tel(
api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
chat_id = '-1001926663084',
mensaje = f'{filename} Ya acabé. {len(volt_din)} pulsos hasta el umbral'
)

foto_tel(api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
          chat_id = '-1001926663084',
          file_opened = open(f'./graficos/{dia}/{filename}-(autoR)-({V}V)-({hora}).png', 'rb'))




#%%
##################################################################
# Voltaje custom (acumulacion de pulsos)
##################################################################
filename = '80-Al-Au(C3-C4)'


volt_meas = []
for i in np.concatenate((np.linspace(0, 8, 50, endpoint=False), np.linspace(8, 0, 50, endpoint=False), np.linspace(0, -3, 50, endpoint=False), np.linspace(-3, 0, 50, endpoint=False))):
    volt_meas.append(0.4)
    volt_meas.append(i)
    
# volt_meas = volt_meas+[0.4]*150
# volt_meas = [0.4]*10

pw = 0.1
rangei = 1e-3 #[1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 1.5]
limiti = 0.5
rangev = 2
T = 0.01
nplc = 0.5

t, volt, curr = smu.custom_volt(volt_meas, pw, rangei, limiti, rangev, T, nplc)
# print(0.4/curr*1e-6)


hora = time.strftime("%H %M %S", time.localtime())
save_csv(t, volt, curr, filename=f'{filename}-(tren-pulsos)-({hora})', root=f'./results/Keithley/{dia}/', delimiter=',', header=f'{time.ctime()}\n Tiempo [s], Voltaje [V], Corriente [A]\n  pw={pw}, T = {T}, nplc={nplc}')

# mensaje_tel(
# api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
# chat_id = '-1001926663084',
# mensaje = f'{filename} Ya acabé'
# )

plt.figure()
plt.scatter(volt[1::2], abs(volt/curr)[:-1:2], c=t[:-1:2], cmap='cool')
plt.yscale('log')
plt.grid()

plt.figure()
plt.plot(t[100:], (volt/curr)[100:], '-o')
plt.xlabel('Tiempo [s]')
plt.ylabel('Resistencia [$\Omega$]')
# plt.ylabel('Corriente [A]')
plt.grid()
plt.show()

plt.savefig(f'./graficos/{dia}/{filename}-(tren-pulsos)-({hora}).png', dpi=400)


# foto_tel(api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
#           chat_id = '-1001926663084',
#           file_opened = open(f'./graficos/{dia}/{filename}-(tren-pulsos)-({hora}).png', 'rb'))



#%%
######################################################
# CODIGO PARA PROBAR DISITNTOS RANGOS DE I
######################################################
a = np.array([])
plt.figure()
for i in ['auto']:
    rangei = i    

    for _ in range(50):
        t_din, volt_din, curr_din, t_rem, volt_rem, curr_rem = smu.hsl(Vmax, Vmin, pw, Npos, Nneg, rangei, limiti, rangev, hslV)
    
        a = np.concatenate((a, np.abs(volt_rem/curr_rem)))
    
    plt.hist(a, label=i)
    
    save_csv(a, filename=f'resistencia2.8k-rangei{i}', root=f'./results/Keithley/{dia}/', delimiter=',', header=f'{time.ctime()}\n Resistencia medida con rangei={i} [Ohm]\n Vmax={Vmax}, Vmin={Vmin}, Npos={Npos}, Nneg={Nneg}, pw={pw}, hslV={hslV}')
    a = np.array([])

for file in os.listdir(f'./results/Keithley/{dia}/'):
    if file.startswith('resistencia2.8k'):
        R = np.loadtxt(f'./results/Keithley/{dia}/' + file, skiprows=3, delimiter=',', unpack=True)
        plt.hist(R, label=file[22:-4])
        print(file[22:-4], np.std(R), np.mean(R))
plt.legend()
plt.xscale('log')
plt.yscale('log')
#%%
##################################################################
# STRESS CON KEITHLEY
##################################################################

num_med = ' '
V = 5 #V
time_interval = 1 #s
total_time = 10 #s

t, curr, volt = smu.stress_DC(V, time_interval, total_time)
# save_csv(t, volt, curr, filename=f'{filename}{num_med}', root=f'./results/Keithley/{dia}/', delimiter=',', header=f'{time.ctime()}\n Tiempo [s], Voltage [V], Corriente [A]\n V={V},time_interval={time_interval},total_time={total_time}')

plt.figure()
plt.plot(t, V/curr, 'o', label=f'{V}V')
plt.xlabel('Tiempo [s]')
plt.ylabel('Resistencia [$\Omega$]')
# plt.yscale('log')
plt.legend()
plt.grid()
# plt.savefig(f'./graficos/{dia}/{filename}-{V}V{num_med}.png', dpi=400)

# mensaje_tel(
#     api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
#     chat_id = '-1001926663084',
#     mensaje = f'Ya acabé con {V}V'
#     )
    
# foto_tel(api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
#          chat_id = '-1001926663084',
#          file_opened = open(f'./graficos/{dia}/{filename}-{V}V{num_med}.png', 'rb'))
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
filename = 'Al-Au(F1-F2)'

num_med = '2'
N = 25
Vpos = 5
Vneg = 5
stepPos = Vpos/N 
stepNeg = Vneg/N
rev = 0
hslV = 0.4
hslF = 1
cycles = 2
T = 0.125
pw = T/2
limitI = 0.5
rangeI = 1e-8
limitV = 5
rangeV = 20
nplc = 0.001

t, volt, curr = runner.iv(smu,Vpos,Vneg,stepPos,stepNeg,rev,hslV,hslF,cycles,T,pw,limitI,rangeI,limitV,rangeV,nplc, gpibAdress)

# filename = 'Al-Au(C5-c6)-bias0.4-7V-2ciclos'
save_csv(t, volt, curr, filename=f'{filename}-(-{Vneg},{Vpos})-{num_med}', root=f'./results/Keithley/{dia}/', delimiter=',', header=f'{time.ctime()}\n Tiempo [s], Voltage [V], Corriente [A]\n Vpos={Vpos}, Vneg={Vneg}, stepPos={stepPos}, stepNeg={stepNeg}, rev={rev}, hslV={hslV}, hslF={hslF}, cycles={cycles}, T={T}, pw={pw}, limitI={limitI}, rangeI={rangeI}, limitV={limitV}, rangeV={rangeV}, nlpc={nplc}')

plt.figure()
plt.scatter(volt[1::2], hslV/abs(curr[::2]), c=t[::2], cmap='cool')

# volt_rem = np.concatenate((volt[1:-1:2][:100], volt[::2][101:201], volt[1:-1:2][202:]))
# curr_rem = np.concatenate((curr[::2][:100], curr[1:-1:2][102:201], curr[::2][202:]))
# plt.scatter(volt_rem, hslV/abs(curr_rem), c=t[:-6:2], cmap='cool')

# plt.plot(volt[1::2], hslV/abs(curr[::2]))
# plt.scatter(volt, curr, c=t, cmap='cool')
plt.xlabel('Voltaje [V]')
plt.ylabel('Resistencia [$\Omega$]')
# plt.ylabel('Corriente [A]')
plt.yscale('log')
plt.colorbar(label='Tiempo [s]')
plt.grid()

plt.savefig(f'./graficos/{dia}/{filename}-(-{Vneg},{Vpos})-{num_med}.png', dpi=400)

mensaje_tel(
api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
chat_id = '-1001926663084',
mensaje = f'{filename} Ya acabé con {T}s'
)
foto_tel(api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
          chat_id = '-1001926663084',
          file_opened = open(f'./graficos/{dia}/{filename}-(-{Vneg},{Vpos})-{num_med}.png', 'rb'))

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
plt.close('all')
from Tonghui_TH283X.TonghuiTH283X import TH283X

lcr = TH283X('USB0::0x0471::0x2827::QF40900001::INSTR')
#%%
##################################################################
# CICLO DE BIAS CON EL TONGHUI
##################################################################
filename = '80-Al-Au(C3-C4)'

# level = 0.1
# lcr.set_volt(level)
bias_list = [0]
level_list = [0.4]

if not (len(bias_list) == len(level_list)):
    input('No hay la misma cantidad de valores')

frecs = np.unique(np.loadtxt('Tonghui_TH283X/results/Caracterización/frecuencia-LCR.csv', delimiter=',', unpack=True, skiprows=2)[1])
# frecs = np.concatenate((frecs[:300:10], frecs[300:600:5], frecs[600:]))
# plt.plot(frecs, 'o')
# plt.yscale('log')
# frecs = frecs[87:]
i = 0
for bias,level in zip(bias_list, level_list):
    lcr.set_volt(level)
    mensaje_tel(
    api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
    chat_id = '-1001926663084',
    mensaje = f'{time.ctime()}\n{i}/{len(bias_list)} - Arranco con {bias}V de bias'
    )
    hora = time.strftime("%H %M %S", time.localtime())
    # lcr.set_DC_bias_volt(bias)
    f, Z, phase = lcr.make_EI(frecs, 'ZTD', fast=False)
    save_csv(f, Z, phase, filename = f'{filename}-level{level}V-bias{bias}V-({hora})', root=f'./results/Tonghui/{dia}/', delimiter=',', header=f'{time.ctime()}\n Frecuencia [Hz], Z [Ohm], Fase [deg]')
    
    plt.savefig(f'./graficos/{dia}/{filename}-level{level}V-bias{bias}V-({hora}).png', dpi=400)
    
    plt.figure()
    Zre = Z*np.cos(phase*np.pi/180)
    Zim = Z*np.sin(phase*np.pi/180)
    plt.scatter(Zre, -Zim, c=f, cmap='cool', norm=LogNorm())
    plt.colorbar(label='Frecuencia [Hz]')
    plt.grid()
    plt.xlabel('Re(Z) [$\Omega$]')
    plt.ylabel('-Im(Z) [$\Omega$]')

    plt.savefig(f'./graficos/{dia}/{filename}-level{level}V-bias{bias}V-({hora})-nyquist.png', dpi=400)
    
    mensaje_tel(
    api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
    chat_id = '-1001926663084',
    mensaje = f'{i+1}/{len(bias_list)} - Ya acabé con {bias}V de bias'
    )
    
    foto_tel(api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
             chat_id = '-1001926663084',
             file_opened = open(f'./graficos/{dia}/{filename}-level{level}V-bias{bias}V-({hora}).png', 'rb'))
    foto_tel(api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
             chat_id = '-1001926663084',
             file_opened = open(f'./graficos/{dia}/{filename}-level{level}V-bias{bias}V-({hora})-nyquist.png', 'rb'))
    i += 1

# lcr.set_DC_bias_volt(0)
lcr.set_volt(0.01)