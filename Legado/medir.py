import pyvisa
import numpy as np
import matplotlib.pyplot as plt
from save_csv import save_csv
from tqdm import tqdm
import time
import math
import os
from send_notification import mensaje_tel, foto_tel
from matplotlib.colors import LogNorm

#Si quieren usar un bot de telegram acá tienen que poner estos datos
api_token = ''
chat_id = ''

#%%
##################################################################
# CAMBIARLO EN CADA DIA Y EN CADA MEDICION
# Esto es simplemente para tener todo ordenado según el dia de medición
##################################################################

dia = '12-1'
#%%
##################################################################
# CORRERLO UNA VEZ POR DIA
# Lo mismo que lo anterior, esto crea las carpetas de cada día, si
# las carpetas ya existen tira error
##################################################################

os.mkdir(f'./results/Tonghui/{dia}')
os.mkdir(f'./results/Keithley/{dia}')
os.mkdir(f'./results/Osciloscopio/{dia}')
os.mkdir(f'./graficos/{dia}')

#%%
##################################################################
# INICIALIZAR KEITHLEY
# Importa el codigo para medir con el keithley
##################################################################
from Keithley_K2612B.keithleyK2612B import K2612B
from keithley2600 import Keithley2600

smu = K2612B('USB0::0x05E6::0x2614::4103593::INSTR') #Acá va el serial correspondiente al instrumento

#%%
##################################################################
# Curva IV
# Este bloque realiza un ciclo de remanencia y guarda el tiempo,
# el voltaje y la corriente tanto dinámicos como remanentes.
##################################################################
filename = '85-C-Al-Au(A1-B2)' #Nombre distintivo de los archivos que se guardan

Vmax = 5 #El valor máximo al que llega el ciclo
Vmin = -5 #El valor mínimo al que llega el ciclo
hslV = 0.4 #El voltaje de lectura en la remanencia
pw = 0.1 #El tiempo que dura el pulso
Npos = 50 #La cantidad de pulsos positivos
Nneg = 50 #La cantidad de pulsos negativos
rangei = 1e-3 #El rango en corriente del smu, solo puede ser: [1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 1.5]
limiti = 0.5 #La corriente límite
rangev = 2 #El rango en voltaje
cycles = 1 #Cantidad de ciclos a realizar
T1 = 0.01 #Tiempo de espera entre pulso de escritura y de lectura
T2 = 0.01 #Tiempo de espera entre pulso de lectura y de escritura
nplc = 0.5 #El nplc que utiliza el smu

#Acá realiza el ciclo y guarda todo en arrays
t_din, volt_din, curr_din, t_rem, volt_rem, curr_rem = smu.hsl(Vmax, Vmin, pw, Npos, Nneg, rangei, limiti, rangev, cycles, T1, T2, nplc, hslV)


hora = time.strftime("%H %M %S", time.localtime()) #Esto es solo para que en el nombre del archivo aparezca la hora
#Guarda los datos en un csv
save_csv(t_din, volt_din, curr_din, t_rem, volt_rem, curr_rem, filename=f'{filename}-({Vmin},{Vmax})-({hora})', root=f'./results/Keithley/{dia}/', delimiter=',', header=f'{time.ctime()}\n Tiempo dinamica [s], Voltaje dinamica [V], Corriente dinamica [A], Tiempo remanente [s], Voltaje remanente [V], Corriente remanente [A]\n Vmax={Vmax}, Vmin={Vmin}, Npos={Npos}, Nneg={Nneg}, pw={pw}, cycles={cycles}, hslV={hslV}, T1 = {T1}, T2 = {T2}, nplc={nplc}')

#Grafica los datos
plt.figure()
plt.scatter(volt_din, volt_rem/abs(curr_rem), c=t_rem, cmap='cool')
plt.xlabel('Voltaje [V]')
plt.ylabel('Resistencia [$\Omega$]')
plt.yscale('log')
plt.colorbar(label='Tiempo [s]')
plt.grid()
plt.show()

#Guarda el gráfico en un png
plt.savefig(f'./graficos/{dia}/{filename}-({Vmin},{Vmax})-({hora}).png', dpi=400)

