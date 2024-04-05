This repository aims to document and hold the code required for Team 1 of UMass Boston's 23'-24' Senior Design class. The foundation for much of the code can be found [here.](https://github.com/AbhiSharma04/Drone-Mesh-Communication-Network) This repository was put together by three graduate students of computer science who worked together with our team for the fall semester. Their work provided a lot of help, but as our project developed, it became time to make some changes and specialize things for our own uses.

### Notes:
#### USB Order
When running the drone script for the first time, the Arduino might need to be unplugged and plugged back in. The script works assuming that the XBee is connected before the Arduino. This matters because of the way the USB numbers are assigned by the Pi OS. It would be nice if there was a workaround where this wouldn't matter. Actually a possible solution would be to check for the specific error, and if it thrown, try again with the USB directories switched.
#### Drone Data Broadcasting
Drones are currently competing to get there data read. The transmission is not happening with any sort of efficiency. There are several ways we can try to address this, but this is not a huge priority at the moment. I think a flawed system which is complete is better than an optimized system which is missing parts.
#### Mesh Network Behavioral Clarification
How do we even want this network to function? Possibility: Change script on drone so that XBee mode is configured to send data to a single other drone. Write this script so that the target drone can be changed. I don't think that's a mesh network though. Should probably have them all sending and receiving, but that just begs the question: what is the hub for?

### To Do:

#### Software
1) ~~Change XBee code on hub to accept broadcast signal from drone 1~~
2) ~~Change script on hub to decode XBee string~~
3) ~~Test that connection between the two has been established~~
4) ~~Remove device from dictionary~~
5) ~~Add GPS coordinates to dictionary~~
6) ~~Add device address dictionary to hub~~
7) ~~Test with second drone node~~
	1) ~~install script onto pi~~
	2) ~~get sensors working~~
	3) ~~check that hub gets data from both (might need to be done at home)~~
8) ~~Do one of the following: (this actually might not matter cause of how I did the array setup)~~
9) ~~Change script on hub to pass data into model. Get rid of GUI and webserver. Get rid of need for CSV files.~~
10) ~~Move fire prediction onto drones. Yes/No will be only thing sent back to hub. Hub will be responsible for maintaining mesh network~~
	1) ~~Drones send output~~
	2) ~~Hub receives output~~
11) ~~Hub code can correctly connect to XBees when in range~~
12) ~~Hub code can correctly connect to XBees when out of range~~
13) ~~Back up files from Drone 1~~
14) ~~Redownload all necessary libraries onto Drone 1~~
15) ~~Get everything working on Drone 2 to work on Drone 1~~
16) ~~Solve the USB Order problem described in Notes above~~
17) ~~add functionality for drones to recieve messages~~
18) ~~add functionality for drones to pass on other drone's messages~~
19) ~~add checks for data packets~~
	1) ~~if sender of packet == the current drone, discard~~
	2) ~~add list to packet to keep track of nodes its visited, if the current drone is in the list, discard~~
	3) ~~if target == current drone, read packet~~
	4) ~~else pass on the packet~~
20) Install Mission Planner on Drone 2
21) Create script to get GPS coordinates
22) Integrate with current script
23) Get script to run on startup
24) Download Raspbian onto 32 GB microSD. Use this as a replacement for microSD currently in Drone 1
25) Add to hub script a way to reconfigure drone order based on results of ML model
26) Change drone networking to do one at a time
#### Hardware
1) ~~Update PCB design~~
2) ~~Order PCB~~
3) Assemble PCB
4) Manually test line-of-site range for a pair of XBees, or find a reliable figure online
5) Calibrate second drone
