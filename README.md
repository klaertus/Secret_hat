# Secret_Hat
Raspberry Pi subsystem for the Sense Hat

This project was developed as part of a competition organized by UClouvain. It contains many applications for a potential intelligence agency, adapted to be used on the Sense Hat.


## Installation

```bash
https://github.com/r4ma050/Secret_Hat.git
cd Secret_hat
./install.sh
```

## Applications

*  Message encryption
*  System and board infos
*  Tracking infos
*  Timer
*  Backdoor
*  Pirate box
*  Settings


#### Message encryption
Application allowing to encrypt messages with the positions of the Sense Hat. 

| WARNING: Please consider that the lib used to encrypt messages and hash passwords is not secure, and has only been used as part of the competition! |
| --- |
#### System and board infos
Application displaying informations about the Raspberry and the Sense hat.

#### Tracking infos
Application allowing to record logs and informations (time, ip, ping, Sense Hat temperature, pressure, humidity, orientation, compass, accelerometer, gyroscope and traceroute) and save them in saved_logs.txt.

#### Timer
A timer allowing to activate GPIOs, reset the Secret Hat or shutdown it.

#### Backdoor
Simple backdoor using Facebook or Dataplicity.

#### Pirate Box
PHP file explorer in /shared to share files to another connected users. This app uses https://github.com/prasathmani/tinyfilemanager for the explorer.

#### Setting
Setting application allowing to set up Wifi (connect or AP), the main password, the brightness, the password precision (50 is default, 1 is too much precise), and reset the Secret Hat.

## Configuration

If the config.ini file doesn't exist, it is automatically created with defaults values. 
### Wifi APs
Add yours wifis APs to the config.ini, like this 
```
[wifi]
ssid1 = key1
ssid2 = key2
ssid3 = key3
```

### Password configuration

There are three resetting mode:
* Reset only all configuration, and deletes all messages
* Delete all subsystem
* Only block during a exponential time

### Applications
Each application has his own config file. There are a global config file for displaying applications in main menu. Be careful when editing this file, because if there is an error, the main script will crash.
```
[apps]
app number = app script | App menu name 
```