#Manda un mensaje a un bot de telegram una vez que termina
mensaje_tel(
api_token = api_token,
chat_id = chat_id,
mensaje = f'{filename} Ya acabé'
)
foto_tel(api_token = api_token,
          chat_id = chat_id,
          file_opened = open(f'./graficos/{dia}/{filename}-({Vmin},{Vmax})-({hora}).png', 'rb'))

#%%
##################################################################
# Pulsos hasta R de umbral y despues lectura
# Realiza la cantidad de pulsos necesarios hasta llegar a un cierto umbral de R
# Se puede también leer la remanencia después de llegar al umbral
# Para determinar el umbral, se elige un porcentaje de la resistencia inicial
##################################################################
filename = '85-C-Al-Au(A1-B2)'

V = -4.8 #La amplitud en voltaje del pulso
# I = -6e-7 #La intensidad de corriente del pulso
Tmax = 0 #s El tiempo que se queda midiendo con pulsos de lectura luego de llegar al umbral
hslV = 0.4 #Voltaje de lectura
Twrite = 0.05 #Largo del pulso de escritura
Tread = 0.1 #Largo del pulso de lectura
rangei = 1e-3 #[1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 1.5]
limiti = 0.5
rangev = 2
ratioRth = 0.6 #Razón de la resistencia de umbral respecto a la inicial
Nth = 5 #Cantidad de pulsos máxima hasta llegar al umbral, si llega a este valor corta
T1 = 0.01 #Tiempo de espera entre pulso de escritura y de lectura
T2 = T1 #Tiempo de espera entre pulso de lectura y de escritura
nplc = 0.5 #El nplc que utiliza el smu

#Mensaje que avisa que arrancó a medir
mensaje_tel(
api_token = api_token,
chat_id = chat_id,
mensaje = f'Arranqué con el autoR {filename}'
)

#Los datos medidos, guarda todo lo mismo que un ciclo normal y además el Nfire y la resistencia de umbral
t_din, volt_din, curr_din, t_rem, volt_rem, curr_rem, Nfire, Rth = smu.autoR(V, Tmax, rangei, limiti, rangev, Twrite, Tread, T1, T2, nplc, Nth, hslV, ratioRth)
#Lo análogo para pulsos de corriente
# t_din, volt_din, curr_din, t_rem, volt_rem, curr_rem, Nfire, Rth = smu.autoR_I(I, Tmax, rangei, limiti, rangev, Twrite, Tread, T1, T2, nplc, Nth, hslV, ratioRth)

#Guarda los archivos con la hora, para el de corriente tienen un nombre distinto
hora = time.strftime("%H %M %S", time.localtime())
save_csv(t_rem, volt_rem, curr_rem, filename=f'{filename}-(autoR)-({V}V)-({hora})', root=f'./results/Keithley/{dia}/', delimiter=',', header=f'{time.ctime()}\n Tiempo remanente [s], Voltaje remanente [V], Corriente remanente [A]\n V={V}, Tmax={Tmax}, Twrite={Twrite}, Tread={Tread}, hslV={hslV}, T1 = {T1}, T2 = {T2}, nplc={nplc}, Nfire={Nfire}, ratioRth={ratioRth}, Rth={Rth}, Nth={Nth}')
# save_csv(t_rem, volt_rem, curr_rem, filename=f'{filename}-(autoR_I)-({I}A)-({hora})', root=f'./results/Keithley/{dia}/', delimiter=',', header=f'{time.ctime()}\n Tiempo remanente [s], Voltaje remanente [V], Corriente remanente [A]\n I={I}, Tmax={Tmax}, Twrite={Twrite}, Tread={Tread}, hslV={hslV}, T1 = {T1}, T2 = {T2}, nplc={nplc}, Nfire={Nfire}, ratioRth={ratioRth}, Rth={Rth}, Nth={Nth}')

#Genera el gráfico de la resistencia remanente en función del tiempo
plt.figure()
plt.plot(t_rem, abs(volt_rem/curr_rem), '-o')
plt.hlines(Rth, min(t_rem), max(t_rem), colors='k', linestyles='dashed')
plt.xlabel('Tiempo [s]')
plt.ylabel('Resistencia [$\Omega$]')
plt.yscale('log')
plt.grid()
plt.show()

plt.savefig(f'./graficos/{dia}/{filename}-(autoR)-({V}V)-({hora}).png', dpi=400)
# plt.savefig(f'./graficos/{dia}/{filename}-(autoR_I)-({I}A)-({hora}).png', dpi=400)


