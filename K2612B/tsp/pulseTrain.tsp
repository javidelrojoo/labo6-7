function pulseTrainV(V,rangeV,pw,T,n)
	-- Voltage pulses (without measuring)
	-- Generate a 10-point pulse train where each pulse has a width of 600
	-- microseconds and a pulse period of 5 milliseconds.
	-- Alias the trigger timers to use for pulse width and period.
	period_timer 					= trigger.timer[1]
	pulse_timer 					= trigger.timer[2]
	-- Create a fixed level voltage sweep.
	smua.trigger.source.listv({V})
	smua.trigger.source.action 		= smua.ENABLE
	smua.source.rangev = rangeV
	smua.trigger.measure.action 	= smua.DISABLE
	-- Set pulse width.
	pulse_timer.delay 				= pw--0.0006
	-- Trigger pulse width timer with period timer.
	pulse_timer.stimulus 			= period_timer.EVENT_ID
	-- Output one pulse per period.
	pulse_timer.count 				= 1
	-- Set the pulse period.
	period_timer.delay 				= T--0.005
	-- Set pulse period count to generate 10 pulses.
	period_timer.count 				= n-1
	-- Trigger pulse period timer when a sweep is initiated.
	period_timer.stimulus 			= smua.trigger.SWEEPING_EVENT_ID
	-- Configure the timer to output a trigger event when it
	-- starts the first delay.
	period_timer.passthrough 		= true
	-- Trigger SMU source action using pulse period timer
	smua.trigger.source.stimulus 	= period_timer.EVENT_ID
	-- Trigger SMU end pulse action using pulse width timer.
	smua.trigger.endpulse.action 	= smua.SOURCE_IDLE
	smua.trigger.endpulse.stimulus 	= pulse_timer.EVENT_ID
	-- Set Trigger Model counts.
	smua.trigger.count 				= 1
	-- Configure the SMU to execute a 10-point pulse train.
	smua.trigger.arm.count 			= n
	-- Prepare SMU to output pulse train.
	smua.source.output 				= smua.OUTPUT_ON
	smua.trigger.initiate()
	-- Wait for the sweep to complete.
	waitcomplete()
	smua.source.output 				= smua.OUTPUT_OFF
end