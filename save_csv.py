import numpy as np
import matplotlib.pyplot as plt
import os

def save_csv(*data, filename, root='.\\', delimiter=',', header='', rewrite=False):
    
    isfile = os.path.isfile(root+filename+'.csv')
    num = 0
    while not rewrite and isfile:
        num += 1
        isfile = os.path.isfile(root+filename+f'-{num}'+'.csv')
        
    if isfile:
        print('ATENCIÓN: SE SOBREESCRIBIRÁ EL ARCHIVO')
    
    if num == 0:
        np.savetxt(root+filename+'.csv', np.transpose(np.array([*data])), header=header, delimiter=delimiter)
    else:
        np.savetxt(root+filename+f'-{num}'+'.csv', np.transpose(np.array([*data])), header=header, delimiter=delimiter)
    return