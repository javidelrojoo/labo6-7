import pyvisa as visa
import numpy as np

import visa
import numpy as np

class TDS1002B:
    """Clase para el manejo del osciloscopio TDS2000 usando PyVISA de interfaz
    """
    
    def __init__(self, name):
        # Inicialización: Abre la conexión con el osciloscopio y muestra su identificación.
        self._osci = visa.ResourceManager().open_resource(name)
        print(self._osci.query("*IDN?"))

        # Configuración de la curva y adquisición por sampleo.
        self._osci.write('DAT:ENC RPB') 
        self._osci.write('DAT:WID 1')
        self._osci.write("DAT:STAR 1")
        self._osci.write("DAT:STOP 2500") 
        self._osci.write("ACQ:MOD SAMP")
        self._osci.write("LOC")  # Bloquea el control del osciloscopio.
    	
    def __del__(self):
        # Destructor: Cierra la conexión con el osciloscopio.
        self._osci.close()			

    def config(self):
        # Configuración predeterminada de canales y tiempo.
        self.set_channel(channel=1, scale=20e-3)
        self.set_channel(channel=2, scale=20e-3)
        self.set_time(scale=1e-3, zero=0)

    def unlock(self):
        # Desbloquea el control del osciloscopio.
        self._osci.write("UNLOC")

    def set_channel(self, channel, scale, zero=0):
        # Configura el canal especificado con la escala y posición vertical.
        self._osci.write("CH{0}:SCA {1}".format(channel, scale))
        self._osci.write("CH{0}:POS {1}".format(channel, zero))
	
    def get_channel(self, channel):
        # Obtiene la configuración actual del canal especificado.
        return self._osci.query("CH{0}?".format(channel))
		
    def set_time(self, scale, zero=0):
        # Configura la escala y posición horizontal (tiempo).
        self._osci.write("HOR:SCA {0}".format(scale))
        self._osci.write("HOR:POS {0}".format(zero))	
	
    def get_time(self):
        # Obtiene la configuración actual del tiempo.
        return self._osci.query("HOR?")
	
    def read_data(self, channel):
        # Hace aparecer el canal en pantalla (por si no está habilitado).
        self._osci.write("SEL:CH{0} ON".format(channel)) 
        # Selecciona el canal.
        self._osci.write("DAT:SOU CH{0}".format(channel))
        self._osci.write("DAT:STAR 1")
        self._osci.write("DAT:STOP 10000")
        
        # Obtiene los parámetros necesarios para convertir los datos binarios a valores físicos.
        xze, xin, yze, ymu, yoff = self._osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';') 
        # Lee y convierte los datos binarios a valores físicos.
        data = (self._osci.query_binary_values('CURV?', datatype='B', container=np.array) - yoff) * ymu + yze        
        tiempo = xze + np.arange(len(data)) * xin
        return tiempo, data
    
    def get_range(self, channel):
        # Obtiene el rango vertical del canal.
        xze, xin, yze, ymu, yoff = self._osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')         
        rango = (np.array((0, 255)) - yoff) * ymu + yze
        return rango
