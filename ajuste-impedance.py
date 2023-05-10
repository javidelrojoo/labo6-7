# -*- coding: utf-8 -*-
from impedance.models.circuits import CustomCircuit
import matplotlib.pyplot as plt
import numpy as np

path = 'Tonghui TH283X/results/probe-station/26-4/'
filename = 'Al-Au-(C5-C6)-400mV'
# f, Z, phase = np.loadtxt('circuito_memristor/circuito1.csv', delimiter=',', unpack=True, skiprows=1)
f, Z, phase = np.loadtxt(f'{path}{filename}.csv', delimiter=',', unpack=True, skiprows=1)
# f_err = 0.01/100 * f
# Z_err, phase_err = Z*3/100, phase*3/100


circuit_str = 'p(R3-p(R1,C1)-p(R2,C2),C3)'
# circuit_str = ''

# initial_guess = [56.07, 10.31e6, 464.09e-9, 13.05e3, 449.95e-9, 4.54e-12]
initial_guess = [56.07, 10.31e6, 464.09e-9, 13.05e3, 449.95e-9]
# initial_guess = [50, 1e-7, 1e3, 1e-7]

circuit = CustomCircuit(circuit_str, initial_guess=initial_guess, constants={'C3':4.54e-12})

Z_re = Z*np.cos(phase*np.pi/180)
Z_im = Z*np.sin(phase*np.pi/180)
Z = Z_re + 1j*Z_im

circuit.fit(f, Z)
print(circuit)
Z_fit = circuit.predict(f)


fig, axs = plt.subplots(2, 1, sharex=True)

axs[0].errorbar(f, np.abs(Z)*1e-3, xerr=f_err, yerr=Z_err*1e-3, color='C0', linestyle='None', marker='o', capsize=5, markevery=15, errorevery=15, label='Datos')
# axs[0].plot(f, np.abs(Z_fit)*1e-3, 'r')
axs[0].set_ylabel('Impedancia [k$\Omega$]')
axs[0].set_xscale('log')
axs[0].grid()

axs[1].errorbar(f, np.angle(Z, deg=True), xerr=f_err, yerr=phase_err, color='C0', linestyle='None', marker='o', capsize=5, markevery=15, errorevery=15, label='Datos')
# axs[1].plot(f, np.angle(Z_fit, deg=True), 'r')
axs[1].set_ylabel('Fase [°]')
axs[1].set_xlabel('Frecuencia [Hz]')
axs[1].grid()

plt.tight_layout()
# plt.savefig('graficos/bode-resistencia-pura-con-picos-feos.png', dpi=400)
plt.show()