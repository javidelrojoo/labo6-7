# -*- coding: utf-8 -*-
"""
|===================================================================|
|                                                                   |
|                           ECyT.UNSAM                              |
|                           LINE - 2018                             |
|                                                                   |
|===================================================================|
|                                                                   |
|              oMMMMMMMMMMMMMMMMmymMMMMMMMMMMMMMMMMo                |    
|              oMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMo                |       
|              oMMMMMd++++oosyhmMMMmhysoo++++dMMMMMo                |       
|              oMMMMMy          .+.          sMMMMMo                |       
|              oMMMMMs                       sMMMMMo                |       
|              oMMMMMs                       sMMMMMo                |       
|              oMMMMMs                       sMMMMMo                |       
|              oMMMMMs                       sMMMMMo                |       
|              oMMMMMs                       sMMMMMo                |                       
|              oMMMMMs                       sMMMMMo                |       
|              oMMMMMs                       sMMMMMo                |       
|              oMMMMMmyyyysso+:.   .:+ossyyyymMMMMMo                |       
|              oMMMMMMMMMMMMMMMMmymMMMMMMMMMMMMMMMMo                |       
|              oMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMo                |       
|              -//////////++oshmMMMmhsoo+//////////-                |       
|                               `/`                                 |           
|                                                                   |
|===================================================================| 
|===================================================================|
|  Script para controlar remotamente la SMU k2612B                  |
|                                                                   |                        
|  User: gsanca                                                     |
|    This file is the main function. Do not edit this.              |
|                                                                   |
|====================================================================
|                                                                   |
|  You must have:                                                   |
|      - setup.py                                                   |
|      - test.py                                                    |
|      - functions.py                                               |
|                                                                   |     
|  And install the followings libs:                                 |
|      - visa                                                       |
|      - time                                                       |
|      - numpy                                                      |
|      - matplotlib                                                 |
|      - re                                                         |
|      - os                                                         |
|===================================================================|
Created on Fri Jul 27 17:35:22 2018

@author: gsanca
"""

def k2612B(option):
    
    from functions import clear_all, gpib, plot, save, startSMU, loadScripts
    from setup import setup
    import tests
    from time import sleep
    
    clear_all()
    
    print("k2612B Controlling interface for python")
    print("Author: G. A. Sanca - gsanca@unsam.edu.ar")
    
    # Initializate GPIB
    gpibAdrress = '0x05E6::0x2614::4103593'
    [smu,rm]    = gpib(gpibAdrress)
    
    startSMU(smu)
    sleep(1)
    loadScripts(smu)
    sleep(1)
    
    # Loading setups configurations
    config    = setup()
    plotFlag  = config[11]
    saveFlag  = config[12]
    metaData  = config[13]
    
    print("\n")
    print("Starting measurement...")
    input("Press ENTER to continue...")
    
    if option == 0:
        # Running tests 
        tests.IVlist(smu)
        rm.close
        
    elif option == 1:
        
        [t, readingsV, readingsI, calculatedR] = tests.readIV(smu)
        # Plotting and saving data
        if plotFlag:
            graph = plot(readingsV,readingsI)
        else:
            graph = 'NULL'
        if saveFlag:
            save(t,readingsV,readingsI,calculatedR,metaData,graph)

    elif option == 2:
        print("hola")

k2612B(0)
