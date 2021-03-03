

# SM1.py - Library (work in proegress)
#
# Requires PySerial and time libraries
#
# Michele Giugliano and Matteo Manzati, 26/2/2021

import serial 		# PySerial library, required for serial communications
import time 		# time library, required for implementing "delays" (to wait)

STX = chr(0x02)		# These are constant whose values have been looked up in the
DLE = chr(0x10)		# official ANSI definition of the ASCII alphabet.
ACK = chr(0x06)		# They are specified as hexadecimal values (i.e. 0x..) for no
NAK = chr(0x15)		# particular reason, other than the easy correspondences found
ETX = chr(0x03)		# on the official documents we got.

#COMPORT = '/dev/tty.usbserial-AL05TVH5'  # it would be COM3 or COM2
DELAY = 0.1                              # seconds - delay the SM1 unit takes (at most) to respond

#--------------------------------------------------------------------------------------------------------
# This function calculates the BBC (Block Check Character) from an input string of characters, 'str1'.
#
# The serial communication protocol by Luigs and Neumann, interfacing the PC with the 
# Data Exchange Controller of a LM1 unit, employs and requires an ad hoc 'checksum' code.
# This described, albeit very concisely, in the documentation.
#
def BCC(str1):							# Hardware Block Check Character, as explained in the LN's doc.
	len1 = len(str1)					# The lenght of input string is obtained here.
	ans = ord(str1[0])                	# This is the value (as a decimal number) of first char (see unicode tables).   

	for i in range(1,len1):           	# For each other element of the string,... 
		ans = (ans ^ (ord(str1[i])))  	# calculate the XOR, element by element, and return the result as 'ans'. 
        								# Note: ans is a single byte (8 bits), while LM1 requires two bytes as BBC. 
        								# These two bytes are obtained from the 'high' and low 'nibble' of 'ans'
        								# (see https://stackoverflow.com/questions/42896154/python-split-byte-into-high-low-nibbles)

	high = ans >> 4						# The high nibble is obtained by "4-times right shift" of 'ans' in binary form.
	low  = ans & 0x0F 					# The low nibble is obtained by a AND operation with a 00001111 'mask', by definition.
        								# However, from LN's doc, we read: BCC consists of two bytes: 
	high = high + 0x30 					# HiNibble(BCC) + 0x30 and
	low  = low  + 0x30 					# LowNibble(BCC) + 0x30 . And so we defined them.

	out  = chr(high) + chr(low)			# We combine the two bytes (characters), concatenating them into a string.
	return out                          # We now (proudly) return the BCC.
#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# This function initialises and returns the (PySerial) 'serial' object. It specifies some fixed 
# parameters that we found working with the SM1 unit we have.
# The input argument 'comport' is a string containing 'COM1', 'COM2', etc. on Windows or 
# something like '/dev/tty.usbserial-AL05TVH5' on macOs and linux
# 
def setup_serialcom(comport):

	ser          = serial.Serial()			# The serial object ser is created and instantiated.
											# Its own properties are specified:
	ser.port     = comport   				# - the name of the com port
	ser.baudrate = 19200					# - the baud rate (19200 was found to work)
	ser.bytesize = 8						# - the start bit (8 was found to work)
	ser.parity   = 'O' 						# - the parity ('O' as in odd was found to work)
	ser.stopbits = 1						# - the stop bit (1 was found to work)
	ser.xonxoff  = False					# - xonxoff OFF
	ser.rtscts   = False					# - rtscts OFF
	ser.dsrdtr   = False					# - dsrdtr OFF
	ser.timeout  = 5						# - time out [seconds]

	# Let's now open the serial port.
	if ser.is_open:
		print('COM port was already open. Closing it...')
		ser.close()

	ser.open()

	if ser.is_open:
		print('COM port opened successfully...')

	return ser 								# The 'ser' object is returned as output of this function.
#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# This function packages the instructions required by the handshaking protocol with LM1:
# PC sends STX.... LM1 responds (within 100ms) with DLE... then PC is allowed to send a command
#
# Note: this function is 'blocking': it won't return until the handshaking is completed. 
#
def initiate_handshaking(ser):				# Useful function to initiate the handshaking with LM1

	responded = False						# Boolean variable: false until the LM1 gives us green light

	while not responded :					# Let's enter a loop where 
		ser.write(STX.encode()) 			# we keep sending STX (start-of-text),
		time.sleep(DELAY)					# then we wait a bit, and then
		data = ser.read(1)					# we check if LM1 responded with DLE (data-link-escape)
		if data == DLE.encode() :			# It that's the case, 
			responded = True
			return True						# we exit the loop and return.

#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# This function reads the response of LM1, after all the ping-pong of handshaking is done.
#
def read_response(ser):
	temp = ''
	while ser.inWaiting() > 0:
		data = ser.read(1)
		temp = temp + data.decode('ascii')
	return temp
