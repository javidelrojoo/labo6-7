import numpy as np
import os

day = '6-28'
path = f'./results/Tonghui/{day}/'
os.mkdir(f'EIS Analyser/{day}')
# filename = '2.79k-sincorreccion-probe'

for filename in os.listdir(path):
    filename = filename.split('.csv')[0]
    frec, Z, phase = np.loadtxt(f'{path}{filename}.csv', delimiter=',', skiprows=1, unpack=True)

    Zre = Z*np.cos(np.pi/180 * phase)
    Zim = Z*np.sin(np.pi/180 * phase)

    with open(f'EIS Analyser/{day}/{filename}.txt', 'w') as f:
        f.write(f'{len(frec)}\n')
        for i in range(len(frec)):
            f.write(f'{Zre[i]}\t{-Zim[i]}\t{frec[i]}\n')