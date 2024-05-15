This repository aims to document and hold the code required for Team 1 of UMass Boston's 23'-24' Senior Design class: Robert, Yousuf, Brandon.

### Operation Manual
There are three main components to the system: the central hub and two drones. Connecting to the system is currently a week point of our project, as the correct scripts do not run automatically. A great next step could be to have the scripts run at startup. For now, each of the three Raspberry Pis (hub, drone 1, drone 2) need to be connected to a Wi-Fi network so that they can be controlled via SSH. To initialize the Wi-Fi connection for the first time, you will need an external monitor, keyboard, and mouse. 
For each Pi, once you have it connected to Wi-Fi, open up the terminal and type “"ifconfig". This command will show the IP address of the Pi which is needed for SSH. Record each of these addresses for later. Once all three are connected, on a separate computer, connect to each of the Pis through SSH using the IP addresses (you can have all three SSH sessions running at once). There are several different apps you can use for this, but if you do not have any experience with SSH, then we would recommend PuTTY since it is free and has always worked for us. Once connected to the Pi, you will need to sign in. The credentials for each of the Pis are shown in Table 2.

Device	Username	Password
Central Hub	hub	hub
Drone 1	droneone	droneone
Drone 2	drone1	drone1
Table 2 – Raspberry Pi credentials

Once you are logged into a Pi, you will need to locate the “senior_design” directory. This should be either in the “Desktop” directory or in the user directory. Once in this directory, it may be wise to get the latest version of the code by fetching any updates from the repository on Github. To do this, type “git pull”. If there are any new updates to the code, this should be automatically download them. 
Now, the script which you will run will depend on the device you are on. For drone 1, which is the drone with the custom PCB on the Pi, you will have to run


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
20) ~~Install Mission Planner on Drone 2~~
21) ~~Create script to get GPS coordinates~~
22) ~~Integrate with current script~~
23) Get script to run on startup
24) Download Raspbian onto 32 GB microSD. Use this as a replacement for microSD currently in Drone 1
25) Add to hub script a way to reconfigure drone order based on results of ML model
26) Change drone networking to do one at a time
27) Change drone script to get sensor data only once lead drone has reached its destination
28) ~~Change hub code to take user input for gps location~~
29) Add flight instructions to hub script
#### Hardware
1) ~~Update PCB design~~
2) ~~Order PCB~~
3) ~~Assemble PCB~~
4) ~~Manually test line-of-site range for a pair of XBees, or find a reliable figure online~~
5) ~~Calibrate second drone~~