mensaje_tel(
api_token = api_token,
chat_id = chat_id,
mensaje = f'{filename} Ya acabé. {len(volt_din)} pulsos hasta el umbral'
)

foto_tel(api_token = api_token,
          chat_id = chat_id,
          file_opened = open(f'./graficos/{dia}/{filename}-(autoR)-({V}V)-({hora}).png', 'rb'))
# foto_tel(api_token = api_token,
#           chat_id = chat_id,
#           file_opened = open(f'./graficos/{dia}/{filename}-(autoR_I)-({I}A)-({hora}).png', 'rb'))

#%%
##################################################################
# Curva IV y despues autoR
# Esto es una unión entre las dos funciones anteriores, hecho para
# poder automatizar la medición del Nfire a la vez que se puede
# variar algún parámetro. En particular, ahora como está armado, se
# varian dos parámetros, pero se puede cambiar fácilmente. Los mensajes
# sirven para ir sabiendo el progreso de las mediciones
##################################################################
filename = '85-C-Al-Au(A1-B2)'

tons = [0.05] #Algún parámetro que se quiera variar
for ton in tons:
    # Pongo el try para que esto no tire error si no hay internet o algo asi y que siga midiendo
    try:
        mensaje_tel(
        api_token = api_token,
        chat_id = chat_id,
        mensaje = f'{filename} arranqué con {ton} s.'
        )
    except:
        pass
    Nfires = []
    paramsList = [-6e-7, -7e-7, -8e-7, -9e-7, -1e-8]*2 #Un segundo parámetro que se quiera variar
    
    for i, param in enumerate(paramsList):
        Vmax = 5
        Vmin = -5
        hslV = 0.4
        pw = 0.1
        Npos = 50
        Nneg = 0
        rangei = 1e-3 #[1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 1.5]
        limiti = 0.5
        rangev = 2
        cycles = 2
        T1 = 0.01
        T2 = 0.01
        nplc = 0.5
        
        t_din, volt_din, curr_din, t_rem, volt_rem, curr_rem = smu.hsl(Vmax, Vmin, pw, Npos, Nneg, rangei, limiti, rangev, cycles, T1, T2, nplc, hslV)
        hora = time.strftime("%H %M %S", time.localtime())
        save_csv(t_din, volt_din, curr_din, t_rem, volt_rem, curr_rem, filename=f'{filename}-({Vmin},{Vmax})-({hora})', root=f'./results/Keithley/{dia}/', delimiter=',', header=f'{time.ctime()}\n Tiempo dinamica [s], Voltaje dinamica [V], Corriente dinamica [A], Tiempo remanente [s], Voltaje remanente [V], Corriente remanente [A]\n Vmax={Vmax}, Vmin={Vmin}, Npos={Npos}, Nneg={Nneg}, pw={pw}, cycles={cycles}, hslV={hslV}, T1 = {T1}, T2 = {T2}, nplc={nplc}')
        
        plt.figure()
        plt.scatter(volt_din, abs(volt_rem/curr_rem), c=t_rem, cmap='cool')
        plt.xlabel('Voltaje [V]')
        plt.ylabel('Resistencia [$\Omega$]')
        plt.yscale('log')
        plt.colorbar(label='Tiempo [s]')
        plt.grid()
        plt.show()
        
        plt.savefig(f'./graficos/{dia}/{filename}-({Vmin},{Vmax})-({hora}).png', dpi=400)
        
        try:
            mensaje_tel(
            api_token = api_token,
            chat_id = chat_id,
            mensaje = f'{filename} Ya acabé'
            )
            foto_tel(api_token = api_token,
                      chat_id = chat_id,
                      file_opened = open(f'./graficos/{dia}/{filename}-({Vmin},{Vmax})-({hora}).png', 'rb'))
        except:
            pass
            
        
        # V = param
        I = param
        Tmax = 0 #s
        hslV = 0.4
        Twrite = ton
        Tread = 0.1
        rangei = 1e-3 #[1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 1.5]
        limiti = 0.5
        rangev = 2
        ratioRth = 0.6
        Nth = 50
        T1 = 0.01
        T2 = T1
        nplc = 0.5
        
        try:
            mensaje_tel(
            api_token = api_token,
            chat_id = chat_id,
            mensaje = f'Arranqué con el autoR {filename} con parámetro {param} ({i}/{len(paramsList)})'
            )
        except:
            pass
    
        # t_din, volt_din, curr_din, t_rem, volt_rem, curr_rem, Nfire, Rth = smu.autoR(V, Tmax, rangei, limiti, rangev, Twrite, Tread, T1, T2, nplc, Nth, hslV, ratioRth)
        t_din, volt_din, curr_din, t_rem, volt_rem, curr_rem, Nfire, Rth = smu.autoR_I(I, Tmax, rangei, limiti, rangev, Twrite, Tread, T1, T2, nplc, Nth, hslV, ratioRth)
    
        hora = time.strftime("%H %M %S", time.localtime())
        # save_csv(t_rem, volt_rem, curr_rem, filename=f'{filename}-(autoR)-({V}V)-({hora})', root=f'./results/Keithley/{dia}/', delimiter=',', header=f'{time.ctime()}\n Tiempo remanente [s], Voltaje remanente [V], Corriente remanente [A]\n V={V}, Tmax={Tmax}, Twrite={Twrite}, Tread={Tread}, hslV={hslV}, T1 = {T1}, T2 = {T2}, nplc={nplc}, Nfire={Nfire}, ratioRth={ratioRth}, Rth={Rth}, Nth={Nth}')
        save_csv(t_rem, volt_rem, curr_rem, filename=f'{filename}-(autoR_I)-({I}A)-({hora})', root=f'./results/Keithley/{dia}/', delimiter=',', header=f'{time.ctime()}\n Tiempo remanente [s], Voltaje remanente [V], Corriente remanente [A]\n I={I}, Tmax={Tmax}, Twrite={Twrite}, Tread={Tread}, hslV={hslV}, T1 = {T1}, T2 = {T2}, nplc={nplc}, Nfire={Nfire}, ratioRth={ratioRth}, Rth={Rth}, Nth={Nth}')

        
        Nfires.append(Nfire)
        
        plt.figure()
        plt.plot(t_rem, abs((volt_rem/curr_rem)), '-o')
        plt.hlines(Rth, min(t_rem), max(t_rem), colors='k', linestyles='dashed')
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Resistencia [$\Omega$]')
        plt.yscale('log')
        plt.grid()
        plt.show()
        
        # plt.savefig(f'./graficos/{dia}/{filename}-(autoR)-({V}V)-({hora}).png', dpi=400)
        plt.savefig(f'./graficos/{dia}/{filename}-(autoR_I)-({I}A)-({hora}).png', dpi=400)

        
        try:
            mensaje_tel(
            api_token = api_token,
            chat_id = chat_id,
            mensaje = f'{filename} con parámetro {param}. {len(volt_din)} pulsos hasta el umbral de {round(Rth*1e-6, 3)} MOhms'
            )
            
            # foto_tel(api_token = api_token,
            #           chat_id = chat_id,
            #           file_opened = open(f'./graficos/{dia}/{filename}-(autoR)-({V}V)-({hora}).png', 'rb'))
            
            foto_tel(api_token = api_token,
                      chat_id = chat_id,
                      file_opened = open(f'./graficos/{dia}/{filename}-(autoR_I)-({I}A)-({hora}).png', 'rb'))
        except:
            pass
        time.sleep(60)
    
    # Gráfico del Nfire en función del parámetro variado
    x = np.array(paramsList)
    y =  np.array(Nfires)
    
    plt.figure()
    plt.scatter(x, y)
    plt.xlabel('Parámetro')
    plt.ylabel('Nfire')
    plt.yscale('log')
    plt.grid()
    plt.show()
    
    # plt.savefig(f'./graficos/{dia}/{filename}-(Nfires)-({V}V)-({hora}).png', dpi=400)
    plt.savefig(f'./graficos/{dia}/{filename}-(Nfires)-({I}A)-({hora}).png', dpi=400)
    try:
        # foto_tel(api_token = api_token,
        #           chat_id = chat_id,
        #           file_opened = open(f'./graficos/{dia}/{filename}-(Nfires)-({V}V)-({hora}).png', 'rb'))
        
        foto_tel(api_token = api_token,
                  chat_id = chat_id,
                  file_opened = open(f'./graficos/{dia}/{filename}-(Nfires)-({I}A)-({hora}).png', 'rb'))
    except:
        pass
    
    #Esto es en el caso que tengan alguna configuración medida varias veces, para hacer el promedio
    y_mean = []
    for i in np.unique(x):
      y_mean.append(np.mean(y[np.where(x == i)]))
    
    plt.figure()
    plt.scatter(np.unique(x), y_mean)
    plt.xlabel('Parámetro')
    plt.ylabel('Nfire promedio')
    plt.yscale('log')
    plt.grid()
    plt.show()
    
    # plt.savefig(f'./graficos/{dia}/{filename}-(Nfires_mean)-({V}V)-({hora}).png', dpi=400)
    plt.savefig(f'./graficos/{dia}/{filename}-(Nfires_mean)-({I}A)-({hora}).png', dpi=400)
    try:
        # foto_tel(api_token = api_token,
        #           chat_id = chat_id,
        #           file_opened = open(f'./graficos/{dia}/{filename}-(Nfires_mean)-({V}V)-({hora}).png', 'rb'))
        
        foto_tel(api_token = api_token,
                  chat_id = chat_id,
                  file_opened = open(f'./graficos/{dia}/{filename}-(Nfires_mean)-({I}A)-({hora}).png', 'rb'))
    except:
        pass
    
    plt.close('all')

