import numpy as np
import matplotlib.pyplot as plt

#########################
#FIGURA 1
#########################
frecs = np.logspace(2, np.log10(2e5), 100)
Cs, D = np.loadtxt('pruebas\\capacitor_.47uF.csv', delimiter=',', unpack=True, skiprows=2)

fig, axs = plt.subplots(2, 1, sharex=True)

axs[0].plot(frecs, Cs*1e9, 'C0')
axs[0].set_ylabel('Capacitancia en serie (Cs) [nF]')
axs[0].set_xscale('log')
axs[0].grid()

axs[1].plot(frecs, D, 'C1')
axs[1].set_ylabel('Factor disipativo (D)')
axs[1].set_xlabel('Frecuencia [Hz]')
axs[1].grid()

plt.tight_layout()
plt.savefig('graficos/Cs-D-capacitor.47uF.png', dpi=400)
plt.show()


#########################
#FIGURA 2
#########################
frecs = np.logspace(2, np.log10(2e5), 1000)
f, Z, phase = np.loadtxt('pruebas\\capacitor_.47uF_bode.csv', delimiter=',', unpack=True, skiprows=1)

fig, axs = plt.subplots(2, 1, sharex=True)

axs[0].plot(frecs, 20*np.log10(Z), 'C0')
axs[0].set_ylabel('Ganancia [dB]')
axs[0].set_xscale('log')
axs[0].grid()

axs[1].plot(frecs, -phase, 'C1')
axs[1].set_ylabel('Fase [°]')
axs[1].set_xlabel('Frecuencia [Hz]')
axs[1].grid()

plt.tight_layout()
plt.savefig('graficos/bode-prueba-capacitor.47uF.png', dpi=400)
plt.show()

#########################
#FIGURA 3
#########################
f, Z, phase = np.loadtxt('bode_capacitor\\capacitor_.47uF_1V.csv', delimiter=',', unpack=True, skiprows=1)

fig, axs = plt.subplots(2, 1, sharex=True)

axs[0].plot(f, 20*np.log10(Z), 'C0')
axs[0].set_ylabel('Ganancia [dB]')
axs[0].set_xscale('log')
axs[0].grid()

axs[1].plot(f, -phase, 'C1')
axs[1].set_ylabel('Fase [°]')
axs[1].set_xlabel('Frecuencia [Hz]')
axs[1].grid()

plt.tight_layout()
plt.savefig('graficos/bode-capacitor.47uF.png', dpi=400)
plt.show()