import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

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
Z_err, phase_err = Z*1/100, phase/100

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
plt.savefig('graficos/bode-resistencia-pura.png', dpi=400)
plt.show()