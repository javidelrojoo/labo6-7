import pyvisa
import numpy as np
import matplotlib.pyplot as plt
from save_csv import save_csv
from tqdm import tqdm
from TonghuiTH283X import TH283X

lcr = TH283X('USB0::0x0471::0x2827::QF40900001::INSTR')

lcr.set_freq(1e3)
lcr.get_freq()

lcr.set_volt(0.6)
lcr.get_volt()

lcr.measure('ZTD')

lcr._lcr.query('*OPC?')
lcr._lcr.write('*OPC')
lcr._lcr.query('FETC?')

frecs = np.logspace(np.log10(20), np.log10(2e5), 500)
# frecs = np.linspace(10e3, 2e5, 250)
f, Z, phase = lcr.make_EI(frecs, 'ZTD')

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


lcr.make_bode_plot(f, Z, phase)


save_csv(f, Z, phase, filename='resistencia_10mOhm_correccion a 75Hz', root='resistencia/', delimiter=',', header='Frecuencia [Hz], Z [Ohm], Fase [°]')

n = 100
Zs = np.zeros(n)
phases = np.zeros(n)
for i in tqdm(range(n)):
    Zs[i], phases[i] = lcr.measure('ZTD')

plt.plot(Zs1)
plt.plot(Zs2)
plt.plot(Zs)
plt.show()
save_csv(f, Z, phase, filename='capacitor_R_.47F_29kOhm_1V_1kHz_SLOW', root='./fast-med-slow/', delimiter=',', header='Capacitor de 0.47 nF en serie con resistencia de 29 kOhm. Frecuencia fija en 1 kHz \n Z [Ohm], Fase [°]')

data = np.loadtxt('bode_capacitor/capacitor_R_.47F_29kOhm_1V_FAST.csv', delimiter=',', unpack=True, skiprows=2)
