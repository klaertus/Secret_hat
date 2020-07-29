# Secret Hat
A Raspberry Pi subsystem for the Sense Hat

This project is a subsystem that contains many useful applications, adapted to be used on the Sense Hat.


## Installation

```bash
git clone https://github.com/charl050/Secret_hat.git
cd Secret_hat
./install.sh   # Not finished
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

| WARNING: Please consider that the lib used to encrypt messages and hash passwords is not secure! |
| --- |
#### System and board infos
Application displaying informations about the Raspberry and the Sense hat.

#### Tracking infos
Application allowing to record logs and informations (time, ip, ping, Sense Hat temperature, pressure, humidity, orientation, compass, accelerometer, gyroscope and traceroute) and save them in saved_logs.txt.

#### Timer
A timer allowing to activate GPIOs, reset the Secret Hat or shutdown it.

#### Backdoor
Simple backdoor using Dataplicity.

#### Pirate Box
PHP file explorer to share files with another connected users. This app uses https://github.com/prasathmani/tinyfilemanager for the explorer.

#### Setting
Setting application allowing to set up Wifi (connect or AP), the iptables rules, the main password, the brightness, the password precision (50 is default, 1 is too much precise), shutdown, reboot and reset the Secret Hat.


## Configuration

If the config files doesn't exist or contain error, the Secret Hat will show a error, and ask you if you want to reset config files. Select Yes if it's first boot

### Wifi APs

Add yours wifis APs to the config.ini : 
```
[wifi]
ssid1         # Wifi with no key
ssid2 = key2
ssid3 = key3
```

### Reset

There are three resetting modes :
* Mode 1 : reset all configuration, and delete all messages
* Mode 2 : delete all subsystem
* Mode 3 : block the Secret Hat (only for main password)

### Personalization

Edit the text color and the text scrolling speed in config.ini :
```
[personalization]
color1 = [255,255,0]  # List or tuple
color2 = [0,255,0]  # List or tuple
speed = 0.05  # Float
```

### Iptables rules

Add your own iptables rules in iptables_rules file :

```
# Rule name 1 
rule command 1

# Rule name 2
rule command 2
```
If iptables_rule contains errors, the Secret Hat will show a error and return in the Setting menu.