#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# This function queries the position of the specified unit (see Example 2 from LN's documentation) and
# it returns the position as a string.
#
def query_position(ser, unit):				# Note: 'ser' is the PySerial obj; unit is =1, 2, or 3...
	#CMD = '#1?P'							# This is a sample command to query the P-osition
	CMD = '#' + str(unit) + '?P'			# The command string is assembled here and then
	ALL = CMD + BCC(CMD) + DLE + ETX 		# concatenated with BCC, DLE, and ETX characters.

	initiate_handshaking(ser) 				# Initiating the handshaking...
	ser.write(ALL.encode())					# We can now send the complete (ALL) package,
	time.sleep(DELAY)						# then we wait a bit and then we see whether we
											# can continue..
	data1 = ser.read(1)						# This response should be 'ACK'...
	data2 = ser.read(1)						# This should be 'STX'...

	if ((data1 == ACK.encode()) and (data2 == STX.encode())) :
		ser.write(DLE.encode()) 			# Then we respond with 'DLE',
		time.sleep(DELAY)					# we wait a bit, and then we read the message
		temp = read_response(ser)			# The response from LM1 is read here..
		ser.write(ACK.encode()) 			# Then the PC responds with ACK
											# In the case of '?P' command, the message from LM1
											# has a format like e.g. '#1:P+00000.004='
		msg = temp[0:13]					# This is '#1:P+00000.00' (in this example)
		bcc_computed = BCC(msg)				# We compute the BCC of 'msg' 
		bcc = temp[13:]						# This is '4=' (in this example), the BCC actually received from LM1.

		if ((bcc_computed[0] == bcc[0]) and (bcc_computed[1] == bcc[1])) :	# Check for consistency...
			#print('BCC is correct!')
			return temp[4:13]					# This is '+00000.00' (in this example)
		else:
			print('query_position(): error - wrong BCC received!')
			return ''
	else:
		print('query_position(): LM1 did not respond correctly (ACK and STX)!')
		return ''
#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# This function sets the absolute position of the specified unit 
# note: Example 1 from LN's documentation contains errors. 
#
def set_position(ser, unit, pos):
	#CMD = '#1!GF+01.234,49' (fast)
	CMD = '#' + str(unit) + '!GF' + pos 	# The command string is assembled here and then
	ALL = CMD + BCC(CMD) + DLE + ETX 		# concatenated with BCC, DLE, and the ETX characters.

	initiate_handshaking(ser) 				# Initiating the handshaking...
	ser.write(ALL.encode())					# We can now send the complete (ALL) package,
	time.sleep(DELAY)						# then we wait a bit and then we see whether we

	data1 = ser.read(1)
	if (data1 != ACK.encode()):
		print('set_position(): LM1 did not respond correctly (ACK)')

def set_position_slow(ser, unit, pos):
	#CMD = '#1!GS+01.234,49' (slow)
	CMD = '#' + str(unit) + '!GS' + pos 	# The command string is assembled here and then
	ALL = CMD + BCC(CMD) + DLE + ETX 		# concatenated with BCC, DLE, and the ETX characters.

	initiate_handshaking(ser) 				# Initiating the handshaking...
	ser.write(ALL.encode())					# We can now send the complete (ALL) package,
	time.sleep(DELAY)						# then we wait a bit and then we see whether we

	data1 = ser.read(1)
	if (data1 != ACK.encode()):
		print('set_position_slow(): LM1 did not respond correctly (ACK)')
#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# This function performs a single step, clockwise 
#
def single_step_CW(ser, unit):
	#CMD = '#1!E+'
	CMD = '#' + str(unit) + '!E+' 				# The command string is assembled here and then
	ALL = CMD + BCC(CMD) + DLE + ETX 			# concatenated with BCC, DLE, and the ETX characters.

	initiate_handshaking(ser) 				# Initiating the handshaking...
	ser.write(ALL.encode())					# We can now send the complete (ALL) package,
	time.sleep(DELAY)						# then we wait a bit and then we see whether we

	data1 = ser.read(1)
	if (data1 != ACK.encode()):
		print('single_step_CW(): LM1 did not respond correctly (ACK)')
#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# This function performs a single step, counter-clockwise 
#
def single_step_CCW(ser, unit):
	#CMD = '#1!E-'
	CMD = '#' + str(unit) + '!E-' 				# The command string is assembled here and then
	ALL = CMD + BCC(CMD) + DLE + ETX 			# concatenated with BCC, DLE, and the ETX characters.

	initiate_handshaking(ser) 				# Initiating the handshaking...
	ser.write(ALL.encode())					# We can now send the complete (ALL) package,
	time.sleep(DELAY)						# then we wait a bit and then we see whether we

	data1 = ser.read(1)
	if (data1 != ACK.encode()):
		print('single_step_CCW(): LM1 did not respond correctly (ACK)')
#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# This function steps forward the position of the specified unit
def step_forward(ser, unit, step_size):
	pos = query_position(ser, unit)		# Maybe there is no need to call this every single time...
	
	p      = float(pos) + step_size
	if (p>0):
		newpos = '+' + "{}".format('%08.2F' % p)
	else:
	    newpos = "{}".format('%09.2F' % p)
	#print(newpos)
	set_position(ser, unit, newpos)
