#!/usr/local/bin/python3

# SM1_manipulators_v2.py - it is a slightly improved version of the GUI with the
# more appropriate 'refresh' event generation, according to the style of TKinter.
#
# Mar 4th 2021 - Michele Giugliano and Matteo Manzati

COMPORT = '/dev/tty.usbserial-AL05TVH5' # Serial port (on Windows, replace it with COM1,2,...)
REFRESH = 400 # ms - refresh rate for the X,Y,Z motor position queries

NAME   = 'SM1_manipulators_v2.py'
HEIGHT = 5    # height of the buttons canvas
WIDTH  = 10   # width of the buttons canvas

from tkinter import *           # Imports everything from the tkinter lib
import tkinter.font as font     # Import the font sublibrary from tkinter
from SM1 import *               # The SM1 library is imported here
#--------------------------------------------------------------------------------

STEP     = StringVar()          # Global variable, containing the 'step size'
STEP.set('1')                   # It is initialised to '1' (~4-7um)...

#--------------------------------------------------------------------------------
# These functions query the position of each motor, update the label of the
# corresponding buttons, and add an additional even (i.e. calling themselves again)
# after a REFRESH time (in ms). (inspired by https://www.youtube.com/watch?v=0I97O2p-4Tc)
#
def display_X_position():
    bX['text'] = query_position(ser, 1)
    bX.after(REFRESH, display_X_position)

def display_Y_position():
    bY['text'] = query_position(ser, 2)
    bY.after(REFRESH, display_Y_position)

def display_Z_position():
    bZ['text'] = query_position(ser, 3)
    bZ.after(REFRESH, display_Z_position)

#--------------------------------------------------------------------------------
# These functions define the behavior when the use presses each of the buttons.
#
def cX(event=None):       #set event to None to take the key argument from .bind
    reset_counter(ser, 1) # When the button is pressed, the corresponding position is "zeroed"..

def cY(event=None):       #set event to None to take the key argument from .bind
    reset_counter(ser, 2) # When the button is pressed, the corresponding position is "zeroed"..

def cZ(event=None):       #set event to None to take the key argument from .bind
    reset_counter(ser, 3) # When the button is pressed, the corresponding position is "zeroed"..

def cGO(event=None):      #set event to None to take the key argument from .bind
	step_forward(ser, 3, int(STEP.get())) # When the "step-advance" button is pressed..
#--------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Let's create the GUI...
#
master = Tk(className='SM1 manipulators - v 0.2') # It creates the main GUI window.
master.geometry("720x490")                        # It sets size only.
master.resizable(True, True)                      # It prevents from resizable.
#
# CREATION AND DEFINITION OF THE GUI OBJECTS
canvas = Canvas(master, background="black")
canvas.pack(side="top",    fill="both", expand=False)
#
myFont1 = font.Font(family='Helvetica', size=30, weight="bold")
myFont2 = font.Font(family='Helvetica', size=20, weight="bold")
#
#------------------------------------------------------------------------------
# BUTTONS AND ENTRY-FIELD CREATION AND ATTRIBUTES
#------------------------------------------------------------------------------
bX  = Button(canvas, text = '',      command = cX,  height = HEIGHT, width = WIDTH, font=myFont1, fg='yellow')
bY  = Button(canvas, text = '',      command = cY,  height = HEIGHT, width = WIDTH, font=myFont1, fg='green')
bZ  = Button(canvas, text = '',      command = cZ,  height = HEIGHT, width = WIDTH, font=myFont1, fg='red')
bGO = Button(canvas, text = 'STEP!', command = cGO, height = HEIGHT, width = 14,    font=myFont1, fg='red')

bSTEP  = Entry(canvas, textvariable=STEP, font=myFont2, justify="left", width=14, bg="white", fg="black", bd=3, highlightcolor="red")
#------------------------------------------------------------------------------
# LAYOUT OF EACH ELEMENT OF THE GUI
#------------------------------------------------------------------------------
bX.grid(row=0,    column=1, sticky="ew")
bY.grid(row=0,    column=2, sticky="ew")
bZ.grid(row=0,    column=3, sticky="ew")
bSTEP.grid(row=1, column=1, sticky="ew")
bGO.grid(row=1,   column=3, sticky="ew")
#------------------------------------------------------------------------------
#
# THIS IS THE START OF THE ACTUAL CODE
ser     = setup_serialcom(COMPORT)      # Connection w serial port established

display_X_position()                    # Position X is queried and refreshed..
display_Y_position()                    # Position Y is queried and refreshed..
display_Z_position()                    # Position Z is queried and refreshed..

#------------------------------------------------------------------------------
# KEYBOARD SHORT CUT
#------------------------------------------------------------------------------
master.bind('<F1>', cX) #binds 'F1' short-cut to 'zeroing' X coordinate
master.bind('<F2>', cY) #binds 'F2' short-cut to 'zeroing' Y coordinate
master.bind('<F3>', cZ) #binds 'F3' short-cut to 'zeroing' Z coordinate
master.bind('<space>', cGO) # binds 'space' short-cut to 'step forward' on Z coordinate
#------------------------------------------------------------------------------

master.mainloop()                       # The main (event) loop is started here..
