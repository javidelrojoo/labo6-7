import pyvisa
import numpy as np
import matplotlib.pyplot as plt
from save_csv import save_csv
from TonghuiTH283X import TH283X

lcr = TH283X('USB0::0x0471::0x2827::QF40900001::INSTR')

lcr.set_freq(20)
lcr.get_freq()

lcr.set_volt(0.6)
lcr.get_volt()

lcr.measure('ZTD')

lcr._lcr.query('*OPC?')
lcr._lcr.write('*OPC')
lcr._lcr.query('FETC?')

frecs = np.logspace(np.log10(20), np.log10(2e5), 500)
f, Z, phase = lcr.make_EI(frecs, 'ZTD')



plt.plot(f, 20*np.log10(Z), '-o')
plt.xscale('log')
plt.figure()
plt.plot(f, -phase, '-o')
plt.xscale('log')
plt.show()


save_csv(f, Z, phase, filename='capacitor_.47F_1V', root='./bode_capacitor/', delimiter=',', header='Frecuencia [Hz], Z [Ohm], Fase [°]')


frecs = np.logspace(np.log10(20), np.log10(2e5), 1000)
frecs_lcr = np.zeros(1000)

for i, f in enumerate(frecs):
    lcr.set_freq(f)
    frecs_lcr[i] = lcr.get_freq()

plt.plot(frecs, frecs_lcr)
plt.show()

save_csv(frecs, frecs_lcr, filename='frecuencia-LCR', root='Caracterización/', header='Frecuencia que pedimos vs frecuencia que manda \n Frecuencia pedida [Hz], Frecuencia LCR [Hz]')



