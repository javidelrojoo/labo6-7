function init_buffers(whichsmu)
	whichsmu.nvbuffer1.clear() 
	whichsmu.nvbuffer2.clear() 
	whichsmu.nvbuffer1.appendmode          = 1 --enable appending to nvbuffer1
	whichsmu.nvbuffer2.appendmode          = 1 --enable appending to nvbuffer2
	whichsmu.nvbuffer1.collectsourcevalues = 1 --enable source values to be collected to nvbuffer1 
	whichsmu.nvbuffer2.collectsourcevalues = 1 --enable source values to be collected to nvbuffer2
	whichsmu.nvbuffer1.collecttimestamps   = 1 --enable time stamps to be collected to nvbuffer1		
	whichsmu.nvbuffer2.collecttimestamps   = 1 --enable time stamps to be collected to nvbuffer2
end

function welcome()
    display.clear()
    display.setcursor(1, 1)
    display.settext("LINE.ECyT")
    display.setcursor(2, 1)
    display.settext("Press EXIT to continue")
end

function hslAdd(a,n,value)
	aux = {}
	for i=0,n,1 do 
		aux[2*i]	= a[i]
		aux[2*i+1]	= value
	end
	return aux
end

function ramp_gen(Vpos, Vneg, stepPos, stepNeg, reverse)
	ramp 		= {}
	k 	 		= 0
	vValue 		= 0
	iterMaxPos	= (2.0*Vpos/stepPos)
	iterMaxNeg	= (2.0*Vneg/stepNeg)
	
    -- reverse mode condition
    if reverse == 0 then
		-- positive ramp
		for i = 0, iterMaxPos, 1 do
			if i < (iterMaxPos/2)  then
				vValue = i*stepPos
			else
				vValue = Vpos - (i - iterMaxPos/2)*stepPos
			end
			ramp[k] = vValue
			k    	= k + 1
		end
	
	
		-- negative ramp
		for i = 0, iterMaxNeg, 1 do
			if i < (iterMaxNeg/2)  then
				vValue = i*stepNeg
			else
				vValue = Vneg - (i - iterMaxNeg/2)*stepNeg
			end
			ramp[k] = (-1)*vValue
			k   	= k + 1
		end
	
	else
		-- negative ramp
		for i = 0, iterMaxNeg, 1 do
			if i < (iterMaxNeg/2)  then
				vValue = i*stepNeg
			else
				vValue = Vneg - (i - iterMaxNeg/2)*stepNeg
			end
			ramp[k] = (-1)*vValue
			k    	= k + 1
		end
		
		-- positive ramp
		for i = 0, iterMaxPos, 1 do
			if i < (iterMaxPos/2)  then
				vValue = i*stepPos
			else
				vValue = Vpos - (i - iterMaxPos/2)*stepPos
			end
			ramp[k] = vValue
			k    	= k + 1
		end
	end 
	
	return ramp
end

