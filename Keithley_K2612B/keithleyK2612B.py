import time
import pyvisa
import numpy as np
from tqdm import tqdm

class K2612B:
    def __init__(self, name):
        self._smu = pyvisa.ResourceManager().open_resource(name)
        self._smu.write('smub.reset()')
        self._smu.write('display.screen = display.SMUB')
        print(self._smu.query("*IDN?"))
    
    def __del__(self):
        self._smu.close()
    
    def hsl(self, Vmax, Vmin, pw, Npos, Nneg, rangei, limiti, rangev, cycles, T1, T2, nplc, hslV=.4):
        self._smu.write(f'smub.measure.nplc = {nplc}')
        self._smu.write('smub.source.func = smub.OUTPUT_DCVOLTS')  # Configurar el modo de generación de voltaje a voltaje DC
        
        # self._smu.write('smub.measure.autorangei = smub.AUTORANGE_OFF')
        # self._smu.write('smub.measure.autorangev = smub.AUTORANGE_OFF')
        # self._smu.write(f'smub.source.limiti = {limiti}')
        # self._smu.write(f'smub.measure.rangei = {rangei}')
        # self._smu.write(f'smub.measure.rangev = {rangev}')
        
        self._smu.write('smub.measure.autorangei = smub.AUTORANGE_ON')
        self._smu.write('smub.measure.autorangev = smub.AUTORANGE_ON')
        
        volt_meas = np.array([])
        for i in range(cycles):
            volt_meas = np.concatenate((volt_meas, np.linspace(0, Vmax, Npos//2, endpoint=False), np.linspace(Vmax, 0, Npos//2, endpoint=False), np.linspace(0, Vmin, Nneg//2, endpoint=False), np.linspace(Vmin, 0, Nneg//2, endpoint=False)))
        
        start_time = time.time()
        
        t_din = []
        volt_din = []
        curr_din = []
        
        t_rem = []
        volt_rem = []
        curr_rem = []
        
        self._smu.write(f'smub.source.levelv = 0')
        
        for i in tqdm(volt_meas):
            
            self._smu.write(f'smub.source.levelv = {i}')
            self._smu.write('smub.source.output = smub.OUTPUT_ON')
            time.sleep(pw/2)
            t_din.append(time.time() - start_time)
            i_din, v_din = self._smu.query('print(smub.measure.iv())').split('\t')
            volt_din.append(float(v_din.strip('\n')))
            curr_din.append(float(i_din.strip('\n')))
            time.sleep(pw/2)
            self._smu.write('smub.source.output = smub.OUTPUT_OFF')
            
            time.sleep(T1)
            
            self._smu.write(f'smub.source.levelv = {hslV}')
            self._smu.write('smub.source.output = smub.OUTPUT_ON')
            time.sleep(pw/2)
            t_rem.append(time.time() - start_time)
            i_rem, v_rem = self._smu.query('print(smub.measure.iv())').split('\t')
            volt_rem.append(float(v_rem.strip('\n')))
            curr_rem.append(float(i_rem.strip('\n')))
            time.sleep(pw/2)
            self._smu.write('smub.source.output = smub.OUTPUT_OFF')
            
            time.sleep(T2)
            
        self._smu.write('smub.source.output = smub.OUTPUT_OFF')
        
        return np.array(t_din), np.array(volt_din), np.array(curr_din), np.array(t_rem), np.array(volt_rem), np.array(curr_rem)
    
    def custom_volt(self, volt_meas, pw, rangei, limiti, rangev, T, nplc):
        self._smu.write(f'smub.measure.nplc = {nplc}')
        self._smu.write('smub.source.func = smub.OUTPUT_DCVOLTS')  # Configurar el modo de generación de voltaje a voltaje DC
        
        # self._smu.write('smub.measure.autorangei = smub.AUTORANGE_OFF')
        # self._smu.write('smub.measure.autorangev = smub.AUTORANGE_OFF')
        # self._smu.write(f'smub.source.limiti = {limiti}')
        # self._smu.write(f'smub.measure.rangei = {rangei}')
        # self._smu.write(f'smub.measure.rangev = {rangev}')
        
        self._smu.write('smub.measure.autorangei = smub.AUTORANGE_ON')
        self._smu.write('smub.measure.autorangev = smub.AUTORANGE_ON')
        
        start_time = time.time()
        
        t = []
        volt = []
        curr = []
        self._smu.write(f'smub.source.levelv = 0')
        
        for i in tqdm(volt_meas):
            
            self._smu.write(f'smub.source.levelv = {i}')
            self._smu.write('smub.source.output = smub.OUTPUT_ON')
            time.sleep(pw/2)
            t.append(time.time() - start_time)
            i, v = self._smu.query('print(smub.measure.iv())').split('\t')
            volt.append(float(v.strip('\n')))
            curr.append(float(i.strip('\n')))
            time.sleep(pw/2)
            self._smu.write('smub.source.output = smub.OUTPUT_OFF')
            
            time.sleep(T)
            
        self._smu.write('smub.source.output = smub.OUTPUT_OFF')
        
        return np.array(t), np.array(volt), np.array(curr)
    
        
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
    
    def autoR(self, V, Rth1, Rth2, rangei, limiti, rangev, cycles, pw, T1, T2, nplc, hslV=.4):
        self._smu.write(f'smub.measure.nplc = {nplc}')
        self._smu.write('smub.source.func = smub.OUTPUT_DCVOLTS')  # Configurar el modo de generación de voltaje a voltaje DC
        
        # self._smu.write('smub.measure.autorangei = smub.AUTORANGE_OFF')
        # self._smu.write('smub.measure.autorangev = smub.AUTORANGE_OFF')
        # self._smu.write(f'smub.source.limiti = {limiti}')
        # self._smu.write(f'smub.measure.rangei = {rangei}')
        # self._smu.write(f'smub.measure.rangev = {rangev}')
        
        self._smu.write('smub.measure.autorangei = smub.AUTORANGE_ON')
        self._smu.write('smub.measure.autorangev = smub.AUTORANGE_ON')
        
        
        start_time = time.time()
        
        t_din = []
        volt_din = []
        curr_din = []
        
        t_rem = []
        volt_rem = []
        curr_rem = []
        
        self._smu.write(f'smub.source.levelv = 0')
        
        self._smu.write(f'smub.source.levelv = {hslV}')
        self._smu.write('smub.source.output = smub.OUTPUT_ON')
        time.sleep(pw/2)
        i_rem, v_rem = self._smu.query('print(smub.measure.iv())').split('\t')
        time.sleep(pw/2)
        i_rem = float(i_rem.strip('\n'))
        self._smu.write('smub.source.output = smub.OUTPUT_OFF')
        print(f'R = {hslV/i_rem*1e-6} MOhm')
        
        while hslV/i_rem > Rth1:
            
            self._smu.write(f'smub.source.levelv = {V}')
            self._smu.write('smub.source.output = smub.OUTPUT_ON')
            time.sleep(pw/2)
            t_din.append(time.time() - start_time)
            i_din, v_din = self._smu.query('print(smub.measure.iv())').split('\t')
            volt_din.append(float(v_din.strip('\n')))
            curr_din.append(float(i_din.strip('\n')))
            time.sleep(pw/2)
            self._smu.write('smub.source.output = smub.OUTPUT_OFF')
            
            time.sleep(T1)
            
            self._smu.write(f'smub.source.levelv = {hslV}')
            self._smu.write('smub.source.output = smub.OUTPUT_ON')
            time.sleep(pw/2)
            t_rem.append(time.time() - start_time)
            i_rem, v_rem = self._smu.query('print(smub.measure.iv())').split('\t')
            volt_rem.append(float(v_rem.strip('\n')))
            curr_rem.append(float(i_rem.strip('\n')))
            i_rem = float(i_rem.strip('\n'))
            time.sleep(pw/2)
            self._smu.write('smub.source.output = smub.OUTPUT_OFF')
            print(f'{len(volt_din)} - R = {hslV/i_rem*1e-6} MOhm')
            
            time.sleep(T2)
            
            if time.time() - start_time > 60*10:    
                break
        print(f'Se llegó a {Rth1*1e-6} MOhm con {len(volt_din)} pulsos')
        
        while True:
            self._smu.write(f'smub.source.levelv = {hslV}')
            self._smu.write('smub.source.output = smub.OUTPUT_ON')
            time.sleep(pw/2)
            t_rem.append(time.time() - start_time)
            i_rem, v_rem = self._smu.query('print(smub.measure.iv())').split('\t')
            volt_rem.append(float(v_rem.strip('\n')))
            curr_rem.append(float(i_rem.strip('\n')))
            i_rem = float(i_rem.strip('\n'))
            time.sleep(pw/2)
            self._smu.write('smub.source.output = smub.OUTPUT_OFF')
            print(f'R = {hslV/i_rem*1e-6} MOhm')
            time.sleep(T2*10)
            if time.time() - start_time > 60*15:    
                break
        
        self._smu.write('smub.source.output = smub.OUTPUT_OFF')
        
        return np.array(t_din), np.array(volt_din), np.array(curr_din), np.array(t_rem), np.array(volt_rem), np.array(curr_rem)
    