# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 17:40:11 2018

@author: gsanca
"""

import functions
import time
#from setup import setup
import runner


def IVlist(smu):
        
    [top,
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
    metaData] = runner.setup()
    
    """
    list(Vpos,Vneg,stepPos,stepNeg,rev,hslV,hslF,cycles,T,pw,limitI,limitV,nplc)
    
    old:
    list(max,step,rev,hslV,hslF,cycles,T,pw,limitI,limitV,nplc)
    """
    
    
    Vpos 	= 3
    Vneg	   = 1
    stepPos	= 0.5
    stepNeg	= 0.1
    rev		= 1
    hslV	   = 0.1
    hslF	   = 0
    cycles	= 1
    T		   = 0.1
    pw		= 0.01
    limitI	= 0.01
    limitV	= 5
    nplc	   = 0.001
    
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
                    str(limitV)     + "," +
                    str(nplc))
    
#    paramsStr =     (str(top)   + "," +
#                    str(step)   + "," +
#                    str(rev)    + "," +
#                    str(hslV)   + "," +
#                    str(hslF)   + "," +
#                    str(cycles) + "," +
#                    str(T)      + "," +
#                    str(pw)     + "," +
#                    str(limitI) + "," +
#                    str(limitV) + "," +
#                    str(nplc))

    commandStr = "list(" + paramsStr + ")" 
    smu.write(commandStr)
    
#    pulses      = 4*(top/step) 
#    testTime    = T*pulses*cycles
#    
#    time.sleep(1)
#    time.sleep(testTime)
    
def readIV(smu):
    
    [t,volt,curr] = functions.readBuffer(smu, 'b')
    print(t, volt, curr)
    times       = caster(t)
    readingsI   = caster(curr)
    readingsV   = caster(volt)
    calculatedR = []
    if len(readingsV) == len(readingsI):
        i = 0
        for voltage in readingsV:
            calculatedR.append(voltage/readingsI[i])
            i = i + 1
            
    return times, readingsV, readingsI, calculatedR
            
def caster(string):
    out = []
    for values in string.split(','):
        aux = values
        out.append(float(aux))
    return out


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------    
def rutina1(smu):    
    ###########################################################################
    # Rutina
    ###########################################################################
    functions.configSMU_A(smu)

    smu.write('smua.nvbuffer1.clear()')
    smu.write('smua.nvbuffer2.clear()')
    
    smu.write('smua.measure.count = 10')
    smu.write('smua.measure.v(smua.nvbuffer1)')

    
    smu.write('smua.source.output = smua.OUTPUT_OFF')

#------------------------------------------------------------------------------
def rutina2(smu):
    """
    smuX.measureYandstep()
    """
    smu.write('local ivalues = {}')
    smu.write('smua.source.rangev = 1')
    smu.write('smua.source.levelv = 0')
    smu.write('smua.measure.rangei = 0.01')
    smu.write('smua.source.output = smua.OUTPUT_ON')
    smu.write('for index = 1, 10 do\n ivalues[index] = smua.measureiandstep(index / 10)\nend')
    #smu.write('ivalues[11] = smua.measure.i()')

#------------------------------------------------------------------------------
def readingBufferExample(smu):
    
    smu.write('smua.reset()')
    smu.write("smua.nvbuffer1.clear()")
    smu.write("smua.nvbuffer2.clear()")
    smu.write("smua.nvbuffer1.clear()")
    smu.write("smua.nvbuffer2.clear()")
    time.sleep(0.5)

    smu.write('smua.reset()')
    smu.write('display.screen = display.SMUA')
    smu.write('display.smua.measure.func = display.MEASURE_DCAMPS')
    smu.write('smua.measure.autorangei = smua.AUTORANGE_ON')
    smu.write('format.data = format.ASCII')
    smu.write('smua.nvbuffer1.clear()')
    smu.write('smua.nvbuffer1.appendmode = 1')
    smu.write('smua.nvbuffer1.collectsourcevalues = 1')
    smu.write('smua.measure.count = 1')
    smu.write('smua.source.func = smua.OUTPUT_DCVOLTS')
    smu.write('smua.source.levelv = 0.0')
    smu.write('smua.source.output = smua.OUTPUT_ON')
    forStr = 'for v = 1, 10 do smua.source.levelv = v * 0.1 smua.measure.i(smua.nvbuffer1) end'
    smu.write(forStr)
    smu.write('smua.source.output = smua.OUTPUT_OFF')
    
    read = smu.query('printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)')
    sour = smu.query('printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.sourcevalues)')
    x = functions.caster(read)
    y = functions.caster(sour)
    
    return x, y

#------------------------------------------------------------------------------
def dualBufferExample(smu):
#    -- Restore Series 2600B defaults.
    smu.write('smua.reset()')
    smu.write("smua.nvbuffer1.clear()")
    smu.write("smua.nvbuffer2.clear()")
#    -- Select measure I autorange.1
    smu.write('smua.measure.autorangei = smua.AUTORANGE_ON')
#    -- Select measure V autorange.
    smu.write('smua.measure.autorangev = smua.AUTORANGE_ON')
#    -- Select ASCII data format.
    smu.write('format.data = format.ASCII')
#    -- Clear buffer 1.
    smu.write('smua.nvbuffer1.clear()')
#    -- Clear buffer 2.
    smu.write('smua.nvbuffer2.clear()')
#    -- Set buffer count to 100.
    count = 100
    smu.write('smua.measure.count = ' + str(count))
#    -- Set measure interval to 0.1 s.
    interval = 0.1
    smu.write('smua.measure.interval = ' + str(interval))
#    -- Select source voltage function.
    smu.write('smua.source.func = smua.OUTPUT_DCVOLTS')
#    -- Output 1 V.
    smu.write('smua.source.levelv = 1')
#    -- Turn on output.
    smu.write('smua.source.output = smua.OUTPUT_ON')
#    -- Store current readings in buffer 1, voltage readings in buffer 2.
    smu.write('smua.measure.overlappediv(smua.nvbuffer1, smua.nvbuffer2)')
#    -- Wait for buffer to fill.
    smu.write('waitcomplete()')
    waitTime = count * interval  + 2
    time.sleep(waitTime)
#    -- Turn off output.
    smu.write('smua.source.output = smua.OUTPUT_OFF')
#    -- Output buffer 1 readings 1 to 100.
    curr = smu.query('printbuffer(1, 100, smua.nvbuffer1)')
#    -- Output buffer 2 readings 1 to 100.
    volt = smu.query('printbuffer(1, 100, smua.nvbuffer2)')
    
    #x = caster(volt)
    #y = caster(curr)
    
    smu.write('smua.reset()')
    return volt,curr

#------------------------------------------------------------------------------
def rutinaLabView(smu):    
    ###########################################################################
    # Rutina
    ###########################################################################
    configSMU_A(smu)
    
    
    smu.write('smua.nvbuffer1.clear()')
    smu.write('smua.nvbuffer2.clear()')
    
    #smu.write('smua.source.limiti = 0.1')
    
    
    smu.write('smua.measure.nplc  = 0.01')
    smu.write('smua.source.levelv = 2') 
    smu.write('delay(0.01)') 
    """
    smuX.measure.Y()
    """
    smu.write('smua.measure.i(smua.nvbuffer1)') 
    smu.write('waitcomplete()')
    smu.write('smua.source.levelv=0') 
    smu.write('delay(0.01)') 
    #smu.write('smua.source.limiti = 0.01')
    
    # Level... se genera con la rampa???
    smu.write('smua.source.levelv=2')
    smu.write('smua.measure.i(smua.nvbuffer2)')
    smu.write('waitcomplete()')
    smu.write('smua.source.levelv=0')
    #smu.write('errorqueue.clear()')
    # Hasta aca el primer write, sin ningun read
    
    
    # aca vienen los writes mas read

    auxRead = smu.query('print(smua.nvbuffer1.n)')
    print('primera')
    print(auxRead)
    """
