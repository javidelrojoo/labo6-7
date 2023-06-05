import pyvisa
import numpy as np
import matplotlib.pyplot as plt
from save_csv import save_csv
from tqdm import tqdm
from TonghuiTH283X import TH283X
import time
import math
import os

lcr = TH283X('USB0::0x0471::0x2827::QF40900001::INSTR')
#%%
lcr.set_freq(1e3)
lcr.get_freq()

lcr.set_volt(0.3)
lcr.get_volt()

lcr.set_DC_bias_volt(0)

lcr.measure('ZTD')

lcr._lcr.query('*OPC?')
lcr._lcr.write('*OPC')
lcr._lcr.query('FETC?')

lcr.make_corr_open()

#%%
dia = '29-5'
filename = 'Al-Au(D5-D6)-level0.4-pol-neg'
#%%
os.mkdir(f'../results/Tonghui/{dia}')
os.mkdir(f'../graficos/{dia}')
#%%
lcr.set_volt(0.4)
bias_list = [0, -3, -5, -3, 0]


frecs = np.unique(np.loadtxt('results\Caracterización\\frecuencia-LCR.csv', delimiter=',', unpack=True, skiprows=2)[1])
frecs = frecs[::2]
frecs = frecs[87:]
# frecs = np.logspace(np.log10(20), np.log10(2e5), 300)
# frecs = np.linspace(10e3, 2e5, 250)

for i,bias in enumerate(bias_list):
    lcr.set_DC_bias_volt(bias)
    f, Z, phase = lcr.make_EI(frecs, 'ZTD', fast=False)
    save_csv(f, Z, phase, filename = filename+f'-{i}-bias{bias}', root=f'../results/Tonghui/{dia}/', delimiter=',', header='{time.ctime()}\n Frecuencia [Hz], Z [Ohm], Fase [°]')
    
    mensaje_tel(
    api_token = '6228563199:AAFh4PtD34w0dmV_hFlQC7Vqg3ScI600Djs',
    chat_id = '-1001926663084',
    mensaje = f'{i+1}/{len(bias_list)} - Ya acabé con {bias}V de bias'
    )

    plt.savefig(f'../graficos/{dia}/{filename}-{i}-bias{bias}.png', dpi=400)
    plt.figure()

lcr.set_DC_bias_volt(0)
#%%
plt.close('all')
plt.plot(f, Z, 'o')
plt.xscale('log')

lcr.set_DC_bias_volt(0)
lcr.set_DC_bias_off()

Z_mod = 28e3 + 1j/(f*2*np.pi*500e-9)
phase_mod = np.angle(Z_mod, deg=True)

plt.plot(f, 20*np.log10(Z), '-o')
# plt.plot(f2, 20*np.log10(Z2), '-ro')
# plt.plot(f, 20*np.log10(np.abs(Z_mod)))
# plt.plot(f, Z, '-o')
plt.xscale('log')
plt.figure()
plt.plot(f, -phase, '-o')
plt.plot(f, phase_mod)
plt.xscale('log')
plt.show()

lcr.make_corr_open(20, 200e3)

lcr.make_bode_plot(f, Z, phase)

toc = time.time()
lcr.measure('ZTD')
print(time.time() - toc)

n = 200
Zs = np.zeros(n)
phases = np.zeros(n)
for i in tqdm(range(n)):
    Zs[i], phases[i] = lcr.measure('ZTD')

Zs1, phases1 = np.loadtxt('fast-med-slow/capacitor_R_.47F_29kOhm_1V_1kHz_MED.csv', delimiter=',', unpack=True, skiprows=2)
Zs2, phases2 = np.loadtxt('fast-med-slow/capacitor_R_.47F_29kOhm_1V_1kHz_SLOW.csv', delimiter=',', unpack=True, skiprows=2)
Zs3, phases3 = np.loadtxt('fast-med-slow/capacitor_R_.47F_29kOhm_1V_1kHz_FAST.csv', delimiter=',', unpack=True, skiprows=2)


plt.plot(Zs1)
plt.plot(Zs2)
plt.plot(Zs3)
plt.plot(Zs)
plt.plot(Z_ALC)
plt.show()
save_csv(Zs, phases, filename='capacitor_R_.47F_29kOhm_1V_1kHz_MED-ALC', root='./fast-med-slow/', delimiter=',', header='Capacitor de 0.47 nF en serie con resistencia de 29 kOhm. Frecuencia fija en 1 kHz \n Z [Ohm], Fase [°]')

f_1, Z_1, phase_1 = np.loadtxt('probe-station/muestra-Au-Au-(14-24).csv', delimiter=',', unpack=True, skiprows=1)
lcr.make_bode_plot(f_1, Z_1, phase_1)


