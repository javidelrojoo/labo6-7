#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm, LogNorm
import matplotlib.patheffects as pe
import os
#%%
from impedance.models.circuits import CustomCircuit
from impedance_grapher import bode_plot
#%%
def error_ZTD(fs, Zs, V):
    Ka = np.zeros_like(fs)
    Kb = np.zeros_like(fs)
    
    for i, (f, Z) in enumerate(zip(fs, Zs)):
        if f<100:
            Ka[i] = 1e-3/Z * (1 + 200/V) * (1 + np.sqrt(100/f))
            Kb[i] = Z*1e-9* (1-70/V) * (1 + np.sqrt(100/f))
        if 100<=f<=100e3:
            Ka[i] = 1e-3/Z * (1 + 200/V)
            Kb[i] = Z*1e-9* (1-70/V)
        if 100e3<f<=200e3:
            Ka[i] = 1e-3/Z * (2 + 200/V)
            Kb[i] = Z*3e-9* (1-70/V)
    
    Kc = 0.0003
    A = 0.35
    Ae = (A + (Ka + Kb + Kc)*100)
    return Ae * Zs/100, 180/np.pi * Ae/100
#%%
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

#########################
#FIGURA 4
#########################
def Z_RC(f, R, C):
    return np.abs(R + 1j/(f*2*np.pi*C))

def phase_RC(f, R, C):
    return np.angle(R + 1j/(f*2*np.pi*C), deg=True)

f, Z, phase = np.loadtxt('bode_capacitor\\capacitor_R_.47F_29kOhm_1V.csv', delimiter=',', unpack=True, skiprows=1)

f_err = 0.01/100 * f
Z_err, phase_err = error_ZTD(f, Z, 1)

popt_Z, pcov_Z = curve_fit(Z_RC, f, Z, p0 = [20e3, 500e-9], sigma=Z_err, absolute_sigma=True)
print(f'R = ({popt_Z[0]*1e-3} +/- {np.sqrt(np.diag(pcov_Z))[0]*1e-3}) kOhm \n C = ({popt_Z[1]*1e9} +/- {np.sqrt(np.diag(pcov_Z))[1]*1e9}) nF')

popt_phase, pcov_phase = curve_fit(phase_RC, f, -phase, p0 = [20e3, 500e-9], sigma=phase_err, absolute_sigma=True)
print(f'R = ({popt_phase[0]*1e-3} +/- {np.sqrt(np.diag(pcov_phase))[0]*1e-3}) kOhm \n C = ({popt_phase[1]*1e9} +/- {np.sqrt(np.diag(pcov_phase))[1]*1e9}) nF')

fig, axs = plt.subplots(2, 1, sharex=True)

axs[0].plot(f, Z_RC(f, *popt_Z)*1e-3, 'r', label='Ajuste')
axs[0].errorbar(f, Z*1e-3, xerr=f_err, yerr=Z_err*1e-3, color='C0', linestyle='None', marker='o', capsize=5, markevery=15, errorevery=15, label='Datos')
axs[0].set_ylabel('|Z| [k$\Omega$]')
axs[0].set_xscale('log')
axs[0].legend()
axs[0].grid()

axs[1].plot(f, phase_RC(f, *popt_phase), 'r', label='Ajuste')
axs[1].errorbar(f, -phase, xerr=f_err, yerr=phase_err, color='C0', linestyle='None', marker='o', capsize=5, markevery=15, errorevery=15, label='Datos')
axs[1].set_ylabel('Fase [°]')
axs[1].set_xlabel('Frecuencia [Hz]')
axs[1].grid()

plt.tight_layout()
plt.savefig('graficos/bode-capacitor.47F-resistencia29kOhm-ajuste.png', dpi=400)
plt.show()

#########################
#FIGURA 5
#########################

f1, Z1, phase1 = np.loadtxt('bode_capacitor\\capacitor_R_.47F_29kOhm_1V.csv', delimiter=',', unpack=True, skiprows=1)
f2, Z2, phase2 = np.loadtxt('bode_capacitor\\capacitor_R_.47F_29kOhm_1V_OPEN_SHORT.csv', delimiter=',', unpack=True, skiprows=1)

