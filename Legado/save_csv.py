import numpy as np
import matplotlib.pyplot as plt
import os

import os

def save_csv(*data, filename, root='.\\', delimiter=',', header='', rewrite=False):
    # Comprobar si el archivo ya existe en la ubicación especificada.
    isfile = os.path.isfile(root + filename + '.csv')
    
    # Si no se permite la sobreescritura y el archivo ya existe, buscar un nombre alternativo.
    num = 0
    while not rewrite and isfile:
        num += 1
        isfile = os.path.isfile(root + filename + f'-{num}' + '.csv')
        
    # Si el archivo ya existe y no se permite la sobreescritura, imprimir un aviso.
    if isfile:
        print('ATENCIÓN: SE SOBREESCRIBIRÁ EL ARCHIVO')
    
    # Seleccionar el nombre de archivo correcto basado en si se encontraron duplicados.
    if num == 0:
        np.savetxt(root + filename + '.csv', np.transpose(np.array([*data])), header=header, delimiter=delimiter)
    else:
        np.savetxt(root + filename + f'-{num}' + '.csv', np.transpose(np.array([*data])), header=header, delimiter=delimiter)
    
    return
