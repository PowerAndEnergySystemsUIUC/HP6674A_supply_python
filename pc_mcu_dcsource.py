### PC listens to command from serial port ###
### if it is a number, it will send 
###

import serial
import re
from dc_soucre_supply_HP_6674A import *
from time import sleep


gpib  = prologix_serial(port="/dev/ttyUSB0", baud=115200, debug=False, timeout=5)
dcsource = prologix_6674A(prologix=gpib, addr=9, mode="VOLT", rang="20",  debug=False)

mcu = serial.Serial("/dev/ttyUSB1", 115200, timeout=0)

while True:
	data = mcu.read(9999)
	if len(data) > 0:
		print 'reveived:', data
		nondigit = re.search(r'[^0-9]', data)
		if nondigit:
			dcsource.shutoff()
			print "dc source is off"
		else: 
			volt = int (data)
			if volt < 48:
				dcsource.setvoltage(data)
				print "Set dc source to output"+data+"V"

	sleep(0.5)
	print 'not blocked'

mcu.close()
gpib.terminate()
