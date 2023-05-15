# -*- coding: utf-8 -*-
from impedance.models.circuits import CustomCircuit
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from scipy.optimize import curve_fit

path = 'Tonghui TH283X/results/probe-station/26-4/'
filename = 'Al-Au-(F1-F2)-400mV'

# f, Z, phase = np.loadtxt('circuito_memristor/circuito1.csv', delimiter=',', unpack=True, skiprows=1)
f, Z, phase = np.loadtxt(f'{path}{filename}.csv', delimiter=',', unpack=True, skiprows=1)
# f_err = 0.01/100 * f
# Z_err, phase_err = Z*3/100, phase*3/100


# # circuit_str = 'p(R3-p(R1,C1)-p(R2,C2),C3)'
# circuit_str = 'p(C1,R1)-R3'

# # initial_guess = [56.07, 10.31e6, 464.09e-9, 13.05e3, 449.95e-9, 4.54e-12]
# # initial_guess = [56.07, 10.31e6, 464.09e-9, 13.05e3, 449.95e-9]
# # initial_guess = [50, 1e-7, 1e3, 1e-7]
# initial_guess = [4e-10, 170e3, 1.6e3]
# # initial_guess = [1, 10e6]

# circuit = CustomCircuit(circuit_str, initial_guess=initial_guess) #, constants={'C3':4.54e-12}

Z_re = Z*np.cos(phase*np.pi/180)
Z_im = Z*np.sin(phase*np.pi/180)
Z = Z_re + 1j*Z_im

# circuit.fit(f, Z, global_opt=True) #, sigma=np.hstack([Z.real*3/100, Z.imag*3/100]), absolute_sigma=True
# print(circuit)
# Z_fit = circuit.predict(f)


def Z_circuit(f, C1, R1, R3):
    w = 2*np.pi*f
    Z = 1/(1/R1 + 1j*w*C1) + R3 #+ 1/(1/R2 + 1j*w*C2)
    return np.hstack([Z.real, Z.imag])

print('Please wait...')
p0 = np.array([4e-10, 170e3, 500])
popt, pcov = curve_fit(Z_circuit, f, np.hstack([Z_re, Z_im]), p0=p0, bounds=(0, np.inf))
print(popt)
if sum(np.sqrt((p0-popt)**2))==0:
    print('No ajustó nada')
Z_fit = Z_circuit(f, *popt)
Z_fit = Z_fit[:int(len(Z_fit)/2)] + 1j*Z_fit[int(len(Z_fit)/2):]

plt.close('all')
fig, axs = plt.subplots(2, 1, sharex=True)

axs[0].scatter(f, np.abs(Z)*1e-3, color='C0', label='Datos')
axs[0].plot(f, np.abs(Z_fit)*1e-3, 'r')
axs[0].set_ylabel('Impedancia [k$\Omega$]')
axs[0].set_xscale('log')
axs[0].grid()

axs[1].scatter(f, np.angle(Z, deg=True), color='C0', label='Datos')
axs[1].plot(f, np.angle(Z_fit, deg=True), 'r')
axs[1].set_ylabel('Fase [°]')
axs[1].set_xlabel('Frecuencia [Hz]')
axs[1].grid()

plt.tight_layout()
# plt.savefig('graficos/bode-resistencia-pura-con-picos-feos.png', dpi=400)

plt.figure()
plt.scatter(np.real(Z)*1e-3, -np.imag(Z)*1e-3, c=f, cmap='cool', norm=LogNorm())
plt.plot(np.real(Z_fit)*1e-3, -np.imag(Z_fit)*1e-3, 'k')
plt.xlabel('Re(Z) [k$\Omega$]')
plt.ylabel('Im(Z) [k$\Omega$]')
plt.grid()
plt.colorbar(label='Frecuencia [Hz]')

plt.show()
