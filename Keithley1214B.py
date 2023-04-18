# -*- coding: utf-8 -*-
import pyvisa
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

class SMU1214B:
    
    def __init__(self, name):
        self._smu = pyvisa.ResourceManager().open_resource(name)
        print(self._smu.query("*IDN?"))
        self._smu.write('reset()')
        # loadTSP("misc",smu)
        self._smu.write('beeper.enable = 0')
        self._smu.write('welcome()')
        self.initBuffers()
    
    def initBuffers(self):
        self._smu.write('init_buffers(smua)')
        self._smu.write('init_buffers(smub)')
        self._smu.write('format.data = format.ASCII')


smu = SMU1214B('USB0::0x05E6::0x2614::4103593::INSTR')
smu._smu.write('PulsedSweepVSingle(1, 2, 10, 0.1, 0.1, 0.1, 2)')
