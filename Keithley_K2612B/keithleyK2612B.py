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
