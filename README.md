# swep
bugfixes for erin's swarming emotional pianos 

# TODO
The pi script is supposed to send a '1' after a button press. Issue is that the OSC library seems to only permit sending a single-digit int in the TTS, but a single-digit int seems to trigger problems on startup, so Erin wants to know if you can instead send a string stating 'start'. 

1. Clone this repo on a pi. 
2. In blinker2019.py, Create a loop that simulates a button press, something every 3 seconds lets say. 
3. This button press needs to trigger the playback of a video, AND send the OSC 'start' message to the ESP8266. 
4. Note that the OSC is being sent on the multicast bus (255.255.255.255). 
5. make a max patch with the external [oscmulticast 255.255.255.255 54321] to listen for these messages. 
6. alternative: find out if the ESP8266 has a websocket library, which can connect to the pi (server) as a client. **for a later date, This might also pave the way for faster data handling (look into whether the multicast bus is slower than websockets?)**