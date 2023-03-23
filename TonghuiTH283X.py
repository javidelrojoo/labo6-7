import visa
import numpy as np

class TH283X:
    def __init__(self, name):
        self._lcr = visa.ResourceManager().open_resource(name)
        print(self._lcr.query("*IDN?"))
    
    def __del__(self):
        self._lcr.close()
    
    def set_freq(self, value, units=''): #Setea la frecuencia en el valor pedido, units solo acepta multiplos (k, M). 
        if value == 'MIN':
            self._lcr.write('FREQ MIN')
            return
        if value == 'MAX':
            self._lcr.write('FREQ MAX')
            return
        self._lcr.write(f'FREQ {value}{units.upper()}HZ')
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