#%%
##################################################################
# Voltaje custom (acumulacion de pulsos)
# Esto es para realizar un ciclo pero pudiendo modificar los voltajes
# de escritura como se quiera. No hace lecturas en remanencia
##################################################################
filename = '80-Al-Au(C3-C4)'

#Acá creo el array de voltaje de escritura, está hecho muy manualmente, depende lo que se quiera se puede hacer mejor
volt_meas = []
for i in np.concatenate((np.linspace(0, 8, 50, endpoint=False), np.linspace(8, 0, 50, endpoint=False), np.linspace(0, -3, 50, endpoint=False), np.linspace(-3, 0, 50, endpoint=False))):
    volt_meas.append(0.4)
    volt_meas.append(i)


pw = 0.1
rangei = 1e-3 #[1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 1.5]
limiti = 0.5
rangev = 2
T = 0.01
nplc = 0.5

t, volt, curr = smu.custom_volt(volt_meas, pw, rangei, limiti, rangev, T, nplc)
print(0.4/curr*1e-6)


hora = time.strftime("%H %M %S", time.localtime())
save_csv(t, volt, curr, filename=f'{filename}-(tren-pulsos)-({hora})', root=f'./results/Keithley/{dia}/', delimiter=',', header=f'{time.ctime()}\n Tiempo [s], Voltaje [V], Corriente [A]\n  pw={pw}, T = {T}, nplc={nplc}')

