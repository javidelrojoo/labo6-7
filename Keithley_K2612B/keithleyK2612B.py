import time
import pyvisa
import numpy as np

class K2612B:
    def __init__(self, name):
        self._smu = pyvisa.ResourceManager().open_resource(name)
        self._smu.write('smub.reset()')
        self._smu.write('display.screen = display.SMUB')
        print(self._smu.query("*IDN?"))
    
    def __del__(self):
        self._smu.close()
    
    def hsl(self, Vmax, Vmin, hslV=.4, pw, Npos, Nneg):
        self._smu.write('smub.source.func = smub.OUTPUT_DCVOLTS')  # Configurar el modo de generación de voltaje a voltaje DC
        self._smu.write('smub.measure.autorangei = smub.AUTORANGE_ON')
        self._smu.write('smub.measure.autorangev = smub.AUTORANGE_ON')
        
        volt_meas = np.concatenate((np.linspace(0, Vmax, Npos//2, endpoint=False), np.linspace(Vmax, 0, Npos//2, endpoint=False), np.linspace(0, Vmin, Nneg//2, endpoint=False), np.linspace(Vmin, 0, Nneg//2, endpoint=False)))
        
        start_time = time.time()
        
        t_din = []
        volt_din = []
        curr_din = []
        
        t_rem = []
        volt_rem = []
        curr_rem = []
        
        self._smu.write('smub.source.levelv = 0')
        self._smu.write('smub.source.output = smub.OUTPUT_ON')
        
        for i in volt_meas:
            
            self._smu.write(f'smub.source.levelv = {i}')
            t_din.append(time.time() - start_time)
            v_din, i_din = self._smu.query('print(smub.measure.iv())').split('\t')
            volt_din.append(float(v.strip('\n')))
            curr_din.append(float(i.strip('\n')))
            
            time.sleep(pw)
            
            self._smu.write(f'smub.source.levelv = {hslV}')
            t_rem.append(time.time() - start_time)
            v_rem, i_rem = self._smu.query('print(smub.measure.iv())').split('\t')
            volt_rem.append(float(v.strip('\n')))
            curr_rem.append(float(i.strip('\n')))
            
            time.sleep(pw)
        
        self._smu.write('smub.source.output = smub.OUTPUT_OFF')
        
        return np.array(t_din), np.array(volt_din), np.array(curr_din), np.array(t_rem), np.array(volt_rem), np.array(curr_rem)
        
    def stress_DC(self, V, time_interval, total_time):
        # Configuración del SMU
        #self._smu.write('display.measure.func = display.MEASURE_DCAMPS')  # Configurar el modo de medición a corriente
        self._smu.write('smub.source.func = smub.OUTPUT_DCVOLTS')  # Configurar el modo de generación de voltaje a voltaje DC
        self._smu.write(f'smub.source.levelv = {V}')  # Establecer el voltaje de salida deseado
        self._smu.write('smub.source.output = smub.OUTPUT_ON')
        self._smu.write('smub.measure.autorangei = smub.AUTORANGE_ON')
        self._smu.write('smub.measure.autorangev = smub.AUTORANGE_ON')
        
        start_time = time.time()
        t = []
        volt = []
        curr = []
        while True:
            # Realizar una medición
            t.append(time.time() - start_time)
            v, i = self._smu.query('print(smub.measure.iv())').split('\t')
            volt.append(float(v.strip('\n')))
            curr.append(float(i.strip('\n')))

            # Verificar si se ha alcanzado la duración total de la medición
            if t[-1] >= total_time:
                break

            # Esperar el intervalo de tiempo antes de la siguiente medición
            time.sleep(time_interval)
        self._smu.write('smub.source.output = smub.OUTPUT_OFF')
        return np.array(t), np.array(volt), np.array(curr)
