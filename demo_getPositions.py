#!/usr/local/bin/python3

from SM1 import *   # The SM1 library is imported here

COMPORT = '/dev/tty.usbserial-AL05TVH5' # Serial port (on Windows, it is COM1,2,...)

ser     = setup_serialcom(COMPORT)      # Connection w serial port established

print('Reading axes position...\n')

output1  = query_position(ser, 1)       # Position device n. 1 acquired (as a string)
output2  = query_position(ser, 2)       # Position device n. 2 acquired (as a string)
output3  = query_position(ser, 3)       # Position device n. 3 acquired (as a string)

print('yellow axis: ' + output1)        # Print the position on screen
print('green  axis: ' + output2)        # Print the position on screen
print('red    axis: ' + output3)        # Print the position on screen

print('')


print(query_status(ser, 3))


ser.close()                             # Connection with serial port closed