# mensaje_tel(
# api_token = api_token,
# chat_id = chat_id,
# mensaje = f'{filename} Ya acabé'
# )

plt.figure()
plt.scatter(volt[1::2], abs(volt/curr)[:-1:2], c=t[:-1:2], cmap='cool')
plt.yscale('log')
plt.grid()

plt.figure()
plt.plot(t[100:], (volt/curr)[100:], '-o')
plt.xlabel('Tiempo [s]')
plt.ylabel('Resistencia [$\Omega$]')
# plt.ylabel('Corriente [A]')
plt.grid()
plt.show()

plt.savefig(f'./graficos/{dia}/{filename}-(tren-pulsos)-({hora}).png', dpi=400)


# foto_tel(api_token = api_token,
#           chat_id = chat_id,
#           file_opened = open(f'./graficos/{dia}/{filename}-(tren-pulsos)-({hora}).png', 'rb'))

#%%
##################################################################
# IMPORTS PARA OSCILOSCOPIO
##################################################################
from TektronixTDS1002B import TDS1002B

osci = TDS1002B('USB0::0x0699::0x0413::C012302::INSTR')
#%%
##################################################################
# OSCILOSCOPIO Y KEITHLEY
# Este es un codigo que utilizamos para medir los pulsos con un
# osciloscopio para chequear que manda lo que debe, de forma un poco
# sistematica
##################################################################
Vmax = 5
Vmin = -5
hslV = 0.4
pw = 0.1
Npos = 2
Nneg = 0
rangei = 1e-3 #[1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 1.5]
limiti = 0.5
rangev = 2
cycles = 2
T1 = 0.01
T2 = 0.01
nplc = 0.5

