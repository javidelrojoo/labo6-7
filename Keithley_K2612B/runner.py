# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 12:09:07 2018

@author: gsanca
"""


"""
SCRIPT TO RUN THE listIV FUNCTION
"""

import numpy as np

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
    sample          = "test-1" # Sb70Te30_20190821_L16_W2_(2,1) , sample-1-Palermo_2B-aniserie   
    
    Vpos            = 3.0
    Vneg            = 6.0
    stepPos         = 0.25
    stepNeg         = 0.25
    
    Vgate           = 0
    TR              = 0
    
    rev             = 0              # Invert fase
    limitI          = 50E-02         # Compliance current
    rangeI          = 10E-2
    limitV          = 20             # Compliance voltage      
    rangeV          = 20
    T               = 0.15            # Period #1s
    pw              = 0.05          # 10 ms
    hslF            = 0              # Hysteresis switching loop flag
    hslV            = 0           # Reading level
    nplc            = 0.001
    cycles          = 1
    
    # Pulses
    # -------------------------------------------------------------------------
    V1              = 3
    V2              = -6
    n_1             = 1
    n_2             = 1
    v_read          = -0.5



    if hslF == 0:
        HSL  = 'OFF'
    elif hslF == 1:
        HSL  = 'ON'
    else:
        HSL  = 'OFF'
        hslF = 0
    if not TR:
        Vgate = 'NONE'
        
    
    # Saving preferences
    # -------------------------------------------------------------------------
    plotFlag      = 1                   # Plot 
    saveFlag      = 1                   # Save data in *.csv

    # Voltage setup
    # -------------------------------------------------------------------------    
    # Positive values 
    voltStep      = 0.5
    voltStop      = 3.5


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
 
    metaData = ["Sample         \t" + sample,
                "Test type      \t IV curve \tCycles = " + str(cycles), 
                "Reverse        \t" + str(rev),
                "V stop pos     \t" + str(Vpos),
                "V step pos     \t" + str(stepPos), 
                "V stop neg     \t" + str(Vneg),
                "V step neg     \t" + str(stepNeg), 
                "I_limit        \t" + str(limitI),
                "I_range        \t" + str(rangeI),
                "V_limit        \t" + str(limitV),
                "Pulse width    \t" + str(pw),
                "Period         \t" + str(T),
                "HSL            \t" + str(HSL) +"\t"+ str(hslV) +"\t"+ "v_read" +"\t"+ str(v_read) ,
                "nplc           \t" + str(nplc),
                "Vgate          \t" + str(Vgate)]   
    
    return [Vpos,
            Vneg,
            stepPos,
            stepNeg,
            rev,
            hslV,
            hslF,
            cycles,
            T,
            pw,
            limitI,
            limitV,
            nplc,
            V1,
            V2,
            n_1,
            n_2,
            v_read,
            metaData,
            Vgate,
            rangeI,
            rangeV]


    
def set_su(limitI):
        
    sample          = "sample_1_palermo-D(1,8)"      #sample_1_palermo-C(-1,-1) sample_1_palermo-A-5-3  3-BC31#01
    Vpos            = 3
    Vneg            = 0
    stepPos         = 0.05
    stepNeg         = 0.05    
    Vgate           = 0 
    rev             = 0               # Invert fase
    #limitI          = 50E-03          # Compliance current
    rangeI          = limitI
    limitV          = 20              # Compliance voltage      
    rangeV          = 20
    T               = 100E-03             # Period #1s
    pw              = 10E-03           # 10 ms
    hslF            = 0              # Hysteresis switching loop flag
    hslV            = -0.22           # Reading level
    nplc            = 0.001
    cycles          = 1

    HSL  = 'OFF'
    Vgate = 'NONE'
    
 
    metaData = ["Sample         \t" + sample,
                "Test type      \t IV curve \tCycles = " + str(cycles), 
                "Reverse        \t" + str(rev),
                "V stop pos     \t" + str(Vpos),
                "V step pos     \t" + str(stepPos), 
                "V stop neg     \t" + str(Vneg),
                "V step neg     \t" + str(stepNeg), 
                "I_limit        \t" + str(limitI),
                "I_range        \t" + str(rangeI),
                "V_limit        \t" + str(limitV),
                "Pulse width    \t" + str(pw),
                "Period         \t" + str(T),
                "HSL            \t" + str(HSL) +"\t"+ str(hslV) +"\t"+ "v_read" +"\t"+ str(0) ,
                "nplc           \t" + str(nplc),
                "Vgate          \t" + str(Vgate)]   
    
    return [Vpos,Vneg,stepPos,stepNeg,rev,hslV,hslF,cycles,T,pw,limitI,limitV,
            nplc,0,0,0,0,0,metaData,Vgate,rangeI,rangeV]    
    
def reset_su():
        
    sample          = "sample_1_palermo-D(1,8)"      #sample_1_palermo-C(-1,-1) sample_1_palermo-A-5-3  3-BC31#01
    Vpos            = 0
    Vneg            = 3
    stepPos         = 0.05
    stepNeg         = 0.05    
    Vgate           = 0
    rev             = 0               # Invert fase
    limitI          = 50E-03          # Compliance current
    rangeI          = 50E-03
    limitV          = 20              # Compliance voltage      
    rangeV          = 20
    T               = 100E-03             # Period #1s
    pw              = 10E-03           # 10 ms
    hslF            = 0              # Hysteresis switching loop flag
    hslV            = -0.22           # Reading level
    nplc            = 0.001
    cycles          = 1
    
    HSL  = 'OFF'
    Vgate = 'NONE'

    metaData = ["Sample         \t" + sample,
                "Test type      \t IV curve \tCycles = " + str(cycles), 
                "Reverse        \t" + str(rev),
                "V stop pos     \t" + str(Vpos),
                "V step pos     \t" + str(stepPos), 
                "V stop neg     \t" + str(Vneg),
                "V step neg     \t" + str(stepNeg), 
                "I_limit        \t" + str(limitI),
                "I_range        \t" + str(rangeI),
                "V_limit        \t" + str(limitV),
                "Pulse width    \t" + str(pw),
                "Period         \t" + str(T),
                "HSL            \t" + str(HSL) +"\t"+ str(hslV) +"\t"+ "v_read" +"\t"+ str(0) ,
                "nplc           \t" + str(nplc),
                "Vgate          \t" + str(Vgate)]   
    
    return [Vpos,Vneg,stepPos,stepNeg,rev,hslV,hslF,cycles,T,pw,limitI,limitV,
            nplc,0,0,0,0,0,metaData,Vgate,rangeI,rangeV]    

def read_su():
        
    sample          = "sample_1_palermo-D(1,8)"      #sample_1_palermo-C(-1,-1) sample_1_palermo-A-5-3  3-BC31#01
    Vpos            = 0.5
    Vneg            = 0.5
    stepPos         = 0.05
    stepNeg         = 0.05    
    Vgate           = 0    
    rev             = 0               # Invert fase
    limitI          = 50E-03          # Compliance current
    rangeI          = 50E-03
    limitV          = 20              # Compliance voltage      
    rangeV          = 20
    T               = 100E-03             # Period #1s
    pw              = 10E-03           # 10 ms
    hslF            = 0              # Hysteresis switching loop flag
    hslV            = -0.22           # Reading level
    nplc            = 0.001
    cycles          = 1
    
    HSL   = 'OFF'
    Vgate = 'NONE'

 
    metaData = ["Sample         \t" + sample,
                "Test type      \t IV curve \tCycles = " + str(cycles), 
                "Reverse        \t" + str(rev),
                "V stop pos     \t" + str(Vpos),
                "V step pos     \t" + str(stepPos), 
                "V stop neg     \t" + str(Vneg),
                "V step neg     \t" + str(stepNeg), 
                "I_limit        \t" + str(limitI),
                "I_range        \t" + str(rangeI),
                "V_limit        \t" + str(limitV),
                "Pulse width    \t" + str(pw),
                "Period         \t" + str(T),
                "HSL            \t" + str(HSL) +"\t"+ str(hslV) +"\t"+ "v_read" +"\t"+ str(0) ,
                "nplc           \t" + str(nplc),
                "Vgate          \t" + str(Vgate)]   
    
    return [Vpos,Vneg,stepPos,stepNeg,rev,hslV,hslF,cycles,T,pw,limitI,limitV,
            nplc,0,0,0,0,0,metaData,Vgate,rangeI,rangeV]    

def experiment():
    
    i_cc = [50E-03,40E-03,30E-03,20E-03,10E-03]

    for currents in i_cc:
        set_su(currents)
        iv()
        read_su()
        iv()
        reset_su()
        iv()
        read_su()
        
        set_su(currents)
        iv()
        read_su()
        iv()
        reset_su()
        iv()
        read_su()



def IVlist(smu,Vpos,Vneg,stepPos,stepNeg,rev,hslV,hslF,cycles,T,pw,limitI,rangeI,limitV,rangeV,nplc):
        
    """
    list_iv(Vpos,Vneg,stepPos,stepNeg,rev,hslV,hslF,cycles,T,pw,limitI,limitV,nplc)
    """
    paramsStr =     (str(Vpos)      + "," +
                    str(Vneg)       + "," +
                    str(stepPos)    + "," +
                    str(stepNeg)    + "," +
                    str(rev)        + "," +
                    str(hslV)       + "," +
                    str(hslF)       + "," +
                    str(cycles)     + "," +
                    str(T)          + "," +
                    str(pw)         + "," +
                    str(limitI)     + "," +
                    str(rangeI)     + "," +
                    str(limitV)     + "," +
                    str(rangeV)     + "," +
                    str(nplc))

    commandStr = "list_iv(" + paramsStr + ")" 
    
    # Vpos,Vneg,stepPos,stepNeg,rev,hslV,hslF,cycles,T,pw,limitI,limitV,nplc
    #commandStr = "list_iv(1,0.5,0.5,0.1,0,0.2,0,1,0.1,0.01,0.03,10,0.001)"
    smu.write(commandStr)
    
    
def IVlist_1T1R(smu,Vpos,Vneg,stepPos,stepNeg,Vgate,rev,hslV,hslF,cycles,T,pw,limitI,rangeI,limitV,rangeV,nplc):
        
    """
    list_iv(Vpos,Vneg,stepPos,stepNeg,Vgate,rev,hslV,hslF,cycles,T,pw,limitI,limitV,nplc)
    """
    paramsStr =     (str(Vpos)      + "," +
                    str(Vneg)       + "," +
                    str(stepPos)    + "," +
                    str(stepNeg)    + "," +
                    str(Vgate)      + "," +
                    str(rev)        + "," +
                    str(hslV)       + "," +
                    str(hslF)       + "," +
                    str(cycles)     + "," +
                    str(T)          + "," +
                    str(pw)         + "," +
                    str(limitI)     + "," +
                    str(rangeI)     + "," +
                    str(limitV)     + "," +
                    str(rangeV)     + "," +
                    str(nplc))

    commandStr = "list_iv_1T1R(" + paramsStr + ")" 
    
    # Vpos,Vneg,stepPos,stepNeg,rev,hslV,hslF,cycles,T,pw,limitI,limitV,nplc
    #commandStr = "list_iv(1,0.5,0.5,0.1,0,0.2,0,1,0.1,0.01,0.03,10,0.001)"
    smu.write(commandStr)

#def run():
def iv(smu,Vpos,Vneg,stepPos,stepNeg,rev,hslV,hslF,cycles,T,pw,limitI,rangeI,limitV,rangeV,nplc,gpibAdrress):
 
    import Keithley_K2612B.functions as functions
    from time import sleep
    functions.clear_all()
    [smu,rm]    = functions.gpib(gpibAdrress)
    smu.write('reset()')
    smu.write("errorqueue.clear()")
    functions.initBuffers(smu)
    [uu,complete_date,uu] = functions.date_time_now()
    print(str(complete_date))
    print("Start measuring...")
    IVlist(smu,Vpos,Vneg,stepPos,stepNeg,rev,hslV,hslF,cycles,T,pw,limitI,rangeI,limitV,rangeV,nplc)
    #IVlist(smu,top,step,rev,hslV,hslF,cycles,T,pw,limitI,limitV,nplc)
    if hslF == 1:
        m = 2
    else:
        m = 1
    pulses      = 2*(Vpos/stepPos) + 2*(Vneg/stepNeg)  
    testTime    = (T + pw)*pulses*m*cycles
    oneMinute   = testTime/60
    import datetime
    minutes     = datetime.timedelta(seconds=testTime)
    if oneMinute < 1:
        print("This will take.. less than a minute")
    else:
        print("This will take.. " + str(minutes))
    sleep(1)
    sleep(testTime)
    sleep(1)

    [uu,complete_date,uu] = functions.date_time_now()
    print("END measuring...")
    print(str(complete_date))
    
    sleep(1)
    
    [t, volt,curr] = functions.readBuffer(smu, 'b')
    
    return t, volt, curr

def stress(smu,V,N,cycles,T,pw,limitI,rangeI,limitV,rangeV,nplc,gpibAdrress):
 
    import Keithley_K2612B.functions as functions
    from time import sleep
    functions.clear_all()
    [smu,rm]    = functions.gpib(gpibAdrress)
    smu.write('reset()')
    smu.write("errorqueue.clear()")
    functions.initBuffers(smu)
    [uu,complete_date,uu] = functions.date_time_now()
    print(str(complete_date))
    print("Start measuring...")
    paramsStr =     (str(V)      + "," +
                    str(N)       + "," +
                    str(cycles)     + "," +
                    str(T)          + "," +
                    str(pw)         + "," +
                    str(limitI)     + "," +
                    str(rangeI)     + "," +
                    str(limitV)     + "," +
                    str(rangeV)     + "," +
                    str(nplc))

    commandStr = "stress(" + paramsStr + ")" 
    smu.write(commandStr)
    
    #IVlist(smu,top,step,rev,hslV,hslF,cycles,T,pw,limitI,limitV,nplc)
    pulses      = N  
    testTime    = (T + pw)*pulses*cycles
    oneMinute   = testTime/60
    import datetime
    minutes     = datetime.timedelta(seconds=testTime)
    if oneMinute < 1:
        print("This will take.. less than a minute")
    else:
        print("This will take.. " + str(minutes))
    sleep(1)
    sleep(testTime)
    sleep(1)

    [uu,complete_date,uu] = functions.date_time_now()
    print("END measuring...")
    print(str(complete_date))
    
    sleep(1)
    [t, volt, curr] = functions.readBuffer(smu, 'b')

    return t, volt, curr
    

def iv_1T1R():
    [Vpos,
     Vneg,
     stepPos,
     stepNeg,
     rev,
     hslV,
     hslF,
     cycles,
     T,
     pw,
     limitI,
     limitV,
     nplc,
     V1,
     V2,
     n_1,
     n_2,
     v_read,
     metaData,
     Vgate,
     rangeI,
     rangeV] = setup()
    
    import functions
    from time import sleep
    functions.clear_all()
    gpibAdrress = 26
    [smu,rm]    = functions.gpib(gpibAdrress)
    smu.write('reset()')
    smu.write("errorqueue.clear()")
    functions.initBuffers(smu)
    [uu,complete_date,uu] = functions.date_time_now()
    print(str(complete_date))
    print("Start measuring...")
    IVlist_1T1R(smu,Vpos,Vneg,stepPos,stepNeg,Vgate,rev,hslV,hslF,cycles,T,pw,limitI,rangeI,limitV,rangeV,nplc)
    #IVlist(smu,top,step,rev,hslV,hslF,cycles,T,pw,limitI,limitV,nplc)
    if hslF == 1:
        m = 2
    else:
        m = 1
    pulses      = 2*(Vpos/stepPos) + 2*(Vneg/stepNeg)  
    testTime    = T*pulses*m*cycles
    oneMinute   = testTime/60
    import datetime
    minutes     = datetime.timedelta(seconds=testTime)
    if oneMinute < 1:
        print("This will take.. less than a minute")
    else:
        print("This will take.. " + str(minutes))
    sleep(1)
    sleep(testTime)
    sleep(1)

    [uu,complete_date,uu] = functions.date_time_now()
    print("END measuring...")
    print(str(complete_date))
    
    sleep(1)
    
    import saver
    saver.saveME(smu,"a")


    

def pulse_run(smu,V1,V2,n_1,n_2,v_read,cycles,T,pw,limitI,rangeI,limitV,rangeV,nplc):
        
    """
    pulse_e(V1,V2,n_1,n_2,v_read,cycles,T,pw,limitI,limitV,nplc)
    """
    paramsStr =     (str(V1)        + "," +
                    str(V2)         + "," +
                    str(n_1)        + "," +
                    str(n_2)        + "," +
                    str(v_read)     + "," +
                    str(cycles)     + "," +
                    str(T)          + "," +
                    str(pw)         + "," +
                    str(limitI)     + "," +
                    str(rangeI)     + "," +
                    str(limitV)     + "," +
                    str(rangeV)     + "," +
                    str(nplc))

    commandStr = "pulse_e(" + paramsStr + ")" 
    
    smu.write(commandStr)


def pulse_run_1T1R(smu,V1,V2,n_1,n_2,v_read,Vgate,cycles,T,pw,limitI,rangeI,limitV,rangeV,nplc):
        
    """
    pulse_e(V1,V2,n_1,n_2,v_read,Vgate,cycles,T,pw,limitI,limitV,nplc)
    """
    paramsStr =     (str(V1)        + "," +
                    str(V2)         + "," +
                    str(n_1)        + "," +
                    str(n_2)        + "," +
                    str(v_read)     + "," +
                    str(Vgate)      + "," +
                    str(cycles)     + "," +
                    str(T)          + "," +
                    str(pw)         + "," +
                    str(limitI)     + "," +
                    str(rangeI)     + "," +
                    str(limitV)     + "," +
                    str(rangeV)     + "," +
                    str(nplc))

    commandStr = "pulse_1T1R(" + paramsStr + ")" 
    
    smu.write(commandStr)



def pulses():

    [Vpos,
     Vneg,
     stepPos,
     stepNeg,
     rev,
     hslV,
     hslF,
     cycles,
     T,
     pw,
     limitI,
     limitV,
     nplc,
     V1,
     V2,
     n_1,
     n_2,
     v_read,
     metaData,
     Vgate,
     rangeI,
     rangeV] = setup()

    
    import functions
    from time import sleep
    functions.clear_all()
    gpibAdrress = 26
    [smu,rm]    = functions.gpib(gpibAdrress)
    smu.write('reset()')
    smu.write("errorqueue.clear()")
    functions.initBuffers(smu)
    [uu,complete_date,uu] = functions.date_time_now()
    print(str(complete_date))
    print("Start measuring...")
    pulse_run(smu,V1,V2,n_1,n_2,v_read,cycles,T,pw,limitI,rangeI,limitV,rangeV,nplc)
    testTime    = (n_1 + n_2 + 2)*cycles*T
    oneMinute   = testTime/60
    import datetime
    minutes     = datetime.timedelta(seconds=testTime)
    if oneMinute < 1:
        print("This will take.. less than a minute")
    else:
        print("This will take.. " + str(minutes))


    sleep(5)
    sleep(testTime*1.1)
    sleep(1)
#
    [uu,complete_date,uu] = functions.date_time_now()
    print("END measuring...")
    print(str(complete_date))
#    
    sleep(1)
#    
    import saver
    saver.saveME(smu,"a")
   

#    smu.write("statusByte = status.condition")
#    statusByte = smu.query("print(statusByte)")
#    statusByte = bin(int(statusByte.split('.')[0]))



def pulses_1T1R():

    [Vpos,
     Vneg,
     stepPos,
     stepNeg,
     rev,
     hslV,
     hslF,
     cycles,
     T,
     pw,
     limitI,
     limitV,
     nplc,
     V1,
     V2,
     n_1,
     n_2,
     v_read,
     metaData,
     Vgate,
     rangeI,
     rangeV] = setup()

    
    import functions
    from time import sleep
    functions.clear_all()
    gpibAdrress = 26
    [smu,rm]    = functions.gpib(gpibAdrress)
    smu.write('reset()')
    smu.write("errorqueue.clear()")
    functions.initBuffers(smu)
    [uu,complete_date,uu] = functions.date_time_now()
    print(str(complete_date))
    print("Start measuring...")
    pulse_run_1T1R(smu,V1,V2,n_1,n_2,v_read,Vgate,cycles,T,pw,limitI,rangeI,limitV,rangeV,nplc)
    testTime    = (n_1 + n_2 + 2)*cycles*T
    oneMinute   = testTime/60
    import datetime
    minutes     = datetime.timedelta(seconds=testTime)
    if oneMinute < 1:
        print("This will take.. less than a minute")
    else:
        print("This will take.. " + str(minutes))


    sleep(5)
    sleep(testTime)
    sleep(1)
#
    [uu,complete_date,uu] = functions.date_time_now()
    print("END measuring...")
    print(str(complete_date))
#    
    sleep(1)
#    
    import saver
    saver.saveME(smu,"a")


