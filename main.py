import pyvisa
import numpy as np
import matplotlib.pyplot as plt
from save_csv import save_csv
from tqdm import tqdm
from TonghuiTH283X import TH283X
import time

lcr = TH283X('USB0::0x0471::0x2827::QF40900001::INSTR')

lcr.set_freq(1e3)
lcr.get_freq()

lcr.set_volt(0.4)
lcr.get_volt()

lcr.measure('ZTD')

lcr._lcr.query('*OPC?')
lcr._lcr.write('*OPC')
lcr._lcr.query('FETC?')

frecs = np.logspace(np.log10(20), np.log10(2e5), 500)
# frecs = np.linspace(10e3, 2e5, 250)
f, Z, phase = lcr.make_EI(frecs, 'ZTD')
save_csv(f, Z, phase, filename='Al-Au-(E7-E8)-400mV-2', root='probe-station/26-4/', delimiter=',', header='Frecuencia [Hz], Z [Ohm], Fase [°]')


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


