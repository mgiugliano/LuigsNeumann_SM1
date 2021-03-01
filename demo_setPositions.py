#!/usr/local/bin/python3

from SM1 import *   # The SM1 library is imported here

COMPORT = '/dev/tty.usbserial-AL05TVH5' # Serial port (on Windows, it is COM1,2,...)

ser     = setup_serialcom(COMPORT)      # Connection w serial port established


print('The axes positions are...\n')

output1  = query_position(ser, 1)       # Position device n. 1 acquired (as a string)
output2  = query_position(ser, 2)       # Position device n. 2 acquired (as a string)
output3  = query_position(ser, 3)       # Position device n. 3 acquired (as a string)

print('yellow axis: ' + output1)        # Print the position on screen
print('green  axis: ' + output2)        # Print the position on screen
print('red    axis: ' + output3)        # Print the position on screen



print('Setting new axes position...\n')

set_position(ser, 1, '+00000.00')                # Position device n. 1 set to 0.
set_position(ser, 2, '+00000.00')                # Position device n. 2 set to 0.
set_position(ser, 3, '+00000.00')                # Position device n. 3 set to 0.

#time.sleep(4)                                   # Sleep 4 s to allow for motors to stop
moving = True
while is_moving(ser, 3):
    print('.', end='', flush=True)
print('\n')

print('Now the axes positions are...\n')

output1  = query_position(ser, 1)       # Position device n. 1 acquired (as a string)
output2  = query_position(ser, 2)       # Position device n. 2 acquired (as a string)
output3  = query_position(ser, 3)       # Position device n. 3 acquired (as a string)

print('yellow axis: ' + output1)        # Print the position on screen
print('green  axis: ' + output2)        # Print the position on screen
print('red    axis: ' + output3)        # Print the position on screen

print('')

ser.close()                             # Connection with serial port closed
