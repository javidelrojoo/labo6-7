function pulse_e(V1,V2,n1,n2,v_read,cycles,T,pw,limitI,rangeI,limitV,rangeV,nplc)
	
	--pulse_e(V1,V2,n1,n2,v_read,cycles,T,pw,limitI,limitV,nplc)
	
	reset()
	smua.reset()
	
	smua.nvbuffer1.clear()
	smua.nvbuffer1.collecttimestamps = 1
	smua.nvbuffer2.clear()
	smua.nvbuffer2.collecttimestamps = 1
	
	format.data = format.ASCII
	format.asciiprecision = 6
	
	-- parameters
    armCount	= cycles	-- 3		-- cycles
	pulsePeriod = T 		-- 100E-03 	-- T
	pulseWidth 	= pw		-- 10E-03	-- pw
	
    k			= 0
	-- pulse generator
	a			= {}
	len 		= n1 + n2 + 1
	len1 		= n1 + 1

    count 		= len + 2
	numPoints 	= count
		
	for i=0,n1,1 do 
		a[i] = V1
	end

	a[len1] = v_read 

	for i=len1+1,len,1 do 
		a[i] = V2
	end

	a[len + 1] = v_read 
    a[len + 2] = 0
    
	-- gsanca 31/07/18
	smua.source.autorangei			= smua.AUTORANGE_ON
	--smua.source.autorangei			= smua.AUTORANGE_OFF
	--smua.source.rangei				= limitI 
	---
	
	-- gsanca 01/08/2018
	smua.source.limiti				= limitI
	
	smua.source.leveli				= 0
	-- Set the DC bias limit.  This is not the limit used during the pulses.
	smua.source.limitv				= 5

	-- Disabling Auto-Ranging and Auto-Zero ensures accurate and consistent timing
	-- gsanca 31/07/18
	smua.measure.autozero			= smua.AUTOZERO_AUTO
	--smua.measure.autozero			= smua.AUTOZERO_ONCE
	smua.measure.autorangev			= smua.AUTORANGE_OFF
	smua.measure.rangev				= math.max(math.abs(V1), math.abs(V2))
	-- gsanca 03/02/2020
	smua.measure.rangei				= rangeI
	
	smua.measure.nplc				= nplc
	-- A timer will be used to control the measure delay so set the built-in delay to 0
	smua.measure.delay				= 0
	-- gsanca 31/07/18
	smua.measure.autorangei 		= 1

	-- Prepare the Reading Buffers
	smua.nvbuffer1.clear()
	smua.nvbuffer1.collecttimestamps= 1
	smua.nvbuffer2.clear()
	smua.nvbuffer2.collecttimestamps= 1

	-- Configure the Trigger Model
	--============================
	-- Pressing the TRIG button on the front panel will trigger the sweep to start
	display.trigger.clear()
    
    	-- Timer 1 controls the pulse period
	trigger.timer[1].count			= numPoints > 1 and numPoints - 1 or 1
	trigger.timer[1].delay			= pulsePeriod
	trigger.timer[1].passthrough	= true
	trigger.timer[1].stimulus		= smua.trigger.ARMED_EVENT_ID

	-- Timer 2 controls the measure delay
	trigger.timer[2].count			= 1
	-- Set the measure delay long enough so that measurements start after the pulse
	-- has settled, but short enough that it fits within the width of the pulse.
	trigger.timer[2].delay			= pulseWidth - (1/localnode.linefreq)*nplc - 60e-6
	trigger.timer[2].passthrough	= false
	trigger.timer[2].stimulus		= trigger.timer[1].EVENT_ID

	-- Timer 3 controls the pulse width
	trigger.timer[3].count			= 1
	trigger.timer[3].delay			= pulseWidth
	trigger.timer[3].passthrough	= false
	trigger.timer[3].stimulus		= trigger.timer[1].EVENT_ID
    
    
	-- Configure SMU Trigger Model for Sweep
	--smua.trigger.source.lineari(start, stop, numPoints)
    smua.trigger.source.listv(a)
	smua.trigger.source.limitv		= limitV
	smua.trigger.source.limiti		= limitI
	smua.trigger.measure.action		= smua.ENABLE
	smua.trigger.measure.iv(smua.nvbuffer1, smua.nvbuffer2)
	smua.trigger.endpulse.action	= smua.SOURCE_IDLE
	smua.trigger.endsweep.action	= smua.SOURCE_IDLE
	smua.trigger.count				= count
	smua.trigger.arm.count 			= armCount
	smua.trigger.arm.stimulus		= 0
	smua.trigger.source.stimulus	= trigger.timer[1].EVENT_ID
	smua.trigger.measure.stimulus	= trigger.timer[2].EVENT_ID
	smua.trigger.endpulse.stimulus	= trigger.timer[3].EVENT_ID
	smua.trigger.source.action		= smua.ENABLE
	--==============================
	-- End Trigger Model Configuration
	
	smua.source.output				= smua.OUTPUT_ON

	-- Start the trigger model execution
	smua.trigger.initiate()
	-- Sweep will not start until the TRIG button is pressed

	-- Wait until the sweep has completed
	waitcomplete()
	smua.source.output				= smua.OUTPUT_OFF
end