for i in np.linspace(0, 1, 25):
    osci.set_time((i+0.01))
    time.sleep(i)
    smu.hsl(Vmax, Vmin, i, Npos, Nneg, rangei, limiti, rangev, cycles, T1, T2, nplc, hslV)
    time.sleep(11*i)

    plt.figure()

    t1, ch1 = osci.read_data(1)

    plt.plot(t1, ch1)

    save_csv(t1, ch1, filename=f'Pulsos-{i}', root=f'./results/Osciloscopio/{dia}/')


#%%
##################################################################
# IMPORTS PARA TONGHUI
##################################################################
plt.close('all')
from Tonghui_TH283X.TonghuiTH283X import TH283X

lcr = TH283X('USB0::0x0471::0x2827::QF40900001::INSTR')
#%%
##################################################################
# CICLO DE BIAS CON EL TONGHUI
# Código para realizar mediciones con el tonghui variando el bias
##################################################################
filename = '80-Al-Au(C3-C4)'

# level = 0.1
# lcr.set_volt(level)
bias_list = [0]
level_list = [0.4]

if not (len(bias_list) == len(level_list)):
    input('No hay la misma cantidad de valores')


frecs = np.unique(np.loadtxt('Tonghui_TH283X/results/Caracterización/frecuencia-LCR.csv', delimiter=',', unpack=True, skiprows=2)[1])
# frecs = np.concatenate((frecs[:300:10], frecs[300:600:5], frecs[600:]))
# plt.plot(frecs, 'o')
# plt.yscale('log')
# frecs = frecs[87:]
i = 0
for bias,level in zip(bias_list, level_list):
    lcr.set_volt(level) #Setea el level
    
    mensaje_tel(
    api_token = api_token,
    chat_id = chat_id,
    mensaje = f'{time.ctime()}\n{i}/{len(bias_list)} - Arranco con {bias}V de bias'
    )
    
    hora = time.strftime("%H %M %S", time.localtime())
    # lcr.set_DC_bias_volt(bias)
    
    #Realiza el EI, en las frecuencias seleccionadas, 'ZTD' es la función con la que mide, y el fast fueron intentos para
    #hacer más rapida la medición y no aportó mucho, dejarlo en False
    f, Z, phase = lcr.make_EI(frecs, 'ZTD', fast=False)
    save_csv(f, Z, phase, filename = f'{filename}-level{level}V-bias{bias}V-({hora})', root=f'./results/Tonghui/{dia}/', delimiter=',', header=f'{time.ctime()}\n Frecuencia [Hz], Z [Ohm], Fase [deg]')
    
    plt.savefig(f'./graficos/{dia}/{filename}-level{level}V-bias{bias}V-({hora}).png', dpi=400)
    
    plt.figure()
    Zre = Z*np.cos(phase*np.pi/180)
    Zim = Z*np.sin(phase*np.pi/180)
    plt.scatter(Zre, -Zim, c=f, cmap='cool', norm=LogNorm())
    plt.colorbar(label='Frecuencia [Hz]')
    plt.grid()
    plt.xlabel('Re(Z) [$\Omega$]')
    plt.ylabel('-Im(Z) [$\Omega$]')

    plt.savefig(f'./graficos/{dia}/{filename}-level{level}V-bias{bias}V-({hora})-nyquist.png', dpi=400)
    
    mensaje_tel(
    api_token = api_token,
    chat_id = chat_id,
    mensaje = f'{i+1}/{len(bias_list)} - Ya acabé con {bias}V de bias'
    )
    
    foto_tel(api_token = api_token,
             chat_id = chat_id,
             file_opened = open(f'./graficos/{dia}/{filename}-level{level}V-bias{bias}V-({hora}).png', 'rb'))
    foto_tel(api_token = api_token,
             chat_id = chat_id,
             file_opened = open(f'./graficos/{dia}/{filename}-level{level}V-bias{bias}V-({hora})-nyquist.png', 'rb'))
    i += 1

# Deja el voltaje después de medir en lo mínimo que puede, no tiene forma de apagarse
lcr.set_volt(0.01)
