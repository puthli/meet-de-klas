# meet-de-klas
(Measure the classroom)
IoT product to measure air-quality in schools

This repository contains:
1. Micropython code for the pycom LoPy board including
- driver for the CoZIR AH CO2 sensor
- LoRaWan code to connect to thethingsnetwork.org (TTN) open LoRa Network

2. Docker scripts to start up the associated server including
- Keycloak Identity Management
- Fiware Orion and Comet data broker and historical database
- Dashboard application written in D3
- Security proxy written in node.js
(coming soon..)

3. Configuration settings for 
- thethingsnetwork console
- Fiware Orion and Fiware Comet
- Keycloak
(coming soon..)

4. Notification code for the smartphone app
(coming soon..)
