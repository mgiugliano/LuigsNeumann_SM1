#!/usr/local/bin/python3

# SM1_manipulators.py
#
# Feb 25th 2021 - Michele Giugliano


NAME   = 'SM1_manipulators.py'
HEIGHT = 5  # height of the buttons
WIDTH  = 10  # width of the buttons

#import os as os                 # Useful for inferring log file "basename"
#import time
from tkinter import *           # Imports everything from the tkinter lib
import tkinter.font as font

from SM1 import *   # The SM1 library is imported here

COMPORT = '/dev/tty.usbserial-AL05TVH5' # Serial port (on Windows, it is COM1,2,...)


def cX(event=None):       #set event to None to take the key argument from .bind
    #print('Button X')
    reset_counter(ser, 1)

def cY(event=None):       #set event to None to take the key argument from .bind
    #print('Button Y')
    reset_counter(ser, 2)

def cZ(event=None):       #set event to None to take the key argument from .bind
    #print('Button Z')
    reset_counter(ser, 3)

def cGO(event=None):       #set event to None to take the key argument from .bind
    #print('Button Z')
	step_forward(ser, 3, int(STEP.get()))

#def cSTEP(event=None):       #set event to None to take the key argument from .bind
#    print('Field STEP')



#------------------------------------------------------------------------------
master = Tk(className='SM1 manipulators - v 0.1') # It creates the main GUI window.
master.geometry("720x490")                       # It sets size only.
#center_window(425, 290)                           # It sets both position and size.
master.resizable(True, True)                    # It prevents from resizable.

# CREATION AND DEFINITION OF THE GUI OBJECTS
canvas = Canvas(master, background="black")
#btn_fr = Frame(master, background="black")

canvas.pack(side="top",    fill="both", expand=False)
#btn_fr.pack(side="bottom", fill="both", expand=False)

myFont1 = font.Font(family='Helvetica', size=30, weight="bold")
myFont2 = font.Font(family='Helvetica', size=20, weight="bold")

STEP     = StringVar()  #
xpos     = StringVar()  # 
ypos     = StringVar()  # 
zpos     = StringVar()  # 

STEP.set('1')

ser     = setup_serialcom(COMPORT)      # Connection w serial port established

#------------------------------------------------------------------------------
# BUTTONS CREATION AND ATTRIBUTES
#------------------------------------------------------------------------------
bX  = Button(canvas, textvariable = xpos,    command = cX,  height = HEIGHT, width = WIDTH, font=myFont1)
bY  = Button(canvas, textvariable = ypos,    command = cY,  height = HEIGHT, width = WIDTH, font=myFont1)
bZ  = Button(canvas, textvariable = zpos,    command = cZ,  height = HEIGHT, width = WIDTH, font=myFont1)

bGO  = Button(canvas, text = 'GO (Z)!!',    command = cGO,  height = HEIGHT, width = 14, font=myFont1)

bSTEP  = Entry(canvas, textvariable=STEP, font=myFont2, justify="left", width=14, bg="white", fg="black", bd=3, highlightcolor="red")


#------------------------------------------------------------------------------
# LAYOUT OF EACH ELEMENT OF THE GUI
#------------------------------------------------------------------------------
bX.grid(row=0, column=1, sticky="ew")
bY.grid(row=0, column=2, sticky="ew")
bZ.grid(row=0, column=3, sticky="ew")
bSTEP.grid(row=1, column=1, sticky="ew")
bGO.grid(row=1, column=3, sticky="ew")




#master.mainloop()

while True:
	output1  = query_position(ser, 1)       # Position device n. 1 acquired (as a string)
	output2  = query_position(ser, 2)       # Position device n. 2 acquired (as a string)
	output3  = query_position(ser, 3)       # Position device n. 3 acquired (as a string)

	xpos.set(output1)
	ypos.set(output2)
	zpos.set(output3)
	time.sleep(0.5)
    #print('Hello World!')
    #time.sleep(1)
    #update_idletasks()
	master.update()
