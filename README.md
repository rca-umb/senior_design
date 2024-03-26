This repository aims to document and hold the code required for Team 1 of UMass Boston's 23'-24' Senior Design class. The foundation for much of the code can be found [here.](https://github.com/AbhiSharma04/Drone-Mesh-Communication-Network) This repository was put together by three graduate students of computer science who worked together with our team for the fall semester. Their work provided a lot of help, but as our project developed, it became time to make some changes and specialize things for our own uses.

### To Do:

#### Software
1) ~~Change XBee code on hub to accept broadcast signal from drone 1~~
2) ~~Change script on hub to decode XBee string~~
3) ~~Test that connection between the two has been established~~
4) Remove device from dictionary
5) Add GPS coordinates from dictionary
6) Add device address dictionary to hub
7) Test with second drone node
8) Do one of the following:
	1) ensure all of the data is sending/receiving in order
	2) change strings to byte arrays
9) Change script on hub to pass data into model. Get rid of GUI and webserver. Get rid of need for CSV files.
10) Back up files from Drone 1
11) Download Raspbian onto 32 GB microSD. Use this as a replacement for microSD currently in Drone 1.
12) Redownload all necessary libraries onto Drone 1
13) Get script working again on this new download
14) Install Mission Planner on Drone 1
15) Create script to get GPS coordinates
16) Change script on drone so that XBee mode is configured to send data to a single other drone. Write this script so that the target drone can be changed.
17) Add to hub script a way to reconfigure drone order based on results of ML model
18) Move fire prediction onto drones. Yes/No will be only thing sent back to hub. Hub will be responsible for maintaining mesh network
#### Hardware
1) ~~Update PCB design~~
2) Order PCB
3) Assemble PCB
