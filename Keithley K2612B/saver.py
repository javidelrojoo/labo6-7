# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 12:01:57 2018

@author: gsanca
"""

"""
SCRIPT TO SAVE DATA GENERATED FROM listIV TEST
"""


import functions
from runner import setup

def caster(string):
    out = []
    for values in string.split(','):
        aux = values
        out.append(float(aux))
    return out

def saveME(smu,whichSMU):
    
    config    = setup()
    plotFlag  = 1 #config[11]
    saveFlag  = 1 #config[12]
    metaData  = config[18]
    
    
    [t,volt,curr] = functions.readBuffer(smu,whichSMU)
#    times       = caster(t)
#    readingsI   = caster(curr)
#    readingsV   = caster(volt)

    times       = caster(t)
    readingsI   = caster(curr)
    readingsV   = caster(volt)


#    calculatedR = []
#    if len(readingsV) == len(readingsI):
#        i = 0
#        for voltage in readingsV:
#            calculatedR.append(voltage/readingsI[i])
#            i = i + 1
    
    
    # Plotting and saving data
    if plotFlag:
        #graph = functions.plot(times,readingsV)
        graph = functions.plot(readingsV,readingsI)
    else:
        graph = 'NULL'
    if saveFlag:
        functions.save(times,readingsV,readingsI,metaData,graph)

