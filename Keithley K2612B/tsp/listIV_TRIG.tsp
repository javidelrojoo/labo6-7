function listTRIG(max,step,rev,hslV,hslF,cycles,T,pw,limitI,limitV,nplc)
	-- parameters
	min			= 0			
	reverse		= rev 		-- 1
    hslValue	= hslV		-- 0.5		-- hslV
    hslFlag		= hslF		-- 1		-- hslF
    armCount	= cycles	-- 3		-- cycles
	pulsePeriod = T 		-- 100E-03 	-- T
	pulseWidth 	= pw		-- 10E-03	-- pw
	nplc 		= nplc		-- 0.001	-- nplc
	limitI		= limitI 	-- 0.1		-- limitI
	limitV 		= limitV  	-- 5		-- limitV
	
    -- reverse mode condition
    if reverse == 1 then
    	p = 1
    	n = -1
	else
		p = -1
		n = 1
	end
	
	-- ramp generator
    k		= 0
	a		= {}
	iterMax	= 2*(2.0*(max - min)/step)
	
	for j = 0, 1, 1 do
		for i = 0, iterMax/2, 1 do
			if (max-min)/step >= i then
				vValue = i*step + min
			else
				vValue = 2*max - min - i*step
			end
			if j == 0 then
				a[k] = n*vValue
			else
				a[k] = p*vValue 
			end
			k = k + 1
		end
	end
    
    -- HSL mode configuration
    if hslFlag == 1 then
    	count 	= 2*iterMax + 1
    	a 		= hslAdd(a,iterMax,hslValue)
	else
    	count = iterMax
	end
	
	numPoints 	= count
    
	smua.source.autorangei			= smua.AUTORANGE_OFF
	smua.source.rangei				= limitI 
	smua.source.leveli				= 0
	-- Set the DC bias limit.  This is not the limit used during the pulses.
	smua.source.limitv				= 5

	-- Disabling Auto-Ranging and Auto-Zero ensures accurate and consistent timing
	smua.measure.autozero			= smua.AUTOZERO_ONCE
	smua.measure.autorangev			= smua.AUTORANGE_OFF
	smua.measure.rangev				= math.max(math.abs(max), math.abs(min))
	smua.measure.nplc				= nplc
	-- A timer will be used to control the measure delay so set the built-in delay to 0
	smua.measure.delay				= 0

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
	trigger.timer[1].stimulus		= display.trigger.EVENT_ID

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