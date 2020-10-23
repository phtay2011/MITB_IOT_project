# Welcome to MITB IOT PROJECT!

## Folder navigation

 - Main folder contains code that will run on AWS (This is all the stuff that the server will run)
	 - main.py - This is the main flask app that will be running the API
	 - gmap_api.py - This module does the route calculation and traffic light instructions
	 - mqtt_module.py - This module takes the traffic light instruction and publish to the broker
 - hardware_code - This stores all the code that will be run on laptop / microbit
	 -  laptop_gateway.py - This will be run on laptop. This guy will subscribe to a topic and send the info via serial to the microbit
	 - MB gateway - This will receive info from laptop via serial and broadcast it via radio
	 - MB radio linked to GW - This will receive info from MG gateway via radio and print the traffic light color on LED
 - Other stuff not part of main code
	 - Google Map plot test.ipynb - This is for MAX to see how the map will look like on the Front End
	 - sample_payloads.md - This is the API docs
	 - requirements_deployment.txt - This is the list of packages to install

## UML diagrams

```mermaid
sequenceDiagram
/generate_starting_route ->> gmap_api: Sends gps coordinates
gmap_api-->>/generate_starting_route: Returns traffic light instructions and best route
/generate_starting_route ->> mqtt_module (Publisher): Sends traffic light instructions to this module
mqtt_module (Publisher) ->> HiveMQ: Sends traffic light instructions to the HiveMQ Broker
HiveMQ ->> laptop_gateway(subscriber): Receives the info from the broker  
laptop_gateway(subscriber) ->> MB gateway: Sends info to gateway microbit via serial
MB gateway ->> MB radio linked to GW: Sends info from gateway microbit to traffic light microbit
```
