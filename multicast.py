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

#palumbo bootstrap code
import threading

WAIT_SECONDS = 3

def spoof():
    print(time.ctime())
    threading.Timer(WAIT_SECONDS, spoof).start()
    
spoof()

oscRemoteIP = "255.255.255.255"
oscRemotePort = 54321


#wireless osc setup
client = SimpleUDPClient(oscRemoteIP, oscRemotePort)
client._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

finally:
  GPIO.cleanup() # reset GPIO pins before exit
