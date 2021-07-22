#made for Erin Gee's Swarming Emotional Pianos 2019 installation version on RasPi 2
#using pi supply

#OFF Led on box indicates that power is connected but Pi is off
#ON Led on box indicates that power is connected and Pi is ON
#WAIT Led is jumped from onboard LED on Pi, lets you know when Pi is reading/writing to the hard drive

#for the pi supply
from subprocess import call

#for osc support
from pythonosc.udp_client import SimpleUDPClient

#for the hardware I/O
import RPi.GPIO as GPIO

import time
import subprocess
import sys
import socket

#palumbo bootstrap code part 1
import threading



#Functions for shutting down pi or killing program---------------------------
def shutdown(shutdownPiButton):
  time.sleep(.2)
  if (GPIO.input(shutdownPiButton)):
    print ('logout')
    GPIO.cleanup()  # need to clean up GPIO buffers
    call('halt', shell=False)

  else: print ('ignoring button press')

def exitProgram(exitProgramButton):
  global restorePi
  restorePi = 0
  print ("leaving program")

#variables-------------------------------------------------------------------

shutdownPiButton = 7 #logs out of the raspberry pi

exitProgramButton = 10  #exits the installation program
restorePi = 1           #if this variable is low return exit program

butPin = 11        #input: activates the installation
readyLed = 12      #light to tell you when the program is running
activatePin = 13   #output: activates the robots

oscRemoteIP = "255.255.255.255"
oscRemotePort = 54321


GPIO.setwarnings(False)

# GPIO.setmode(GPIO.BOARD)          # this determines what GPIO mode we are in
# GPIO.setup(readyLed, GPIO.OUT)    #led lights when installation is "ready"
# GPIO.setup(activatePin, GPIO.OUT) #sends robot signal

# # all buttons are pulled up, active low
# GPIO.setup(shutdownPiButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # connected to Log Out button
# GPIO.setup(exitProgramButton, GPIO.IN, pull_up_down=GPIO.PUD_UP) # push this "kill" button to use the Pi like normal
# GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)            # connected to installation button and "test"

#wireless osc setup
client = SimpleUDPClient(oscRemoteIP, oscRemotePort)
client._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#code-------------------------------------------------------------------

# #call functions when state changes are detected on buttons
# GPIO.add_event_detect(shutdownPiButton, GPIO.FALLING, callback=shutdown, bouncetime=1500)     #powerdown function
# GPIO.add_event_detect(exitProgramButton, GPIO.FALLING, callback=exitProgram, bouncetime=1000) #killprogram function

#what time is it
time_stamp = time.time()

#dummy value : will make sure that the LED and activate pin are initialized probperly on first run of loop
prevButtonValue = (-1)
GPIO.output(activatePin, GPIO.LOW)  #robots are sleeping, deactivated
GPIO.output(readyLed, GPIO.HIGH)    #program is running, waiting for input

#palumbo bootstrap code part 2
WAIT_SECONDS = 3

def spoof():
    print ('button pressed!')
    client.send_message("/robot/active", '!')
    time.sleep(0.5)
    client.send_message("/robot/active", '?')
    threading.Timer(WAIT_SECONDS, spoof).start()
    
spoof()

try:
  while restorePi == 1: #while the program is running normally
    buttonValue = GPIO.input(butPin)
    if buttonValue != prevButtonValue:    #button toggled
      prevButtonValue = buttonValue       #toggle button state
      if not buttonValue:
        GPIO.output(readyLed, GPIO.LOW)
        GPIO.output(activatePin, GPIO.HIGH) #message robots to begin (detectButton function on Arduinos)

        # Send one osc message and receive exactly one osc message (blocking)
        print ('button pressed!')
        client.send_message("/robot/active", '!')
        time.sleep(0.5)
        client.send_message("/robot/active", '?')
        GPIO.output(activatePin, GPIO.LOW) #return back to the "not pressed" state after robots have been activated
        subprocess.call("omxplayer" + " Laurence2019-test.mov", shell=True)
        #omx player can only play one thing at a time anyways so extra button presses don't bother anything.
        GPIO.output(readyLed, GPIO.HIGH) #waiting for input once more

except KeyboardInterrupt:
  print ('keyboard interrupt. Now exiting program.') # do this, then clean up GPIO buffers

except OSError as err:
  print ('OS error: ', err)

except :
  print ('other error or exception occurred: ', sys.exc_info()[0])

finally:
  GPIO.cleanup() # reset GPIO pins before exit
