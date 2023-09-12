import pyvisa as visa
import numpy as np


class SDS1202:
    """Clase para el manejo osciloscopio TDS2000 usando PyVISA de interfaz
    """
    
    def __init__(self, name):
        self._osci = visa.ResourceManager().open_resource(name)
        print(self._osci.query("*IDN?"))
        
        self._osci.write(':STOP')  # Detiene la adquisición (opcional)
        self._osci.write(':WAVEFORM:FORMAT BYTE')  # Formato de datos como BYTE (opcional)
        self._osci.write(':WAVEFORM:POINTS:MODE RAW')  # Modo de puntos RAW (opcional)


    	#Configuración de curva
        
        # Modo de transmision: Binario positivo.
        # self._osci.write('DAT:ENC RPB') 
        # 1 byte de dato. Con RPB 127 es la mitad de la pantalla
        # self._osci.write('DAT:WID 1')
        # La curva mandada inicia en el primer dato
        # self._osci.write("DAT:STAR 1") 
        # La curva mandada finaliza en el último dato
        # self._osci.write("DAT:STOP 2500") 

        #Adquisición por sampleo
        # self._osci.write("ACQ:MOD SAMP")
				
        #Bloquea el control del osciloscopio
        self._osci.write("LOCK ON")
    	
    def __del__(self):
        self._osci.close()			

    def config(self):
        #Seteo de canal
        self.set_channel(channel=1, scale=20e-3)
        self.set_channel(channel=2, scale=20e-3)
        self.set_time(scale=1e-3, zero=0)

    def unlock(self):
         #Desbloquea el control del osciloscopio
        self._osci.write("LOCK OFF")

    def set_channel(self, channel, scale, zero=0):
    	#if coup != "DC" or coup != "AC" or coup != "GND":
    	    #coup = "DC"
    	#self._osci.write("CH{0}:COUP ".format(canal) + coup) #Acoplamiento DC
    	#self._osci.write("CH{0}:PROB 
        self._osci.write("CH{0}:SCA {1}".format(channel, scale))
        self._osci.write("CH{0}:POS {1}".format(channel, zero))
	
    def get_channel(self, channel):
        return self._osci.read("CH{0}?".format(channel))
		
    def set_time(self, scale, zero=0):
        self._osci.write("HOR:SCA {0}".format(scale))
        self._osci.write("HOR:POS {0}".format(zero))	
	
    def get_time(self):
        return self._osci.query("HOR?")
	
    def read_data(self):
        # Obtiene los datos de los canales 1 y 2
        self._osci.write(':WAVEFORM:SOURCE CHAN1')
        data_chan1 = self._osci.query_binary_values(':WAVEFORM:DATA?', 'b', is_big_endian=True)
        time_scale_chan1 = float(self._osci.query(':TIMebase:MAIN:SCALE?'))
        time_offset_chan1 = float(self._osci.query(':TIMebase:MAIN:OFFSET?'))
        time_chan1 = np.arange(0, len(data_chan1)) * time_scale_chan1 + time_offset_chan1


        self._osci.write(':WAVEFORM:SOURCE CHAN2')
        data_chan2 = self._osci.query_binary_values(':WAVEFORM:DATA?', 'b', is_big_endian=True)
        time_scale_chan2 = float(self._osci.query(':TIMebase:MAIN:SCALE?'))
        time_offset_chan2 = float(self._osci.query(':TIMebase:MAIN:OFFSET?'))
        time_chan2 = np.arange(0, len(data_chan2)) * time_scale_chan2 + time_offset_chan2

        # Convierte los datos a float
        scale_factor_chan1 = float(self._osci.query(':CHAN1:SCALE?'))
        offset_chan1 = float(self._osci.query(':CHAN1:OFFSET?'))
        data_float_chan1 = np.array([(x - offset_chan1) * scale_factor_chan1 for x in data_chan1])

        scale_factor_chan2 = float(self._osci.query(':CHAN2:SCALE?'))
        offset_chan2 = float(self._osci.query(':CHAN2:OFFSET?'))
        data_float_chan2 = np.array([(x - offset_chan2) * scale_factor_chan2 for x in data_chan2])

        return time_chan1, data_float_chan1, time_chan2, data_float_chan2
    
    def get_range(self, channel):
        xze, xin, yze, ymu, yoff = self._osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', 
                                                                 separator=';')         
        rango = (np.array((0, 255))-yoff)*ymu +yze
        return rango   
