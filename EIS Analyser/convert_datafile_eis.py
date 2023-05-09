import numpy as np
import os

path = 'Tonghui TH283X/results/probe-station/26-4/'
os.mkdir('EIS Analyser/26-4/')
# filename = '2.79k-sincorreccion-probe'
for filename in os.listdir(path):
    filename = filename.split('.csv')[0]
    frec, Z, phase = np.loadtxt(f'{path}{filename}.csv', delimiter=',', skiprows=1, unpack=True)

    Zre = Z*np.cos(np.pi/180 * phase)
    Zim = Z*np.sin(np.pi/180 * phase)

    with open(f'EIS Analyser/26-4/{filename}.txt', 'w') as f:
        f.write(f'{len(frec)}\n')
        for i in range(len(frec)):
            f.write(f'{Zre[i]}\t{-Zim[i]}\t{frec[i]}\n')