fig, axs = plt.subplots(2, gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

axs[0].plot(f1, Z1*1e-3, 'C0', label='Sin corrección', marker='v', markevery=15)
axs[0].plot(f2, Z2*1e-3, 'r', label='OPEN y SHORT', marker='^', markevery=20)
axs[0].set_ylabel('|Z| [k$\Omega$]')
axs[0].set_xscale('log')
axs[0].legend()
axs[0].grid()

axs[1].plot(f, np.abs(Z1-Z2), 'g')
axs[1].set_ylabel('Diferencia [$\Omega$]')
axs[1].set_xlabel('Frecuencia [Hz]')
axs[1].grid()

plt.tight_layout()
plt.savefig('graficos/diferencia-correciones.png', dpi=400)
plt.show()

#########################
#FIGURA 6
#########################

fm, Zm, phasem = np.loadtxt('bode_capacitor\\capacitor_R_.47F_29kOhm_1V.csv', delimiter=',', unpack=True, skiprows=1)
fs, Zs, phases = np.loadtxt('bode_capacitor\\capacitor_R_.47F_29kOhm_1V_FAST.csv', delimiter=',', unpack=True, skiprows=1)
ff, Zf, phasef = np.loadtxt('bode_capacitor\\capacitor_R_.47F_29kOhm_1V_SLOW.csv', delimiter=',', unpack=True, skiprows=1)

fig, axs = plt.subplots(2, gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

axs[0].plot(fm, Zm*1e-3, 'C0', label='MED', marker='v', markevery=15)
axs[0].plot(fs, Zs*1e-3, 'r', label='SLOW', marker='^', markevery=20)
axs[0].plot(ff, Zf*1e-3, 'g', label='FAST', marker='<', markevery=20)
axs[0].set_ylabel('|Z| [k$\Omega$]')
axs[0].set_xscale('log')
axs[0].legend()
axs[0].grid()

axs[1].plot(f, np.abs(Zm-Zs), 'r')
axs[1].plot(f, np.abs(Zm-Zf), 'g')
axs[1].set_ylabel('Diferencia [$\Omega$]')
axs[1].set_xlabel('Frecuencia [Hz]')
axs[1].grid()

plt.tight_layout()
plt.savefig('graficos/diferencia-fast-med-slow.png', dpi=400)
plt.show()

#########################
#FIGURA 7
#########################
# Los datos se guardaron mal
Zm, phasem = np.loadtxt('fast-med-slow\\capacitor_R_.47F_29kOhm_1V_1kHz_MED.csv', delimiter=',', unpack=True, skiprows=1)
Zs, phases = np.loadtxt('fast-med-slow\\capacitor_R_.47F_29kOhm_1V_1kHz_SLOW.csv', delimiter=',', unpack=True, skiprows=1)
Zf, phasef = np.loadtxt('fast-med-slow\\capacitor_R_.47F_29kOhm_1V_1kHz_FAST.csv', delimiter=',', unpack=True, skiprows=1)

plt.plot(Zm, label='MED')
plt.plot(Zs, label='SLOW')
plt.plot(Zf, label='FAST')
plt.legend()
plt.show()

plt.hist(Zf, color = 'g', edgecolor = 'g', label='FAST', alpha=0.7)
plt.hist(Zm, color = 'C0', edgecolor = 'C0', label='MED', alpha=0.7)
plt.hist(Zs, color = 'r', edgecolor = 'r', label='SLOW', alpha=0.7)
plt.xlabel('Impedancia [$\Omega$]')
plt.grid(alpha=0.1)
plt.legend()
plt.savefig('graficos/hist-fast-med-slow.png', dpi=400)
plt.show()

print(f'FAST: {np.mean(Zf)} +/- {np.std(Zf)}\n MED: {np.mean(Zm)} +/- {np.std(Zm)}\n SLOW: {np.mean(Zs)} +/- {np.std(Zs)}\n')

#########################
#FIGURA 8
#########################

f, Z, phase = np.loadtxt('resistencia\\resistencia_10mOhm_correccion a 75Hz.csv', delimiter=',', unpack=True, skiprows=1)

fig, axs = plt.subplots(2, 1, sharex=True)

axs[0].plot(f, Z*1e-6, 'C0')
axs[0].set_ylabel('Impedancia [M$\Omega$]')
axs[0].set_xscale('log')
axs[0].grid()

axs[1].plot(f, phase, 'C1')
axs[1].set_ylabel('Fase [°]')
axs[1].set_xlabel('Frecuencia [Hz]')
axs[1].grid()

plt.tight_layout()
plt.savefig('graficos/bode-resistencia-pura-con-picos-feos.png', dpi=400)
plt.show()


#########################
#FIGURA 9
#########################

def Z_RC(f, R, C):
    return 1/(np.sqrt(C**2*f**2+1/R**2))

def phase_RC(f, R, C):
    w = 2*np.pi*f
    return -w*C*R**2/(1+C**2 * w**2 * R**2)

f, Z, phase = np.loadtxt('resistencia\\resistencia_10mOhm_sincorrecciones.csv', delimiter=',', unpack=True, skiprows=1)

f_err = 0.01/100 * f
Z_err, phase_err = Z*3/100, phase/100

popt_Z, pcov_Z = curve_fit(Z_RC, f, Z, p0 = [1e7, 4.5e-12], sigma=Z_err, absolute_sigma=True)
print(f'R = ({popt_Z[0]*1e-6} +/- {np.sqrt(np.diag(pcov_Z))[0]*1e-6}) MOhm \n C = ({popt_Z[1]*1e12} +/- {np.sqrt(np.diag(pcov_Z))[1]*1e12}) pF')

popt_phase, pcov_phase = curve_fit(phase_RC, f, phase, p0 = [*popt_Z], sigma=phase_err, absolute_sigma=True)
print(f'R = ({popt_phase[0]*1e-3} +/- {np.sqrt(np.diag(pcov_phase))[0]*1e-3}) kOhm \n C = ({popt_phase[1]*1e9} +/- {np.sqrt(np.diag(pcov_phase))[1]*1e9}) nF')

plt.plot(f, Z_RC(f, *popt_Z)*1e-6, 'r', label='Ajuste')
plt.errorbar(f, Z*1e-6, xerr=f_err, yerr=Z_err*1e-6, color='C0', linestyle='None', marker='o', capsize=5, markevery=15, errorevery=15, label='Datos')
plt.ylabel('|Z| [M$\Omega$]')
plt.xlabel('Frecuencia [Hz]')
plt.xscale('log')
plt.legend()
plt.grid()
plt.savefig('graficos/impedancia-resistencia-pura.png', dpi=400)
plt.show()

#########################
#FIGURA 10
#########################
def Z_RL(f, R, L):
    w = 2*np.pi*f
    return np.sqrt(R**2 + (w*L)**2)


f, Z, phase = np.loadtxt('Caracterización\\medicion_corto.csv', delimiter=',', unpack=True, skiprows=1)

f_err = 0.01/100 * f
Z_err, phase_err = Z*3/100, phase*3/100

popt_Z, pcov_Z = curve_fit(Z_RL, f, Z, p0 = [0, 0], sigma=Z_err, absolute_sigma=True)
print(f'R = ({popt_Z[0]*1e3} +/- {np.sqrt(np.diag(pcov_Z))[0]*1e3}) mOhm \n L = ({popt_Z[1]*1e9} +/- {np.sqrt(np.diag(pcov_Z))[1]*1e9}) nH')

popt_phase, pcov_phase = curve_fit(phase_RC, f, phase, p0 = [*popt_Z], sigma=phase_err, absolute_sigma=True)
print(f'R = ({popt_phase[0]*1e-3} +/- {np.sqrt(np.diag(pcov_phase))[0]*1e-3}) kOhm \n C = ({popt_phase[1]*1e9} +/- {np.sqrt(np.diag(pcov_phase))[1]*1e9}) nF')

plt.plot(f, Z_RL(f, *popt_Z), 'r', label='Ajuste')
plt.errorbar(f, Z, xerr=f_err, yerr=Z_err, color='C0', linestyle='None', marker='o', capsize=5, markevery=15, errorevery=15, label='Datos')
plt.ylabel('|Z| [$\Omega$]')
plt.xlabel('Frecuencia [Hz]')
plt.xscale('log')
plt.legend()
plt.grid()
plt.savefig('graficos/impedancia-en-corto.png', dpi=400)
plt.show()

#########################
#FIGURA 12 (La 11 es del circuito)
#########################

f, Z, phase = np.loadtxt('circuito_memristor/circuito1.csv', delimiter=',', unpack=True, skiprows=1)
f_err = 0.01/100 * f
Z_err, phase_err = Z*3/100, phase*3/100


circuit_str = 'p(R3-p(R1,C1)-p(R2,C2),C3)'
# initial_guess = [56.07, 10.31e6, 464.09e-9, 13.05e3, 449.95e-9, 4.54e-12]
initial_guess = [56.07, 10.31e6, 464.09e-9, 13.05e3, 449.95e-9]
# initial_guess = [50, 1e-7, 1e3, 1e-7]

circuit = CustomCircuit(circuit_str, initial_guess=initial_guess, constants={'C3':4.54e-12})

Z_re = Z*np.cos(phase*np.pi/180)
Z_im = Z*np.sin(phase*np.pi/180)
Z = Z_re + 1j*Z_im

circuit.fit(f, Z, sigma=np.hstack([Z.real*3/100, Z.imag*3/100]), absolute_sigma=True)
print(circuit)
Z_fit = circuit.predict(f)


fig, axs = plt.subplots(2, 1, sharex=True)

axs[0].errorbar(f, np.abs(Z)*1e-3, xerr=f_err, yerr=Z_err*1e-3, color='C0', linestyle='None', marker='o', capsize=5, markevery=15, errorevery=15, label='Datos')
axs[0].plot(f, np.abs(Z_fit)*1e-3, 'r')
axs[0].set_ylabel('Impedancia [k$\Omega$]')
axs[0].set_xscale('log')
axs[0].grid()

axs[1].errorbar(f, np.angle(Z, deg=True), xerr=f_err, yerr=phase_err, color='C0', linestyle='None', marker='o', capsize=5, markevery=15, errorevery=15, label='Datos')
axs[1].plot(f, np.angle(Z_fit, deg=True), 'r')
axs[1].set_ylabel('Fase [°]')
axs[1].set_xlabel('Frecuencia [Hz]')
axs[1].grid()

plt.tight_layout()
plt.savefig('graficos/ajuste-circuito1.png', dpi=400)
plt.show()

#########################
#FIGURA 13
#########################

f, Z, phase = np.loadtxt('circuito_memristor/circuito2.csv', delimiter=',', unpack=True, skiprows=1)
f_err = 0.01/100 * f
Z_err, phase_err = Z*3/100, phase*3/100


circuit_str = 'p(R3-p(R1,C1)-p(R2,C2),C3)'
initial_guess = [56.07, 236, 464.09e-9, 55.8, 449.95e-9]

circuit = CustomCircuit(circuit_str, initial_guess=initial_guess, constants={'C3':4.54e-12})

Z_re = Z*np.cos(phase*np.pi/180)
Z_im = Z*np.sin(phase*np.pi/180)
Z = Z_re + 1j*Z_im

circuit.fit(f, Z, sigma=np.hstack([Z.real*3/100, Z.imag*3/100]), absolute_sigma=True)
print(circuit)
Z_fit = circuit.predict(f)


fig, axs = plt.subplots(2, 1, sharex=True)

axs[0].errorbar(f, np.abs(Z), xerr=f_err, yerr=Z_err, color='C0', linestyle='None', marker='o', capsize=5, markevery=15, errorevery=15, label='Datos')
axs[0].plot(f, np.abs(Z_fit), 'r')
axs[0].set_ylabel('Impedancia [$\Omega$]')
axs[0].set_xscale('log')
axs[0].grid()

axs[1].errorbar(f, np.angle(Z, deg=True), xerr=f_err, yerr=phase_err, color='C0', linestyle='None', marker='o', capsize=5, markevery=15, errorevery=15, label='Datos')
axs[1].plot(f, np.angle(Z_fit, deg=True), 'r')
axs[1].set_ylabel('Fase [°]')
axs[1].set_xlabel('Frecuencia [Hz]')
axs[1].grid()

plt.tight_layout()
plt.savefig('graficos/ajuste-circuito2.png', dpi=400)
plt.show()

#########################
#FIGURA 14
#########################

f, Z, phase = np.loadtxt('circuito_memristor/circuito3.csv', delimiter=',', unpack=True, skiprows=1)
f_err = 0.01/100 * f
Z_err, phase_err = Z*3/100, phase*3/100


circuit_str = 'p(R3-p(R1,C1)-p(R2,C2),C3)'
initial_guess = [56.07, 1.7e3, 464.09e-9, 112.4e3, 449.95e-9]

circuit = CustomCircuit(circuit_str, initial_guess=initial_guess, constants={'C3':4.54e-12})

Z_re = Z*np.cos(phase*np.pi/180)
Z_im = Z*np.sin(phase*np.pi/180)
Z = Z_re + 1j*Z_im

circuit.fit(f, Z, sigma=np.hstack([Z.real*3/100, Z.imag*3/100]), absolute_sigma=True)
print(circuit)
Z_fit = circuit.predict(f)


fig, axs = plt.subplots(2, 1, sharex=True)

axs[0].errorbar(f, np.abs(Z)*1e-3, xerr=f_err, yerr=Z_err*1e-3, color='C0', linestyle='None', marker='o', capsize=5, markevery=15, errorevery=15, label='Datos')
axs[0].plot(f, np.abs(Z_fit)*1e-3, 'r')
axs[0].set_ylabel('Impedancia [k$\Omega$]')
axs[0].set_xscale('log')
axs[0].grid()

axs[1].errorbar(f, np.angle(Z, deg=True), xerr=f_err, yerr=phase_err, color='C0', linestyle='None', marker='o', capsize=5, markevery=15, errorevery=15, label='Datos')
axs[1].plot(f, np.angle(Z_fit, deg=True), 'r')
axs[1].set_ylabel('Fase [°]')
axs[1].set_xlabel('Frecuencia [Hz]')
axs[1].grid()

plt.tight_layout()
plt.savefig('graficos/ajuste-circuito3.png', dpi=400)
plt.show()

#########################
#FIGURA 17, 18, 19, 20
#########################

for filename in os.listdir('probe-station')[2:3]:
    f, Z, phase = np.loadtxt('probe-station/' + filename, delimiter=',', unpack=True, skiprows=1)
    print(filename)
    bode_plot(f, Z*1e-3, phase, ylabel1='Impedancia [k$\Omega$]', savefig='graficos/bode-85-Au-Au-(C2-D1)-400mV.png')


#########################
#FIGURA 22
#########################

def lineal(x, a, b):
    return x*a + b

t, V, I = np.loadtxt('K2612B/results/prueba-resistencia14k.csv', delimiter=',', unpack=True, skiprows=2)

Verr = V*8/1000
Ierr = np.array([i*45/1000 if i>90e-9 else i*430/1000 for i in I])

popt, pcov = curve_fit(lineal, V, I, sigma=Ierr, absolute_sigma=True)

R = 1/popt[0]
Rerr = np.sqrt(np.sqrt(np.diag(pcov))[0]**2/R**4)
print(f'R = {R} +/- ')

plt.errorbar(V, I*1e6, xerr=Verr, yerr=Ierr*1e6, fmt='o', capsize=2, label='Datos')
plt.plot(V, lineal(V, *popt)*1e6, 'r', zorder=3, label='Ajuste')
plt.xlabel('Voltaje [V]')
plt.ylabel('Corriente [$\mu$A]')
plt.grid()
plt.legend()
plt.savefig('graficos/SMU-prueba-resistencia14k.png', dpi=400)
plt.show()

#########################
#FIGURA 23
#########################

t, V, I = np.loadtxt('K2612B/results/Al-Au(C1-D2)-ida.csv', delimiter=',', unpack=True, skiprows=2)
plt.plot(V, np.abs(I)*1e6, '-o', label='Datos ida')

t, V, I = np.loadtxt('K2612B/results/Al-Au(C1-D2)-vuelta.csv', delimiter=',', unpack=True, skiprows=2)
plt.plot(V, np.abs(I)*1e6, '-o', label='Datos vuelta')

plt.xlabel('Voltaje [V]')
plt.ylabel('Corriente [$\mu$A]')
plt.grid()
plt.legend()
plt.savefig('graficos/SMU-Al-Au(C1-D2)-ida-vuelta.png', dpi=400)
plt.show()

#########################
#FIGURA 24
#########################

def lineal(x, a, b):
    return x*a + b

t, V, I = np.loadtxt('K2612B/results/Au-Au(C2-D2)-ida.csv', delimiter=',', unpack=True, skiprows=2)

Verr = V*8/1000
Ierr = np.array([i*45/1000 if i>90e-9 else i*430/1000 for i in I])

popt, pcov = curve_fit(lineal, V, I, sigma=Ierr, absolute_sigma=True)

R = 1/popt[0]
Rerr = np.sqrt(np.sqrt(np.diag(pcov))[0]**2/R**4)
print(f'R = {R} +/- ')

plt.errorbar(V, I*1e6, xerr=Verr, yerr=Ierr*1e6, fmt='o', capsize=2, label='Datos')
plt.plot(V, lineal(V, *popt)*1e6, 'r', zorder=3, label='Ajuste')
plt.xlabel('Voltaje [V]')
plt.ylabel('Corriente [$\mu$A]')
plt.grid()
plt.legend()
plt.savefig('graficos/Au-Au(C2-D2)-ida.png', dpi=400)
plt.show()

#########################
#FIGURA 25
#########################

t, V, I = np.loadtxt('K2612B/results/Al-Au(C2-D1)-ida.csv', delimiter=',', unpack=True, skiprows=2)
plt.plot(V, np.abs(I)*1e6, '-o', label='Datos ida')

t, V, I = np.loadtxt('K2612B/results/Al-Au(C2-D1)-vuelta.csv', delimiter=',', unpack=True, skiprows=2)
plt.plot(V, np.abs(I)*1e6, '-o', label='Datos vuelta')

plt.xlabel('Voltaje [V]')
plt.ylabel('Corriente [$\mu$A]')
plt.grid()
plt.legend()
plt.savefig('graficos/SMU-Al-Au(C2-D1)-ida-vuelta.png', dpi=400)
plt.show()

#########################
#FIGURA 28
#########################

t, V, I = np.loadtxt('Keithley K2612B/results/Al-Au(F1-F2)-baja.csv', delimiter=',', unpack=True, skiprows=2)

fig, ax = plt.subplots()

points = np.array([V, abs(I)]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
# Create a continuous norm to map from data points to colors
norm = plt.Normalize(t.min(), t.max())
lc = LineCollection(segments, cmap='cool', norm=norm) #, linestyles='dashed'
# Set the values used for colormapping
lc.set_array(t)
lc.set_linewidth(2)
line = ax.add_collection(lc)
fig.colorbar(line, ax=ax, label='Tiempo [s]')
ax.set_xlabel('Voltaje [V]')
ax.set_ylabel('Corriente [A]')
ax.set_xlim(V.min()*1.1, V.max()*1.1)
ax.set_ylim(abs(I).min()*0.7, abs(I).max()*1.5)
ax.scatter(V, abs(I), label='Datos ida', c=t, cmap='cool')
ax.grid()
ax.set_yscale('log')
plt.savefig('graficos/Al-Au(F1-F2)-baja.png', dpi=400)
plt.show()

#########################
#FIGURA 29
#########################
dir = 'Tonghui TH283X/results/probe-station/26-4/'
for filename in os.listdir(dir):
    frec, Z, phase = np.loadtxt(dir + filename, delimiter=',', unpack=True, skiprows=1)

    Z_re = Z * np.cos(phase*np.pi/180)
    Z_im = Z * np.sin(phase*np.pi/180)
    plt.scatter(Z_re*1e-3, Z_im*1e-3, c=frec, cmap='cool', norm=LogNorm())
    plt.xlabel('Re(Z) [k$\Omega$]')
    plt.ylabel('Im(Z) [k$\Omega$]')
    plt.colorbar(label='Frecuencia [Hz]')
    plt.grid()
    # plt.figure()
    # plt.title(filename)
    # plt.plot(frec, Z*1e-3, 'o')
    # plt.xscale('log')
    # plt.xlabel('Frecuencia [Hz]')
    # plt.ylabel('Impedancia [k$\Omega$]')
    # plt.grid()
    plt.savefig('graficos/26-4 ' + filename.split('.csv')[0] + '.png', dpi=400)
    plt.show()

fig, ax = plt.subplots()

points = np.array([V, abs(I)]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
# Create a continuous norm to map from data points to colors
norm = plt.Normalize(t.min(), t.max())
lc = LineCollection(segments, cmap='cool', norm=norm) #, linestyles='dashed'
# Set the values used for colormapping
lc.set_array(t)
lc.set_linewidth(2)
line = ax.add_collection(lc)
fig.colorbar(line, ax=ax, label='Tiempo [s]')
ax.set_xlabel('Voltaje [V]')
ax.set_ylabel('Corriente [A]')
ax.set_xlim(V.min()*1.1, V.max()*1.1)
ax.set_ylim(abs(I).min()*0.7, abs(I).max()*1.5)
ax.scatter(V, abs(I), label='Datos ida', c=t, cmap='cool')
ax.grid()
ax.set_yscale('log')
# plt.savefig('graficos/Al-Au(F1-F2)-baja.png', dpi=400)
plt.show()

#########################
#FIGURA 42-47
#########################
#%%
plt.close('all')
path = 'Tonghui TH283X/results/probe-station/17-5/'
file = 'Al-Au(F5-F6)'

# f, Z, phase = np.loadtxt(f'{path}{file}-bias0-level0.4.csv', delimiter=',', unpack=True, skiprows=1)
f, Z, phase = np.loadtxt(f'{path}{file}-level0.4-bias0.csv', delimiter=',', unpack=True, skiprows=1)


fig, axs = plt.subplots(4, 2, sharex=True, figsize=(12,8))

axs[0][0].set_title('Bias 0V')
axs[0][0].plot(f, np.abs(Z), 'C0')
axs[0][0].set_ylabel('Impedancia [$\Omega$]')
axs[0][0].set_xscale('log')
axs[0][0].grid()
axs[1][0].plot(f, phase, 'C1')
axs[1][0].set_ylabel('Fase [°]')
axs[1][0].grid()

f, Z, phase = np.loadtxt(f'{path}{file}-level0.4-bias5.csv', delimiter=',', unpack=True, skiprows=1)

axs[0][1].set_title('Bias 5V')
axs[0][1].plot(f, np.abs(Z), 'C0')
axs[0][1].set_ylabel('Impedancia [$\Omega$]')
axs[0][1].set_xscale('log')
axs[0][1].grid()
axs[1][1].plot(f, phase, 'C1')
axs[1][1].set_ylabel('Fase [°]')
axs[1][1].grid()

f, Z, phase = np.loadtxt(f'{path}{file}-level0.4-bias0-2.csv', delimiter=',', unpack=True, skiprows=1)

axs[2][0].set_title('Bias 0V')
axs[2][0].plot(f, np.abs(Z), 'C0')
axs[2][0].set_ylabel('Impedancia [$\Omega$]')
axs[2][0].set_xscale('log')
axs[2][0].grid()
axs[3][0].plot(f, phase, 'C1')
axs[3][0].set_ylabel('Fase [°]')
axs[3][0].grid()


f, Z, phase = np.loadtxt(f'{path}{file}-level0.4-bias-5.csv', delimiter=',', unpack=True, skiprows=1)

axs[2][1].set_title('Bias -5V')
axs[2][1].plot(f, np.abs(Z), 'C0')
axs[2][1].set_ylabel('Impedancia [$\Omega$]')
axs[2][1].set_xscale('log')
axs[2][1].grid()
axs[3][1].plot(f, phase, 'C1')
axs[3][1].set_ylabel('Fase [°]')
axs[3][1].grid()

axs[3][0].set_xlabel('Frecuencia [Hz]')
axs[3][1].set_xlabel('Frecuencia [Hz]')

plt.tight_layout()
plt.savefig(f'graficos/17-5/{file}-bias.png', dpi=400)
plt.show()
#%%

plt.close('all')
path = './results/Tonghui/29-5/'
file = 'Al-Au(D5-D6)-level0.4'
biases = [0, 3, 5, 3, 0]

fig, axs = plt.subplots(6, 2, sharex=True, figsize=(12, 12))
for i, bias in enumerate(biases):
    f, Z, phase = np.loadtxt(f'{path}{file}-{i}-bias{bias}.csv', delimiter=',', unpack=True, skiprows=1)
    
    axs[i-i%2][i%2].set_title(f'{i+1} - Bias {bias}V')
    axs[i-i%2][i%2].plot(f, Z*1e-3, 'C0')
    axs[i-i%2][i%2].set_ylabel('Impedancia [k$\Omega$]')
    axs[i-i%2][i%2].set_xscale('log')
    axs[i-i%2][i%2].grid()
    
    axs[i-i%2+1][i%2].plot(f, phase, 'C1')
    axs[i-i%2+1][i%2].set_ylabel('Fase [°]')
    axs[i-i%2+1][i%2].grid()


axs[5][0].set_xlabel('Frecuencia [Hz]')
axs[3][1].set_xlabel('Frecuencia [Hz]')
axs[3][1].xaxis.set_tick_params(which='both', labelbottom=True)
axs[4][1].set_visible(False)
axs[5][1].set_visible(False)

plt.tight_layout()
plt.savefig(f'graficos/29-5/{file}.png', dpi=400)
plt.show()
#%%
plt.close('all')

#D5-D6 BIAS 0
files = ['results/Tonghui/4-26/Al-Au-(D5-D6)-400mV.csv',
          'results/Tonghui/5-17/Al-Au(D5-D6)-bias0-level0.4.csv',
          'results/Tonghui/5-17/Al-Au(D5-D6)-level0.4-bias0.csv',
          'results/Tonghui/5-17/Al-Au(D5-D6)-level0.4-bias0-2.csv',
          'results/Tonghui/5-29/Al-Au(D5-D6)-level0.4-0-bias0.csv',
          'results/Tonghui/5-29/Al-Au(D5-D6)-level0.4-4-bias0.csv',
          'results/Tonghui/5-29/Al-Au(D5-D6)-level0.4-pol-neg-0-bias0.csv',
          'results/Tonghui/5-29/Al-Au(D5-D6)-level0.4-pol-neg-4-bias0.csv'
          ]

labels = ['26-4',
          '17-5',
          '17-5 (2)',
          '17-5 post cycle',
          '29-5',
          '29-5 post cycle',
          '29-5 post cycle (2)',
          '29-5 post neg cycle']

# for i, file in enumerate(files):
#     plt.figure(1)
#     f, Z, phase = np.loadtxt(file, delimiter=',', unpack=True, skiprows=1)
#     plt.plot(f, Z, '--', label=f'D5-D6 {labels[i]}')
#     plt.figure(2)
#     plt.plot(f, phase, '--', label=f'D5-D6 {labels[i]}')

#F1-F2 BIAS 0
# files = ['results/Tonghui/4-26/Al-Au-(F1-F2)-400mV.csv',
#           'results/Tonghui/5-17/Al-Au(F1-F2)-level0.4-bias0.csv',
#           'results/Tonghui/5-17/Al-Au(F1-F2)-level0.4-bias0-2.csv',
#           'results/Tonghui/5-17/Al-Au(F1-F2)-2do-level0.4-bias0.csv',
#           'results/Tonghui/5-17/Al-Au(F1-F2)-2do-level0.4-bias0-2.csv',
#           'results/Tonghui/5-17/Al-Au(F1-F2)-3ro-level0.4-bias0.csv',
#           'results/Tonghui/5-17/Al-Au(F1-F2)-3ro-level0.4-bias0-2.csv',
#           'results/Tonghui/5-29/Al-Au(F1-F2)-level0.4-0-bias0.csv',
#           'results/Tonghui/5-29/Al-Au(F1-F2)-4puntas-level0.4-0-bias0.csv',
#           'results/Tonghui/5-29/Al-Au(F1-F2)-4puntas-2do-level0.4-0-bias0.csv'
#           ]
# labels = ['26-4',
#           '17-5',
#           '17-5 post 1st cycle',
#           '17-5 post 1st cycle (2)',
#           '17-5 post 2nd cycle',
#           '17-5 post 2nd cycle (2)',
#           '17-5 post 3rd cycle',
#           '29-5 2t',
#           '29-5 4t',
#           '29-5 4t (2)'
#           ]

# for i, file in enumerate(files):
#     plt.figure(1)
#     f, Z, phase = np.loadtxt(file, delimiter=',', unpack=True, skiprows=1)
#     plt.plot(f, Z, label=f'F1-F2 {labels[i]}')
#     plt.figure(2)
#     plt.plot(f, phase, label=f'F1-F2 {labels[i]}')

#F5-F6 BIAS 0
# files = ['results/Tonghui/4-26/Al-Au-(F5-F6)-400mV.csv',
#          'results/Tonghui/5-17/Al-Au(F5-F6)-level0.4-bias0.csv',
#          'results/Tonghui/5-17/Al-Au(F5-F6)-level0.4-bias0-2.csv'
#          ]
# labels = ['26-4',
#           '17-5',
#           '17-5 post cycle'
#           ]

#BIAS 5V
# files = ['results/Tonghui/5-17/Al-Au(D5-D6)-level0.4-bias5.csv',
#          'results/Tonghui/5-29/Al-Au(D5-D6)-level0.4-2-bias5.csv',
#          'results/Tonghui/5-17/Al-Au(F1-F2)-level0.4-bias5.csv',
#          'results/Tonghui/5-17/Al-Au(F1-F2)-2do-level0.4-bias5.csv',
#          'results/Tonghui/5-17/Al-Au(F1-F2)-3ro-level0.4-bias5.csv',
#          'results/Tonghui/5-17/Al-Au(F5-F6)-level0.4-bias5.csv'
#          ]
# labels = ['D5-D6 (17-5)',
#           'D5-D6 (29-5)',
#           'F1-F2 1st cycle',
#           'F1-F2 2nd cycle',
#           'F1-F2 3rd cycle',
#           'F5-F6']

#BIAS -5V
# files = ['results/Tonghui/5-17/Al-Au(D5-D6)-level0.4-bias-5.csv',
#          'results/Tonghui/5-29/Al-Au(D5-D6)-level0.4-pol-neg-2-bias-5.csv',
#          'results/Tonghui/5-17/Al-Au(F1-F2)-level0.4-bias-5.csv',
#          'results/Tonghui/5-17/Al-Au(F1-F2)-2do-level0.4-bias-5.csv',
#          'results/Tonghui/5-17/Al-Au(F1-F2)-3ro-level0.4-bias-5.csv',
#          'results/Tonghui/5-17/Al-Au(F5-F6)-level0.4-bias-5.csv'
#          ]
# labels = ['D5-D6 (17-5)',
#           'D5-D6 (29-5)',
#           'F1-F2 1st cycle',
#           'F1-F2 2nd cycle',
#           'F1-F2 3rd cycle',
#           'F5-F6']


for i, file in enumerate(files):
    plt.figure(1)
    f, Z, phase = np.loadtxt(file, delimiter=',', unpack=True, skiprows=1)
    plt.plot(f, Z, label=f'{labels[i]}')
    plt.figure(2)
    plt.plot(f, phase, label=f'{labels[i]}')


plt.figure(1)
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Impedancia [$\Omega$]')
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.grid()
plt.savefig('graficos/6-5/complation-D5-D6-bias0-Z.png', dpi=400)
# plt.show()

plt.figure(2)
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Fase [°]')
plt.xscale('log')
plt.legend()
plt.grid()
plt.savefig('graficos/6-5/complation-D5-D6-bias0-f.png', dpi=400)
plt.show()
#%%
#########################
#PROMEDIO 30 CICLOS
#########################

t_din, volt_din, curr_din, t_rem, volt_rem, curr_rem = np.loadtxt('./results/Keithley/8-25/90-Al-Au(B1-B2)-(-2.5,7)-6.csv', delimiter=',', unpack=True, skiprows=3)

plt.plot(t_din[1:149], volt_din[1:149], '-o')
plt.plot(t_rem[1:149], volt_rem[1:149], '-o')
len(t_din[:149])

plt.plot(t_din[149:297], volt_din[149:297], '-o')
plt.plot(t_rem[149:297], volt_rem[149:297], '-o')
len(t_din[149:297])

plt.plot(t_din[297:445], volt_din[297:445], '-o')
plt.plot(t_rem[297:445], volt_rem[297:445], '-o')

plt.grid()
plt.show()

n = 1

ciclos = []
for i in range(30):
    ciclos.append(curr_rem[n:n+147])
    # plt.plot(t_din[n:n+147], volt_din[n:n+147], '-o')
    # plt.plot(t_rem[n:n+147], volt_rem[n:n+147], '-o')
    print(i)
    plt.scatter(volt_din[n:n+147], abs(volt_rem[n:n+147]/curr_rem[n:n+147]), c=t_rem[n:n+147], cmap='cool')
    plt.show()
    n += 148
# plt.grid()
# plt.show()
#17, 18
curr_mean = np.mean(np.array(ciclos[:17] + ciclos[19:]), axis=0)
curr_std = np.std(np.array(ciclos[:17] + ciclos[19:]), axis=0)

print(min(0.4/np.abs(curr_mean)), max(0.4/np.abs(curr_mean)))



plt.scatter(volt_din, abs(0.4/curr_rem), c=t_rem, cmap='cool')
plt.colorbar(label='Tiempo [s]')
plt.errorbar(volt_din[1:148], 0.4/np.abs(curr_mean), yerr=0.4*curr_std/curr_mean**2, fmt='-ok', capsize=3, errorevery=2, label='Promedio de ciclos')
plt.hlines(max(0.4/np.abs(curr_mean)), -2.5, 7, linestyles='dashed', colors='red', path_effects=[pe.Stroke(linewidth=2, foreground='k'), pe.Normal()], label='HRS y LRS')
plt.hlines(min(0.4/np.abs(curr_mean)), -2.5, 7, linestyles='dashed', colors='red', path_effects=[pe.Stroke(linewidth=2, foreground='k'), pe.Normal()])
# plt.errorbar(volt_din[1:148], 0.4/np.abs(curr_mean), fmt='-ok', capsize=3, errorevery=2)
plt.xlabel('Voltaje [V]')
plt.ylabel('Resistencia [$\Omega$]')
plt.yscale('log')
plt.tight_layout()
plt.grid()
plt.ylim(top=500000)
plt.legend()
plt.savefig('graficos/8-25/90-Al-Au(B1-B2)-30ciclos-sinruido.png', dpi=400)
plt.show()


# %%
