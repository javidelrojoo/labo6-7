import pyvisa
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

class TH283X:
    def __init__(self, name):
        self._lcr = pyvisa.ResourceManager().open_resource(name)
        print(self._lcr.query("*IDN?"))
        self._lcr.timeout = None
    def __del__(self):
        self._lcr.close()
    
    def set_freq(self, value, units=''): #Setea la frecuencia en el valor pedido, units solo acepta multiplos (k, M). 
        if value == 'MIN':
            self._lcr.write('FREQ MIN')
            return
        if value == 'MAX':
            self._lcr.write('FREQ MAX')
            return
        self._lcr.write(f'FREQ {round(value, 3)}{units.upper()}HZ')
        return
    
    def get_freq(self):
        return self._lcr.query('FREQ?')
    
    def set_volt(self, value): #Setea la voltaje en el valor pedido. 
        if value == 'MIN':
            self._lcr.write('VOLT MIN')
            return
        if value == 'MAX':
            self._lcr.write('VOLT MAX')
            return
        self._lcr.write(f'VOLT {value}V')
        return
    
    def get_volt(self):
        return self._lcr.query('VOLT?')
    
    def set_curr(self, value): #Setea la corriente en el valor pedido, en mA. 
        if value == 'MIN':
            self._lcr.write('CURR MIN')
            return
        if value == 'MAX':
            self._lcr.write('CURR MAX')
            return
        self._lcr.write(f'CURR {value}MA')
        return
    
    def get_curr(self):
        return self._lcr.query('CURR?')
    
    def set_ores(self, value): #Setea la resistencia interna de salida, en Ohms. 
        if value == 'MIN':
            self._lcr.write('ORES MIN')
            return
        if value == 'MAX':
            self._lcr.write('ORES MAX')
            return
        self._lcr.write(f'ORES {value}')
    
    def get_ores(self):
        return self._lcr.query('ORES?')

    def set_func_imp(self, function):
        self._lcr.write(f'FUNC:IMP {function}')
        return
    
    def measure(self, function):
        self.set_func_imp(function)
        
        self._lcr.write('TRIG')
        self._lcr.write('*OPC')
        
        result = self._lcr.query('FETC?')
        meas_A, meas_B, *_ = result.split(',')
        return float(meas_A), float(meas_B)
    
    def make_EI(self, frecs, func):
        n = len(frecs)
        Z = np.zeros(n)
        phase = np.zeros(n)
        f = np.zeros(n)
        fig, axs = plt.subplots(2, 1, sharex=True)
        for i, frec in enumerate(tqdm(frecs)):
            self.set_freq(frec)
            Z[i], phase[i] = self.measure(func)
            f[i] = self.get_freq()
            axs[0].clear()
            axs[1].clear()
            self.make_bode_plot(f[:i], Z[:i], phase[:i], new_fig=False)
            plt.pause(.001)
        return f, Z, phase
    
    def make_bode_plot(self, f, Z, phase, new_fig=True):
        if new_fig:
            fig, axs = plt.subplots(2, 1, sharex=True)

        axs[0].plot(f, np.log10(Z), 'C0')
        axs[0].set_ylabel('Ganancia [dB]')
        axs[0].set_xscale('log')
        axs[0].grid()

        axs[1].plot(f, np.abs(phase), 'C1')
        axs[1].set_ylabel('Fase [°]')
        axs[1].set_xlabel('Frecuencia [Hz]')
        axs[1].grid()

        plt.tight_layout()
        plt.show()
        return
    
    def set_DC_bias_volt(self, value):
        self._lcr.write('BIAS:STAT ON')
        if value == 'MIN':
            self._lcr.write('BIAS:VOLT MIN')
            return
        if value == 'MAX':
            self._lcr.write('BIAS:VOLT MAX')
            return
        self._lcr.write(f'BIAS:VOLT {value}')
        return
    
    def set_DC_bias_off(self):
        self._lcr.write('BIAS:STAT OFF')
    
    def make_corr_open(self, min_frec, max_frec, log=True):
        if log:
            frecs = np.logspace(np.log10(min_frec), np.log10(max_frec), 201)
        else:
            frecs = np.linspace(min_frec, max_frec, 201)
        for i in range(1, 202):
            self._lcr.write(f'CORR:SPOT{i}:FREQ {round(frecs, 3)}')
            self._lcr.write(f'CORR:SPOT{i}:OPEN')
    
    def make_corr_short(self, min_frec, max_frec, log=True):
        if log:
            frecs = np.logspace(np.log10(min_frec), np.log10(max_frec), 201)
        else:
            frecs = np.linspace(min_frec, max_frec, 201)
        for i in range(1, 202):
            self._lcr.write(f'CORR:SPOT{i}:FREQ {round(frecs, 3)}')
            self._lcr.write(f'CORR:SPOT{i}:SHOR')