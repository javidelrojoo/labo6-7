import time
import pyvisa
import numpy as np
from tqdm import tqdm
import sys

class K2612B:
    def __init__(self, name):
        # Inicialización: Abre la conexión con el instrumento, realiza configuraciones iniciales y muestra la identificación del dispositivo.
        self._smu = pyvisa.ResourceManager().open_resource(name)
        self._smu.write('smub.reset()')
        self._smu.write('display.screen = display.SMUB')
        print(self._smu.query("*IDN?"))
    
    def __del__(self):
        # Destructor: Cierra la conexión con el instrumento cuando la instancia de la clase se elimina.
        self._smu.close()
    
    def hsl(self, Vmax, Vmin, pw, Npos, Nneg, rangei, limiti, rangev, cycles, T1, T2, nplc, hslV=.4):
        # Método para realizar barridos de voltajes (hsl) con configuraciones específicas y devolver datos de medición.
        self._smu.write(f'smub.measure.nplc = {nplc}')
        self._smu.write('smub.source.func = smub.OUTPUT_DCVOLTS')  # Configura el modo de generación de voltaje a voltaje DC
        
        # Configuraciones desactivadas:
        # self._smu.write('smub.measure.autorangei = smub.AUTORANGE_OFF')
        # self._smu.write('smub.measure.autorangev = smub.AUTORANGE_OFF')
        # self._smu.write(f'smub.source.limiti = {limiti}')
        # self._smu.write(f'smub.measure.rangei = {rangei}')
        # self._smu.write(f'smub.measure.rangev = {rangev}')
        
        # Configuraciones activadas:
        self._smu.write('smub.measure.autorangei = smub.AUTORANGE_ON')
        self._smu.write('smub.measure.autorangev = smub.AUTORANGE_ON')
        
        # Genera el patrón de voltajes a aplicar durante los ciclos.
        volt_meas = np.array([])
        for i in range(cycles):
            volt_meas = np.concatenate((volt_meas, np.linspace(0, Vmax, Npos//2, endpoint=False), np.linspace(Vmax, 0, Npos//2, endpoint=False), np.linspace(0, Vmin, Nneg//2, endpoint=False), np.linspace(Vmin, 0, Nneg//2, endpoint=False)))
        
        start_time = time.time()
        
        t_din = []  # Lista para almacenar tiempos de la esctritura.
        volt_din = []  # Lista para almacenar voltajes de la esctritura.
        curr_din = []  # Lista para almacenar corrientes de la esctritura.
        
        t_rem = []  # Lista para almacenar tiempos de la lectura.
        volt_rem = []  # Lista para almacenar voltajes de la lectura.
        curr_rem = []  # Lista para almacenar corrientes de la lectura.
        
        self._smu.write(f'smub.source.levelv = 0')  # Establece el nivel de voltaje inicial.
        
        for i in tqdm(volt_meas):
            # Escritura
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
            
            # Lectura
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
        
        # Devuelve los datos medidos.
        return np.array(t_din), np.array(volt_din), np.array(curr_din), np.array(t_rem), np.array(volt_rem), np.array(curr_rem)

    
    def custom_volt(self, volt_meas, pw, rangei, limiti, rangev, T, nplc):
        # Método para aplicar voltajes personalizados y medir corriente y voltaje.
        self._smu.write(f'smub.measure.nplc = {nplc}')
        self._smu.write('smub.source.func = smub.OUTPUT_DCVOLTS')  # Configura el modo de generación de voltaje a voltaje DC
        
        # Configuraciones desactivadas:
        # self._smu.write('smub.measure.autorangei = smub.AUTORANGE_OFF')
        # self._smu.write('smub.measure.autorangev = smub.AUTORANGE_OFF')
        # self._smu.write(f'smub.source.limiti = {limiti}')
        # self._smu.write(f'smub.measure.rangei = {rangei}')
        # self._smu.write(f'smub.measure.rangev = {rangev}')
        
        # Configuraciones activadas:
        self._smu.write('smub.measure.autorangei = smub.AUTORANGE_ON')
        self._smu.write('smub.measure.autorangev = smub.AUTORANGE_ON')
        
        start_time = time.time()
        
        t = []  # Lista para almacenar tiempos de medición.
        volt = []  # Lista para almacenar voltajes medidos.
        curr = []  # Lista para almacenar corrientes medias.
        
        self._smu.write(f'smub.source.levelv = 0')  # Establece el nivel de voltaje inicial.
        
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
        
        self._smu.write('smub.source.output = smub.OUTPUT_OFF')  # Apaga la salida de voltaje.
        
        # Devuelve los datos medidos.
        return np.array(t), np.array(volt), np.array(curr)

    
        
    def stress_DC(self, V, time_interval, total_time):
        # Método para realizar una prueba de estrés aplicando voltaje DC y midiendo corriente y voltaje.
        
        # Configuración del SMU
        # self._smu.write('display.measure.func = display.MEASURE_DCAMPS')  # Configura el modo de medición a corriente
        self._smu.write('smub.source.func = smub.OUTPUT_DCVOLTS')  # Configura el modo de generación de voltaje a voltaje DC
        self._smu.write(f'smub.source.levelv = {V}')  # Establece el voltaje de salida deseado
        self._smu.write('smub.source.output = smub.OUTPUT_ON')
        self._smu.write('smub.measure.autorangei = smub.AUTORANGE_ON')
        self._smu.write('smub.measure.autorangev = smub.AUTORANGE_ON')
        
        start_time = time.time()
        t = []  # Lista para almacenar tiempos de medición.
        volt = []  # Lista para almacenar voltajes medidos.
        curr = []  # Lista para almacenar corrientes medias.

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

        self._smu.write('smub.source.output = smub.OUTPUT_OFF')  # Apaga la salida de voltaje.
        
        # Devuelve los datos medidos.
        return np.array(t), np.array(volt), np.array(curr)

    
    def autoR(self, V, Tmax, rangei, limiti, rangev, Twrite, Tread, T1, T2, nplc, Nth=50, hslV=.4, ratioRth=1/10):
        # Método para realizar una prueba de estrés aplicando voltaje DC y ajustando automáticamente el límite de resistencia.

        # Configuración del SMU
        self._smu.write(f'smub.measure.nplc = {nplc}')
        self._smu.write('smub.source.func = smub.OUTPUT_DCVOLTS')  # Configura el modo de generación de voltaje a voltaje DC
        
        # Configuración del límite de resistencia inicial
        self._smu.write('smub.measure.autorangei = smub.AUTORANGE_ON')
        self._smu.write('smub.measure.autorangev = smub.AUTORANGE_ON')
        
        # Obtener resistencia inicial para establecer el umbral
        t0, volt0, curr0 = self.custom_volt([hslV]*50, Tread, rangei, limiti, rangev, T1, nplc)
        Rth = np.mean(abs(volt0/curr0)) * ratioRth
        print(f'El umbral se estableció en {Rth*1e-6} MOhms')
        
        # Inicializar variables
        start_time = time.time()
        t_din = []
        volt_din = []
        curr_din = []
        
        t_rem = []
        volt_rem = []
        curr_rem = []
        
        # Configurar voltaje de salida para medición de resistencia inicial
        self._smu.write(f'smub.source.levelv = {hslV}')
        self._smu.write('smub.source.output = smub.OUTPUT_ON')
        time.sleep(Tread/2)
        i_rem, v_rem = self._smu.query('print(smub.measure.iv())').split('\t')
        time.sleep(Tread/2)
        i_rem = float(i_rem.strip('\n'))
        v_rem = float(v_rem.strip('\n'))
        self._smu.write('smub.source.output = smub.OUTPUT_OFF')
        sys.stdout.write(f'\rR = {abs(v_rem/i_rem)*1e-6} MOhm')
        
        numRth = 0
        
        # Bucle para ajustar el límite de resistencia
        while numRth < Nth:
            # Aplicar voltaje de escritura
            self._smu.write(f'smub.source.levelv = {V}')
            self._smu.write('smub.source.output = smub.OUTPUT_ON')
            time.sleep(Twrite/2)
            t_din.append(time.time() - start_time)
            volt_din.append(0)  # No se mide voltaje durante la escritura
            curr_din.append(0)  # No se mide corriente durante la escritura
            time.sleep(Twrite/2)
            self._smu.write('smub.source.output = smub.OUTPUT_OFF')
            
            time.sleep(T1)
            
            # Configurar voltaje de salida para medición de resistencia
            self._smu.write(f'smub.source.levelv = {hslV}')
            self._smu.write('smub.source.output = smub.OUTPUT_ON')
            time.sleep(Tread/2)
            t_rem.append(time.time() - start_time)
            i_rem, v_rem = self._smu.query('print(smub.measure.iv())').split('\t')
            volt_rem.append(float(v_rem.strip('\n')))
            curr_rem.append(float(i_rem.strip('\n')))
            i_rem = float(i_rem.strip('\n'))
            v_rem = float(v_rem.strip('\n'))
            time.sleep(Tread/2)
            self._smu.write('smub.source.output = smub.OUTPUT_OFF')
            sys.stdout.write(f'\rR{len(volt_din)} - R = {abs(v_rem/i_rem)*1e-6} MOhm')
            time.sleep(T2)
            
            # Verificar si la resistencia medida es menor al umbral
            if abs(v_rem/i_rem) < Rth:
                numRth += 1
            # Verificar si se ha alcanzado el límite de pulsos
            if len(volt_din) > 1500:
                break
        
        print(f'\nSe llegó a {Rth*1e-6} MOhm con {len(volt_din)} pulsos')
        
        # Continuar tomando mediciones hasta alcanzar el tiempo máximo
        t0 = time.time()
        while True:
            self._smu.write(f'smub.source.levelv = {hslV}')
            self._smu.write('smub.source.output = smub.OUTPUT_ON')
            time.sleep(Tread/2)
            t_rem.append(time.time() - start_time)
            i_rem, v_rem = self._smu.query('print(smub.measure.iv())').split('\t')
            volt_rem.append(float(v_rem.strip('\n')))
            curr_rem.append(float(i_rem.strip('\n')))
            i_rem = float(i_rem.strip('\n'))
            v_rem = float(v_rem.strip('\n'))
            time.sleep(Tread/2)
            self._smu.write('smub.source.output = smub.OUTPUT_OFF')
            sys.stdout.write(f'\rR = {abs(v_rem/i_rem)*1e-6} MOhm')
            time.sleep(T2*10)
            
            # Verificar si se ha alcanzado el tiempo máximo
            if time.time() - t0 > Tmax:    
                break
        
        self._smu.write('smub.source.output = smub.OUTPUT_OFF')
        print(f'\nSe llegó a {Rth*1e-6} MOhm con {len(volt_din)} pulsos')
        
        # Devolver resultados
        return np.array(t_din), np.array(volt_din), np.array(curr_din), np.array(t_rem), np.array(volt_rem), np.array(curr_rem), len(volt_din), Rth

   
    def autohsl(self, Vmax, Vmin, pw, Npos, Nneg, rangei, limiti, rangev, T1, T2, nplc, Rth, hslV=.4):
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
        volt_meas = np.concatenate((volt_meas, np.linspace(0, Vmax, Npos//2, endpoint=False), np.linspace(Vmax, 0, Npos//2, endpoint=False), np.linspace(0, Vmin, Nneg//2, endpoint=False), np.linspace(Vmin, 0, Nneg//2, endpoint=False)))
        
        start_time = time.time()
        
        t_din = []
        volt_din = []
        curr_din = []
        
        t_rem = []
        volt_rem = []
        curr_rem = []
        
        self._smu.write(f'smub.source.levelv = 0')
        
        R_rem = 0
        while R_rem < Rth:
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
            R_rem = volt_rem[-1]/curr_rem[-1]
            
        return np.array(t_din), np.array(volt_din), np.array(curr_din), np.array(t_rem), np.array(volt_rem), np.array(curr_rem)
    
    def autoR_I(self, I, Tmax, rangei, limiti, rangev, Twrite, Tread, T1, T2, nplc, Nth=50, hslV=.4, ratioRth=1/10):
        self._smu.write(f'smub.measure.nplc = {nplc}')
        self._smu.write('smub.source.func = smub.OUTPUT_DCVOLTS')  # Configurar el modo de generación de voltaje a voltaje DC
        
        # self._smu.write('smub.measure.autorangei = smub.AUTORANGE_OFF')
        # self._smu.write('smub.measure.autorangev = smub.AUTORANGE_OFF')
        # self._smu.write(f'smub.source.limiti = {limiti}')
        # self._smu.write(f'smub.measure.rangei = {rangei}')
        # self._smu.write(f'smub.measure.rangev = {rangev}')
        
        self._smu.write('smub.measure.autorangei = smub.AUTORANGE_ON')
        self._smu.write('smub.measure.autorangev = smub.AUTORANGE_ON')
        
        t0, volt0, curr0 = self.custom_volt([hslV]*50, Tread, rangei, limiti, rangev, T1, nplc)
        # print(volt0/curr0)
        Rth = np.mean(abs(volt0/curr0))*ratioRth
        # Rth = 1e8
        print(f'El umbral se puso en {Rth*1e-6}MOhms')
        
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
        time.sleep(Tread/2)
        i_rem, v_rem = self._smu.query('print(smub.measure.iv())').split('\t')
        time.sleep(Tread/2)
        i_rem = float(i_rem.strip('\n'))
        v_rem = float(v_rem.strip('\n'))
        self._smu.write('smub.source.output = smub.OUTPUT_OFF')
        sys.stdout.write(f'\rR = {abs(v_rem/i_rem)*1e-6} MOhm')
        
        numRth = 0
        while numRth < Nth:
            
            self._smu.write('smub.source.func = smub.OUTPUT_DCAMPS')
            self._smu.write(f'smub.source.leveli = {I}')
            self._smu.write('smub.source.output = smub.OUTPUT_ON')
            time.sleep(Twrite/2)
            t_din.append(time.time() - start_time)
            # i_din, v_din = self._smu.query('print(smub.measure.iv())').split('\t')
            # volt_din.append(float(v_din.strip('\n')))
            # curr_din.append(float(i_din.strip('\n')))
            volt_din.append(0)
            curr_din.append(0)
            time.sleep(Twrite/2)
            self._smu.write('smub.source.output = smub.OUTPUT_OFF')
            
            time.sleep(T1)
            
            self._smu.write('smub.source.func = smub.OUTPUT_DCVOLTS')
            self._smu.write(f'smub.source.levelv = {hslV}')
            self._smu.write('smub.source.output = smub.OUTPUT_ON')
            time.sleep(Tread/2)
            t_rem.append(time.time() - start_time)
            i_rem, v_rem = self._smu.query('print(smub.measure.iv())').split('\t')
            volt_rem.append(float(v_rem.strip('\n')))
            curr_rem.append(float(i_rem.strip('\n')))
            i_rem = float(i_rem.strip('\n'))
            v_rem = float(v_rem.strip('\n'))
            time.sleep(Tread/2)
            self._smu.write('smub.source.output = smub.OUTPUT_OFF')
            sys.stdout.write(f'\r{len(volt_din)} - R = {abs(v_rem/i_rem)*1e-6} MOhm')
            time.sleep(T2)
            if abs(v_rem/i_rem) < Rth:
                numRth += 1
            if len(volt_din) > 1500:
                break
        
        print(f'\nSe llegó a {Rth*1e-6} MOhm con {len(volt_din)} pulsos')
        t0 = time.time()
        self._smu.write('smub.source.func = smub.OUTPUT_DCVOLTS')
        while True:
            self._smu.write(f'smub.source.levelv = {hslV}')
            self._smu.write('smub.source.output = smub.OUTPUT_ON')
            time.sleep(Tread/2)
            t_rem.append(time.time() - start_time)
            i_rem, v_rem = self._smu.query('print(smub.measure.iv())').split('\t')
            volt_rem.append(float(v_rem.strip('\n')))
            curr_rem.append(float(i_rem.strip('\n')))
            i_rem = float(i_rem.strip('\n'))
            v_rem = float(v_rem.strip('\n'))
            time.sleep(Tread/2)
            self._smu.write('smub.source.output = smub.OUTPUT_OFF')
            sys.stdout.write(f'\rR = {abs(v_rem/i_rem)*1e-6} MOhm')
            time.sleep(T2*10)
            if time.time() - t0 > Tmax:    
                break
        
        self._smu.write('smub.source.output = smub.OUTPUT_OFF')
        print(f'\nSe llegó a {Rth*1e-6} MOhm con {len(volt_din)} pulsos')
        return np.array(t_din), np.array(volt_din), np.array(curr_din), np.array(t_rem), np.array(volt_rem), np.array(curr_rem), len(volt_din), Rth
   