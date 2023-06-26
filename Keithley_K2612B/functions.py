# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 20:17:35 2018

@author: gsanca
"""

import pyvisa
import time
import matplotlib.pyplot as plt
import os
import numpy as np

"""
List of auxiliary functions needed to program the k2612B equipment
"""



"""
-------------------------------------------------------------------------------
Miscellaneous functions
-------------------------------------------------------------------------------
"""
def date_time_now():
    """
    date_time_now returns the date and file string made with date
    """
    # Date settings
    today       = time.localtime()
    Year        = str(today.tm_year)    
    reduceYear  = str(today.tm_year)[2:]
    completeMon = str(today.tm_mon ).zfill(2)
    completeDay = str(today.tm_mday).zfill(2)
    completeHs  = str(today.tm_hour).zfill(2)
    completeMin = str(today.tm_min ).zfill(2)
    completeSec = str(today.tm_sec ).zfill(2)
    dateString  = reduceYear + completeMon + completeDay + completeHs + completeMin + completeSec

    # File name
    filestring  = Year + completeMon + completeDay       

    # Complate Date
    complete_date = Year + "/" + completeMon + "/" + completeDay + " " + completeHs + ":" + completeMin + ":" + completeSec       

    return [filestring,complete_date,dateString]

#------------------------------------------------------------------------------
def clear_all():
    """
    Clears all the variables from the workspace of the spyder application.
    """
    gl = globals().copy()
    for var in gl:
        if var[0] == '_': continue
        if 'func' in str(globals()[var]): continue
        if 'module' in str(globals()[var]): continue

        del globals()[var]

#------------------------------------------------------------------------------
def plot(x, y):
    """
    Plot function. Use this function to plot IV curves.
    """
    graph = plt.figure()
    #plt.hold(True)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.plot(x, y, '.', linewidth = 1.0, label = 'iv')
    #plt.legend(loc = 'best')
    plt.xlabel('Voltage [V]', fontsize = 14)
    plt.ylabel('Current [A]', fontsize = 14)
    plt.grid(True)
    #plt.hold(False)
    plt.show()
    
    return graph

#------------------------------------------------------------------------------   
def save(times, readingsV, readingsI, metaData, graph):
    """
    Save function. Use this to save data in file. The file name is given by
    the day and hour, in format: yymmddhhmmss. 
    Use this function to save V, I and R data (and meta data).
    """
    [unused,completeDate,dateString] = date_time_now()
    # For makin this cross platform, change the path name
    path          = ".\\results\\"
    ext_fig       = ".png" 
    ext_txt       = ".csv" 
    figure_name   = path + dateString + ext_fig
    text_name     = path + dateString + ext_txt
    """
    Check if the folder exist. This is only Windows compatible (because of VISA)
    """
    if not(os.path.exists(path)):
        os.makedirs(path)
    File = open(text_name, 'w')
    
    """
    Header:
         - date:hour
         - metaData:
                 - configuration
    """    
    File.write("\n") 
    File.write(completeDate + "\n")
    for lines in metaData:
        File.write(lines + "\n")
    File.write("\n")
    File.write("Time\tV\tI\tR\n")
    if len(readingsV) == len(readingsI): 
        for i in range(0,len(readingsV)):
            line = str(times[i]) + '\t' + str(readingsV[i]) + '\t' + str(readingsI[i]) + '\t' +'\n' 
            File.write(line)
    File.close()
    if graph != 'NULL':
        graph.savefig(figure_name, dpi=250, bbox_inches='tight')
    print("Saved as... ")
    print(path + dateString + ".*")


#------------------------------------------------------------------------------
def caster(string):
    out = []
    for values in string.split('\t'):
        aux = values
        out.append(float(aux))
    return out

""" End miscellaneous """


"""
-------------------------------------------------------------------------------
Communication functions
-------------------------------------------------------------------------------
"""
def gpib(address):

    rm          = pyvisa.ResourceManager()
    equiment_id = 'USB0::' + str(address) + '::INSTR'
    smu         = rm.open_resource(equiment_id)
    """
    smu.write('waitcomplete()') 
    time.sleep(1)
    smu.write('reset()')    
    print("Installed equipment:")
    print(smu.query("*IDN?")) 
    smu.write('smua.reset()')
    """
    return smu,rm

""" End communication """

"""----------------------------------------------------------------------------
Configuration functions
----------------------------------------------------------------------------"""
def startSMU(smu):
    smu.write('reset()')
    loadTSP("misc",smu)
    smu.write('beeper.enable = 0')
    smu.write('welcome()')
    initBuffers(smu)
    
    
#------------------------------------------------------------------------------
    
def initBuffers(smu):
    smu.write('init_buffers(smua)')
    smu.write('init_buffers(smub)')
    smu.write('format.data = format.ASCII')


""" End config """


"""----------------------------------------------------------------------------
TSP functions
----------------------------------------------------------------------------"""
def theFunction(smu,start, stop, points, pW, T, limitV, nplc, remote):
    startSMU(smu)
    initBuffers(smu)
    command = "PulsedSweepVSingle(" + str(start) +","+ str(stop) +","+ str(points) +","+ str(pW) +","+ str(T) +","+ str(limitV) +","+ str(nplc) +","+ str(remote) + ")"
    # smu.write(command)
    """
    
    TODO: Ver que pasa con el read buffer
    
    KE26XXB_Pulsed_Sweep_Single
    
    """
    results = []
    header  = smu.query(command)
    # time.sleep((points+2)*T)
    # smu.query('*OPC?')
    while header != 'Time\tVoltage\tCurrent\n':
        header = smu.query("")
    for i in range(points):
        aux = smu.query("")
        results.append(aux.split('\n')) 
    tiempo = np.zeros(points)
    voltage = np.zeros(points)
    current = np.zeros(points)
    for i, result in enumerate(results):
        tiempo[i], voltage[i], current[i] = result[0].split('\t')
    
    return tiempo, voltage, current
    
    #current = smu.query("printbuffer(1,10,smua.nvbuffer1)")
    #voltage = smu.query("printbuffer(1,10,smua.nvbuffer2)")
    
    # current = smu.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1)')
    # voltage = smu.query('printbuffer(1, smub.nvbuffer2.n, smub.nvbuffer2)')
    # time    = smu.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.timestamps)')
    # x       = caster(voltage)
    # y       = caster(current)
    # t       = caster(time)
    # return t,x,y,voltage,current,time

#------------------------------------------------------------------------------
def loadScripts(smu):
    scriptsInFolder = []
    for file in [doc for doc in os.listdir(".\\Keithley_K2612B\\tsp\\") if doc.endswith(".tsp")]:
        filename, file_extension = os.path.splitext(file)
        msg = "Loaded script: " + filename + file_extension
        print(msg)
        scriptsInFolder.append(filename)
        loadTSP(filename,smu)
    return scriptsInFolder

#------------------------------------------------------------------------------
def loadTSP(scriptName,smu):
    """
    This function load the TSP scripts and send them to the k2612B 
    and run the specific script.
    """    
    path     = ".\\Keithley_K2612B\\tsp\\"
    script   = str(scriptName)
    fileName = path + script
    #File     = open(fileName, 'r')
    File     = open(fileName + '.tsp', 'r')
    
    smu.write('reset()')
    smu.write('loadscript ' + script)
    for line in File:
        smu.write(line.strip('\n'))
    smu.write('endscript') 
    smu.write(script + '.run()')

#------------------------------------------------------------------------------
    
def readBuffer(smu, whichSMU):
    time.sleep(5)
    try:
        if whichSMU == "a":
            curr    = smu.query('printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1)')
            volt    = smu.query('printbuffer(1, smua.nvbuffer2.n, smua.nvbuffer2)')
            times    = smu.query('printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.timestamps)')
        
        else:    
            curr    = smu.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1)')
            volt    = smu.query('printbuffer(1, smub.nvbuffer2.n, smub.nvbuffer2)')
            times    = smu.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.timestamps)')
    except ValueError:
        time.sleep(1)
        readBuffer(smu, whichSMU)
    
    
    t = times.strip('\n')
    volt = volt.strip('\n')
    curr = curr.strip('\n')
    
    t = np.array([float(i) for i in t.split(',')])
    volt = np.array([float(i) for i in volt.split(',')])
    curr = np.array([float(i) for i in curr.split(',')])
    
    while not np.array_equal(t,np.sort(t)):
        curr, t, volt = t, volt, curr
        
    return t,volt,curr  
    
    
    
    
    
    
    
    
    
















    
    
    
    
    
    
#------------------------------------------------------------------------------
def configSMU_A(smu):
    ###########################################################################
    # Config
    ###########################################################################
    smu.write("smua.reset()") 
    smu.write("errorqueue.clear()")
    smu.write("smua.source.func = smua.OUTPUT_DCVOLTS")
    smu.write("smua.source.autorangev = smua.AUTORANGE_ON")
    smu.write("smua.measure.autorangei = smua.AUTORANGE_ON")
    smu.write("format.data = format.ASCII") 
    smu.write("smua.nvbuffer1.clear()") 
    smu.write("smua.nvbuffer1.appendmode = 1") 
    smu.write("smua.nvbuffer1.collectsourcevalues = 1")
    smu.write("smua.nvbuffer2.clear()") 
    smu.write("smua.nvbuffer2.appendmode = 1") 
    smu.write("smua.nvbuffer2.collectsourcevalues = 1") 
    smu.write("smua.measure.count = 1") 
    smu.write("smua.source.output =smua.OUTPUT_ON") 




