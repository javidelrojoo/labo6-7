import visa
import numpy as np
import matplotlib.pyplot as plt
from save_csv import save_csv
from TonghuiTH283X import TH283X

lcr = TH283X('GPIB0::9::INSTR')

lcr.set_freq(1, 'k')
lcr.get_freq()

lcr.set_freq(0.1)
lcr.get_volt()

lcr.set_curr('MIN')
lcr.get_curr()

lcr.set_ores(50)
lcr.get_ores()