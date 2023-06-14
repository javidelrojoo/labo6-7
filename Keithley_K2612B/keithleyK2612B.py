import time
import pyvisa
import numpy as np

class K2612B:
    def __init__(self, name):
        self._smu = pyvisa.ResourceManager().open_resource(name)
        print(self._smu.query("*IDN?"))
    
    def __del__(self):
        self._smu.close()
    
    def DC_volt(self, V, time_interval, total_time):
        # Configuración del SMU
        self._smu.write('smub.measure.func = smu.FUNC_DC_CURRENT')  # Configurar el modo de medición a voltaje DC
        self._smu.write('smub.source.channel = smu.CHANNEL_B')  # Seleccionar la fuente B
        self._smu.write('smub.source.func = smu.FUNC_DC_VOLTAGE')  # Configurar el modo de generación de voltaje a voltaje DC
        self._smu.write(f'smub.source.levelv = {V}')  # Establecer el voltaje de salida deseado

        start_time = time.time()
        t = []
        volt = []
        curr = []
        while True:
            # Realizar una medición
            t.append(time.time() - start_time)
            volt.append(float(self._smu.query('smub.measure.v()')))
            curr.append(float(self._smu.query('smub.measure.i()')))

            # Verificar si se ha alcanzado la duración total de la medición
            if t[-1] >= total_time:
                break

            # Esperar el intervalo de tiempo antes de la siguiente medición
            time.sleep(time_interval)
        self._smu.write('smub.source.output = smu.OUTPUT_OFF')
        return np.array(t), np.array(volt), np.array(curr)
