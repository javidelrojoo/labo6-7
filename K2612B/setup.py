# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 15:18:43 2018

@author: gsanca
"""

def setup():
    
    
    # -------------------------------------------------------------------------
    # Modify this values
    # -------------------------------------------------------------------------
    #testType      = 'iv'            # Test type: iv, pulse, badPulse  
    #number        = 1      
    #voltOrCurrent = 'V'             # Modo tension/corriente
    #idaVuelta     = 1               # Realizar la medición con ida y vuelta
    #zeros_mid     = 1 # Agregar ceros (pulsed mode)
    #vRang         = 20
    #iRang         = 'AUTO' #0.01

    rev             = 0                 # Invert fase
    i_cc            = 0.5               # Compliance current
    v_cc            = 5                 # Compliance voltage
    cycles          = 1       
    pw              = 100E-03           # Pulse width
    T               = 800E-03           # Period
    HSL             = 'ON'              # Hysteresis switching loop flag
    levelHSL        = 0.2               # Reading level
    nplc            = 0.001
    
    # Saving preferences
    # -------------------------------------------------------------------------
    plotFlag      = 1                   # Plot 
    saveFlag      = 1                   # Save data in *.csv

    # Voltage setup
    # -------------------------------------------------------------------------    
    # Positive values 
    voltStep      = 0.5
    voltStop      = 3


    # -------------------------------------------------------------------------
    # End setup
    # -------------------------------------------------------------------------
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    top     = voltStop
    step    = voltStep
    hslV    = levelHSL
    limitI  = i_cc
    limitV  = v_cc

    if HSL == 'ON':
        hslF = 1
    elif HSL == 'OFF':
        hslF = 0
    else:
        hslF = 0

 
    metaData = ["Test type   = IV curve" 
                ",reverse = " + str(rev) + 
                "I_limit     = " + str(i_cc),
                "V_limit     = " + str(v_cc),
                "Pulse width = " + str(pw),
                "Period      = " + str(T),
                "HSL (level) = " + str(HSL) +" ("+str(levelHSL)+" V)"]   
    
    return [top,
            step,
            rev,
            hslV,
            hslF,
            cycles,
            T,
            pw,
            limitI,
            limitV,
            nplc,
            plotFlag,
            saveFlag,
            metaData]