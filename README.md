# Secret_Hat

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
Application allowing to encrypt messages with the positions of the Sense Hat

#### System and board infos
Application displaying informations about the Raspberry and the Sense hat

#### Tracking infos
Application allowing to record logs and informations (time, ip, ping, Sense Hat temperature, pressure, humidity, orientation, compass, accelerometer, gyroscope and traceroute) and save them in saved_logs.txt.

#### Timer
Timer allowing to activate GPIOs, reset the Secret Hat or shutdown it.

#### Backdoor
Simple backdoor using Facebook or Dataplicity.

#### Pirate Box
PHP file explorer in /shared to share files to another connected users. This app use https://github.com/prasathmani/tinyfilemanager for the explorer

#### Setting
Setting application allowing to set up Wifi (connect or AP), the main password, the brightness, the password precision (50 is default, 1 is too much precise), and reset the Secret Hat.


