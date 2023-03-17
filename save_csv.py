import numpy as np
import matplotlib.pyplot as plt
import os

def save_csv(*data, filename, root='.\\', delimiter=',', header='', rewrite=False):
    isfile = os.path.isfile(root+filename+'.csv')
    if not rewrite and isfile:
        print('Este archivo ya existe, para sobreescribirlo usar el argumento rewrite')
        return
    if isfile:
        print('ATENCIÓN: SE SOBREESCRIBIÓ EL ARCHIVO')
    np.savetxt(root+filename+'.csv', np.transpose(np.array([*data])), header=header, delimiter=delimiter)
    return