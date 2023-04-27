function TR_list()
	-- Vpos,Vneg,stepPos,stepNeg,rev,hslV,hslF,cycles,T,pw,limitI,limitV,nplc,start_b,stop_b,count_b
	
	Vpos = 3
	Vneg = 1
	stepPos = 0.5
	stepNeg = 0.1
	rev = 0
	hslV = 0.1
	hslF = 0
	cycles = 1
	T = 0.5
	pw = 0.1
	limitI = 0.01
	limitV = 5
	nplc = 0.01
	start_b = 0
	stop_b = 4
	count_b = 1
	
	
	-- parameters		
	reverse		= rev 		-- 1
    hslValue	= hslV		-- 0.5		-- hslV
    hslFlag		= hslF		-- 1		-- hslF
    armCount	= cycles	-- 3		-- cycles
	pulsePeriod = T 		-- 100E-03 	-- T
	pulseWidth 	= pw		-- 10E-03	-- pw
	
	-- ramp generator a 
	a 			= {}
	a 			= ramp_gen(Vpos, Vneg, stepPos, stepNeg, reverse)
	iterMaxPos	= (2.0*Vpos/stepPos)
	iterMaxNeg	= (2.0*Vneg/stepNeg)

    -- HSL mode configuration
    if hslFlag == 1 then
    	count 	= 2*(iterMaxPos + iterMaxNeg) 
    	a 		= hslAdd(a,count,hslValue)
	else
    	count = iterMaxPos + iterMaxNeg 
	end
	numPoints 	= count
  
   	-- smu b
   	k 		= 0
   	b 		= {}
   	
   	if count_b == 1 then
   		for i = 0, count, 1 do
  			b[i] = stop_b
		end
   	else
   		step_b  = (stop_b - start_b)/(count_b - 1)
		for j = 0, count_b, 1 do
  			for i = 0, count, 1 do
  				b[k] = step_b * j + start_b
  				k 	 = k + 1
			end
    	end
   	end
   	

	-- gsanca 31/07/18
	smua.source.autorangei			= smua.AUTORANGE_ON
	-- gsanca 01/08/2018
	smua.source.limiti				= limitI
	smua.source.leveli				= 0
	-- Set the DC bias limit.  This is not the limit used during the pulses.
	smua.source.limitv				= 5

	-- Disabling Auto-Ranging and Auto-Zero ensures accurate and consistent timing
	-- gsanca 31/07/18
	smua.measure.autozero			= smua.AUTOZERO_AUTO
	smua.measure.autorangev			= smua.AUTORANGE_OFF
	smua.measure.rangev				= math.max(math.abs(Vpos), math.abs(Vneg))
	smua.measure.nplc				= nplc
	-- A timer will be used to control the measure delay so set the built-in delay to 0
	smua.measure.delay				= 0
	-- gsanca 31/07/18
	smua.measure.autorangei 		= 1

	-- Prepare the Reading Buffers
	-- smua.buffers
	smua.nvbuffer1.clear()
	smua.nvbuffer1.collecttimestamps= 1
	smua.nvbuffer2.clear()
	smua.nvbuffer2.collecttimestamps= 1
	
	-- smub.buffers
	smub.nvbuffer1.clear()
	smub.nvbuffer1.collecttimestamps= 1
	smub.nvbuffer2.clear()
	smub.nvbuffer2.collecttimestamps= 1
	
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
    
    --count_b = 1
	-- Configure SMU Trigger Model for Sweep (A)
    smua.trigger.source.listv(a)
	smua.trigger.source.limitv		= limitV
	smua.trigger.source.limiti		= limitI
	smua.trigger.measure.action		= smua.ENABLE
	smua.trigger.measure.iv(smua.nvbuffer1, smua.nvbuffer2)
	smua.trigger.endpulse.action	= smua.SOURCE_IDLE
	smua.trigger.endsweep.action	= smua.SOURCE_IDLE
	smua.trigger.count				= count
	smua.trigger.arm.count 			= count_b --armCount
	smua.trigger.arm.stimulus		= 0
	smua.trigger.source.stimulus	= trigger.timer[1].EVENT_ID
	smua.trigger.measure.stimulus	= trigger.timer[2].EVENT_ID
	smua.trigger.endpulse.stimulus	= trigger.timer[3].EVENT_ID
	smua.trigger.source.action		= smua.ENABLE
	--==============================

	-- Configure SMU Trigger Model for Sweep (B)
    smub.trigger.source.listv(b)
	smub.trigger.source.limitv		= limitV
	smub.trigger.source.limiti		= limitI
	smub.trigger.measure.action		= smub.ENABLE
	smub.trigger.measure.iv(smub.nvbuffer1, smub.nvbuffer2)
	smub.trigger.endsweep.action	= smub.SOURCE_IDLE
--	smub.trigger.count				= count_b
--	smub.trigger.arm.count 			= 1
--	smub.trigger.arm.stimulus		= 0
--	smub.trigger.source.stimulus	= trigger.timer[1].EVENT_ID
--	smub.trigger.measure.stimulus	= trigger.timer[2].EVENT_ID--smua.trigger.SWEEP_COMPLETE_EVENT_ID
--	smub.trigger.endpulse.stimulus	= smua.trigger.SWEEP_COMPLETE_EVENT_ID--trigger.timer[3].EVENT_ID
--	smub.trigger.source.action		= smub.ENABLE
	smub.trigger.count				= count
	smub.trigger.arm.count 			= cont_b
	smub.trigger.arm.stimulus		= 0
	smub.trigger.source.stimulus	= trigger.timer[1].EVENT_ID
	smub.trigger.measure.stimulus	= trigger.timer[2].EVENT_ID
	smub.trigger.endpulse.stimulus	= trigger.timer[3].EVENT_ID
	smub.trigger.source.action		= smub.ENABLE
	--==============================
	-- End Trigger Model Configuration
	
	smua.source.output				= smua.OUTPUT_ON
	smub.source.output				= smua.OUTPUT_ON

	-- Start the trigger model execution
	smub.trigger.initiate()
	smua.trigger.initiate()

	-- Wait until the sweep has completed
	waitcomplete()
	smua.source.output				= smua.OUTPUT_OFF
	smub.source.output				= smua.OUTPUT_OFF
end
