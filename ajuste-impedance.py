# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 16:07:02 2023

@author: Charly
"""
from impedance.models.circuits import CustomCircuit
import matplotlib.pyplot as plt
from save_csv import save_csv
import numpy as np

f, Z, phase = np.loadtxt('circuito_memristor/circuito1.csv', delimiter=',', unpack=True, skiprows=1)
# frequencies, Z = preprocessing.readCSV('circuito_memristor/circuito1.csv')

circuit_str = 'p(R3-p(R1,C1)-p(R2,C2),C3)'
# initial_guess = [56.07, 10.31e6, 464.09e-9, 13.05e3, 449.95e-9, 4.54e-12]
initial_guess = [50, 1e-7, 1e3, 1e-7]

circuit = CustomCircuit(circuit_str, initial_guess=initial_guess, constants={'C3':4.54e-12, 'R1':10.31e6})

Z_re = Z*np.cos(phase*np.pi/180)
Z_im = Z*np.sin(phase*np.pi/180)
Z = Z_re + 1j*Z_im

circuit.fit(f, Z)
print(circuit)
Z_fit = circuit.predict(f)

plt.plot(f, np.abs(Z), 'o')
plt.plot(f, np.abs(Z_fit))
plt.xscale('log')
plt.grid()
plt.show()

plt.figure()
plt.plot(f, np.angle(Z, deg=True), 'o')
plt.plot(f, np.angle(Z_fit, deg=True))
plt.xscale('log')
plt.grid()
plt.show()