#    printbuffer(startIndex, endIndex, bufferVar)
    """
    auxRead = smu.query('printbuffer(1, 1, smua.nvbuffer1.sourcevalues)') 
    print('segunda')
    print(auxRead)
    
    auxRead = smu.query('printbuffer(1, 1, smua.nvbuffer1.readings)') 
    print('tercera')
    print(auxRead)
    
    auxRead = smu.query('printbuffer(1, 1, smua.nvbuffer2.readings)') 
    print('cuarta')
    print(auxRead)
 
    #smu.write('smua.nvbuffer1.clear()\nsmua.nvbu ffer2.clear()\n\nsmua.source.limiti = 1')
        
    
    smu.write('smua.source.output = smua.OUTPUT_OFF')
    
    
#    auxRead = 'buuu'
#    return auxRead


    #smua.nvbuffer1.clear()
    #smua.nvbuffer2.clear()
    #smua.source.limiti = %g
    #smua.measure.nplc = %g
    #smua.source.levelv=%g
    #delay(%ge-3)
    #smua.measure.i(smua.nvbuffer1)
    #waitcomplete()
    #smua.source.levelv=0
    #delay(%ge-3)
    #smua.source.limiti = %g
    #smua.source.levelv=%g
    #smua.measure.i(smua.nvbuffer2)
    #waitcomplete()
    #smua.source.levelv=0

#------------------------------------------------------------------------------
def AC_Waveform_Sweep(smu):
    import numpy as np
    """
    function AC_Waveform_Sweep(Vrms, numCycles, frequency, limitI)
    """
    Vrms        = 12
    numCycles   =  2
    freq        = 60
    limitI      = 100e-3

    pointsPerCycle = 7200/freq
    numDataPoints  = pointsPerCycle * numCycles

    smu.write('reset()')
    """
    -- Generate the source values
    """
    Vpp = Vrms * np.sqrt(2)
    smu.write('local Vpp				= ' + str(Vpp))
    smu.write('local sourceValues	= {}')
    smu.write('local pointsPerCycle = ' + str(pointsPerCycle))
    smu.write('local numDataPoints	= ' + str(numDataPoints))
    forStr = 'for i=1, ' + str(numDataPoints) + ' do sourceValues[i]	= ( ' + str(Vpp) + ' * math.sin(i * 2 * math.pi / pointsPerCycle)) end'
    smu.write(forStr)
    """
    -- Configure the SMU ranges
    """
    smu.write('smua.reset()')
    smu.write('smua.source.settling		   = smua.SETTLE_FAST_POLARITY')
    smu.write('smua.source.autorangev		= smua.AUTORANGE_OFF')
    smu.write('smua.source.autorangei		= smua.AUTORANGE_OFF')
    smu.write('smua.source.rangev			= ' + str(Vpp))
    smu.write('smua.source.limiti			= ' + str(limitI))

    smu.write('smua.measure.autorangev		= smua.AUTORANGE_OFF')
    smu.write('smua.measure.autorangei		= smua.AUTORANGE_OFF')
    smu.write('smua.measure.autozero		= smua.AUTOZERO_OFF')
    """
    -- Voltage will be measured on the same range as the source range
    """
    smu.write('smua.measure.rangei			= ' + str(limitI))
    smu.write('smua.measure.nplc          = 0.001')
    """        
    -- Prepare the Reading Buffers
    """
    smu.write('smua.nvbuffer1.clear()')
    smu.write('smua.nvbuffer1.collecttimestamps	= 1')
    smu.write('smua.nvbuffer2.clear()')
    smu.write('smua.nvbuffer2.collecttimestamps	= 1')

    """
    -- Configure the trigger model
    -- ============================
    
    -- Timer 1 controls the time between source points
    """ 
    smu.write('trigger.timer[1].delay = (1 / 7200)')
    smu.write('trigger.timer[1].passthrough = true')
    smu.write('trigger.timer[1].stimulus = smua.trigger.ARMED_EVENT_ID')
    smu.write('trigger.timer[1].count = numDataPoints - 1')

#    -- Configure the SMU trigger model
    smu.write('smua.trigger.source.listv(sourceValues)')
    smu.write('smua.trigger.source.limiti		= ' + str(limitI))
    smu.write('smua.trigger.measure.action	= smua.ENABLE')
    smu.write('smua.trigger.measure.iv(smua.nvbuffer1, smua.nvbuffer2)')
    smu.write('smua.trigger.endpulse.action	= smua.SOURCE_HOLD')
    smu.write('smua.trigger.endsweep.action	= smua.SOURCE_IDLE')
    smu.write('smua.trigger.count				= numDataPoints')
    smu.write('smua.trigger.arm.stimulus		= 0')
    smu.write('smua.trigger.source.stimulus	= trigger.timer[1].EVENT_ID')
    smu.write('smua.trigger.measure.stimulus	= 0')
    smu.write('smua.trigger.endpulse.stimulus= 0')
    smu.write('smua.trigger.source.action		= smua.ENABLE')
#    -- Ready to begin the test

    smu.write('smua.source.output				= smua.OUTPUT_ON')
#    -- Start the trigger model execution
    smu.write('smua.trigger.initiate()')
#    -- Wait until the sweep has completed
    smu.write(' waitcomplete()')
    smu.write('smua.source.output				= smua.OUTPUT_OFF')

#    -- Print the data back to the Console in tabular format
    smu.write('print("Time\tVoltage\tCurrent")')
#    -- Voltage readings are in nvbuffer2.  Current readings are in nvbuffer1.
    smu.write('for x=1,smua.nvbuffer1.n do print(smua.nvbuffer1.timestamps[x], smua.nvbuffer2[x], smua.nvbuffer1[x]) end')


#------------------------------------------------------------------------------
def scriptTest(smu):
    smu.write('reset()')
    smu.write('loadscript scriptTest')
    smu.write('function displayTest()')
    smu.write('display.clear()')
    smu.write('display.setcursor(1, 1)')
    smu.write('display.settext("Press EXIT to Abort")')
    smu.write('display.setcursor(2, 1)')
    smu.write('display.settext("or any key to continue")')
    smu.write('end')
    smu.write('endscript')


#------------------------------------------------------------------------------
def measScript(smu):
    smu.write('reset()')
    
    smu.write('loadscript theFuckingTest')
    
    smu.write('function measNow()')
    smu.write('display.clear()')
    smu.write('display.setcursor(1, 1)')
    smu.write('display.settext("Se viene el script")')
    smu.write('display.setcursor(2, 1)')
    smu.write('display.settext("MMLPQTP")')    
    smu.write('smua.reset()')
    smu.write('display.screen = display.SMUA')
    smu.write('display.smua.measure.func = display.MEASURE_DCAMPS')
    smu.write('smua.measure.autorangei = smua.AUTORANGE_ON')
    smu.write('format.data = format.ASCII')
    smu.write('smua.nvbuffer1.clear()')
    smu.write('smua.nvbuffer1.appendmode = 1')
    smu.write('smua.nvbuffer1.collectsourcevalues = 1')
    smu.write('smua.measure.count = 1')
    smu.write('smua.source.func = smua.OUTPUT_DCVOLTS')
    smu.write('smua.source.levelv = 0.0')
    smu.write('smua.source.output = smua.OUTPUT_ON')
    smu.write('for v = 1, 100 do smua.source.levelv = v * 0.01 smua.measure.i(smua.nvbuffer1) end')
    smu.write('smua.source.output = smua.OUTPUT_OFF')
    smu.write('end')   

    smu.write('function readNVbbuffer1()')
    smu.write('printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)')
    smu.write('end')   

    smu.write('function readNVbbuffer2()')
    smu.write('printbuffer(1, smua.nvbuffer2.n, smua.nvbuffer2.readings)')
    smu.write('end') 
    
    smu.write('endscript')
    
#------------------------------------------------------------------------------
def clearSMU(smu,which):
    smuStr = 'smu' + which 
    smu.write(smuStr + '.nvbuffer1.clear()')
    smu.write(smuStr + '.nvbuffer2.clear()')
    smu.write(smuStr + '.reset()') 
    smu.write(smuStr + '.source.output = smua.OUTPUT_OFF')
    
"""
smua.reset() 
errorqueue.clear()
smua.source.func = smua.OUTPUT_DCVOLTS
smua.source.autorangev = smua.AUTORANGE_ON
smua.measure.autorangei = smua.AUTORANGE_ON
format.data = format.ASCII 
smua.nvbuffer1.clear() 
smua.nvbuffer1.appendmode = 1 
smua.nvbuffer1.collectsourcevalues = 1
smua.nvbuffer2.clear() 
smua.nvbuffer2.appendmode = 1 
smua.nvbuffer2.collectsourcevalues = 1 
smua.measure.count = 1 
smua.source.output =smua.OUTPUT_ON 


smua.nvbuffer1.clear()
smua.nvbuffer2.clear()

smua.source.limiti = %g
smua.measure.nplc = %g
smua.source.levelv=%g 
delay(%ge-3) 
smua.measure.i(smua.nvbuffer1) 
waitcomplete()
smua.source.levelv=0 
delay(%ge-3) 
smua.source.limiti = %g
smua.source.levelv=%g
smua.measure.i(smua.nvbuffer2) 
waitcomplete()
smua.source.levelv=0
errorqueue.clear()


smua.nvbuffer1.clear()\nsmua.nvbuffer2.clear()\n\nsmua.source.limiti = 


smua.source.output = smua.OUTPUT_OFF
"""