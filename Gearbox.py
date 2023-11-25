################################################################################################
# Gearbox module provides debounce logic to Shifter Debouncer software
#
# There is no warranty for the program, to the extent permitted by applicable law. Except 
# when otherwise stated in writing the copyright holders and/or other parties provide the
# program "as is" without warranty of any kind, either expressed or implied, including, but
# not limited to, the implied warranties of merchantability and fitness for a particular purpose.  
# The entire risk as to the quality and performance of the program is with you.  
# Should the program prove defective, you assume the cost of all necessary servicing, 
# repair or correction.
#
# 2023 Menkaura Soft
################################################################################################

import pygame  # Joystick input
import time  # Delays
from CtypeKeyPressSimulator import PressKey, ReleaseKey  # Low level key presses
import keyboard  # Normal key presses


# Keys mode joystick loop
def debouncer(options):

    pygame.init()
    # Initialize joystick module
    pygame.joystick.init()    
    # Create a joystick object and initialize it
    shifter = pygame.joystick.Joystick(int(options['joy_id']))
    shifter.init()
   
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.

            if event.type == pygame.JOYBUTTONDOWN:
                if shifter.get_button(options['up_button']) == True:
                    KeyPress_up(options)
                    time.sleep(float(options['debounce_time']))
                if shifter.get_button(options['down_button']) == True:
                    KeyPress_down(options)
                    time.sleep(float(options['debounce_time']))
                
        # Escape to exit from Anyshift    
        if keyboard.is_pressed('End'):
                done = True


# Function to send key presses for upshift
def KeyPress_up(options):
    time.sleep(0.05)
    PressKey(int(options['up_key'], 16))  # press
    time.sleep(0.03)
    ReleaseKey(int(options['up_key'], 16))  # release


# Function to send key presses for downshift
def KeyPress_down(options):
    time.sleep(0.05)
    PressKey(int(options['down_key'], 16))  # press
    time.sleep(0.03)
    ReleaseKey(int(options['down_key'], 16))  # release      