#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# This function resets the (step) counter for the specified unit 
#
def reset_counter(ser, unit):
	#CMD = '!@S'
	CMD = '#' + str(unit) + '!@S' 				# The command string is assembled here and then
	ALL = CMD + BCC(CMD) + DLE + ETX 			# concatenated with BCC, DLE, and the ETX characters.

	initiate_handshaking(ser) 				# Initiating the handshaking...
	ser.write(ALL.encode())					# We can now send the complete (ALL) package,
	time.sleep(DELAY)						# then we wait a bit and then we see whether we

	data1 = ser.read(1)
	if (data1 != ACK.encode()):
		print('reset_counter(): LM1 did not respond correctly (ACK)')
#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# This function locks the keypad 
#
def lock_keypad(ser):
	#CMD = '!L+'
	CMD = '#1' + '!L+' 						# The command string is assembled here and then
	ALL = CMD + BCC(CMD) + DLE + ETX 		# concatenated with BCC, DLE, and the ETX characters.

	initiate_handshaking(ser) 				# Initiating the handshaking...
	ser.write(ALL.encode())					# We can now send the complete (ALL) package,
	time.sleep(DELAY)						# then we wait a bit and then we see whether we

	data1 = ser.read(1)
	if (data1 != ACK.encode()):
		print('lock_keypad(): LM1 did not respond correctly (ACK)')
#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# This function unlocks the keypad 
#
def unlock_keypad(ser):
	#CMD = '!L+'
	CMD = '#1' + '!L-' 						# The command string is assembled here and then
	ALL = CMD + BCC(CMD) + DLE + ETX 		# concatenated with BCC, DLE, and the ETX characters.

	initiate_handshaking(ser) 				# Initiating the handshaking...
	ser.write(ALL.encode())					# We can now send the complete (ALL) package,
	time.sleep(DELAY)						# then we wait a bit and then we see whether we

	data1 = ser.read(1)
	if (data1 != ACK.encode()):
		print('unlock_keypad(): LM1 did not respond correctly (ACK)')
#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# This function queries the status of the specified unit and
# it returns the status response as a string.
#
def query_status(ser, unit):				# Note: 'ser' is the PySerial obj; unit is =1, 2, or 3...
	#CMD = '#1?Z'							# This is a sample command to query the unit 'status'
	CMD = '#' + str(unit) + '?Z'			# The command string is assembled here and then
	ALL = CMD + BCC(CMD) + DLE + ETX 		# concatenated with BCC, DLE, and ETX characters.

	initiate_handshaking(ser) 				# Initiating the handshaking...
	ser.write(ALL.encode())					# We can now send the complete (ALL) package,
	time.sleep(DELAY)						# then we wait a bit and then we see whether we
											# can continue..
	data1 = ser.read(1)						# This response should be 'ACK'...
	data2 = ser.read(1)						# This should be 'STX'...

	if ((data1 == ACK.encode()) and (data2 == STX.encode())) :
		ser.write(DLE.encode()) 			# Then we respond with 'DLE',
		time.sleep(DELAY)					# we wait a bit, and then we read the message
		temp = read_response(ser)			# The response from LM1 is read here..
		ser.write(ACK.encode()) 			# Then the PC responds with ACK
											# In the case of '?Z' command, the message from LM1
											# has a format like e.g. '#3:VP+00000.00x='
		len1 = len(temp)					# or e.g. '#3:MVP+01267.28pz'				

		msg = temp[0:(len1-4)]				# This is '#3:MVP+01267.28' (in this example)
		bcc_computed = BCC(msg)				# We compute the BCC of 'msg' 
		bcc = temp[(len1-4):(len1-2)]		# This is 'pz' (in this example), the BCC actually received from LM1.

		if ((bcc_computed[0] == bcc[0]) and (bcc_computed[1] == bcc[1])) :	# Check for consistency...
			#print('BCC is correct!')
			return msg						# This is '#3:MVP+01267.28' (in this example)
		else:
			print('query_status(): error - wrong BCC received!')
			return ''
	else:
		print('query_status(): LM1 did not respond correctly (ACK and STX)!')
		return ''
#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# This function return True only if the specified unit is (still) moving.
#
def is_moving(ser, unit):	
 moving = False
 data   = query_status(ser, unit)
 if (data[3]=='M'):
 	moving = True
 return moving
#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# This function, conceived for debugging purposes, makes the (byte) output contained in the SM1's
# messages more readable. 
#
def translate_SM1(msg): 				
	if msg == STX.encode() :			
		return '<STX>'
	elif msg == DLE.encode() :
		return '<DLE>'
	elif msg == ACK.encode() :
		return '<ACK>'
	elif msg == NAK.encode() :
		return '<NAK>'
	elif msg == ETX.encode() :
		return '<ETX>'
	else:
		return msg 	
#--------------------------------------------------------------------------------------------------------

