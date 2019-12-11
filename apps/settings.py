from sense_hat import SenseHat
from lib.init import *
from lib import globals
from lib.encrypt import *
from lib.Wireless import *


from configparser import RawConfigParser
import os
from multiprocessing import Process
from time import sleep

"""
Settings application
"""
# Reset mode to finish line 178
sense = SenseHat()
wireless = Wireless()

config = RawConfigParser(allow_no_value = True)
password_config = RawConfigParser(allow_no_value = True)
config.optionxform = str
config.optionxform = lambda option: option

config.read('config.ini')
password_config.read('password_config.ini')




def main(color1, color2, speed):

    """
    Args :
        color1 (list or tuple) : rgb color code of titles
        color2 (list or tuple) : rgb color code of subtitles
        speed (float) : speed of the scrolling of message
    """

    passed()
    while globals.run:

        # Wifi
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 0:
            show_message_break("1:Wifi", color1, speed)
            get_joystick()
            if globals.direction == 'middle':

                passed()
                while globals.run:

                    # Connect to a wifi network
                    while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 0:
                        show_message_break("1:Connect/Disconnect", color1, speed)
                        get_joystick()
                        if globals.direction == 'middle':
                            passed()

                            if os.system('systemctl is-active hostapd') == 0:
                                while globals.direction != 'middle':
                                    show_message_break("Please stop AP before connect to wifi! Press ok", color2, speed)
                                    get_joystick()
                                passed()
                            else:
                                passed()
                                print(config.sections())
                                current_ssid = wireless.current()
                                if not current_ssid == None:
                                    wireless.disconnect()
                                    while (globals.direction != 'middle' and globals.direction != 'up'):
                                        show_message_break("Disconnected from {}! Press OK".format(current_ssid), color2, speed)
                                        get_joystick()
                                    passed()
                                # Check configuration
                                else:
                                    wifi_hotspots = config['wifi_keys']
                                    if len(wifi_hotspots) == 0 or config['wifi_keys'][str(wifi_hotspots[0])] == None:             # If no wifi configured in config.ini
                                        while (globals.direction != 'middle' and globals.direction != 'up'):
                                            show_message_break("No key in config file! Press OK", color2, speed)
                                            get_joystick()
                                        passed()
                                        break

                                    while globals.run:
                                        print("pok1")

                                        # Display the saved wifi APS
                                        while (globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left'):
                                            show_message_break('{}:{}'.format(globals.section, wifi_hotspots[globals.section]), color2, speed)
                                            get_joystick()
                                            if globals.direction == 'middle' :
                                                passed()
                                                ssid_password = config['wifi_keys'][str(wifi_hotspots[globals.section])]
                                                loading_process = Process(target = loading, args = (color1,))
                                                loading_process.start()

                                                if wireless.connect(ssid=wifi_hotspots[globals.section], password=ssid_password): # Try to connect. wireless.connect() returns True if the Secret Hat is connected
                                                    loading_process.terminate()
                                                    while (globals.direction != 'middle' and globals.direction != 'up'):
                                                        show_message_break("Connected to wifi", color2, speed)
                                                        get_joystick()
                                                    passed()
                                                else:
                                                    loading_process.terminate()
                                                    while (globals.direction != 'middle' and globals.direction != 'up'):
                                                        show_message_break("Can't connect! Press OK", color2, speed)
                                                        get_joystick()
                                                    passed()
                                        passed(len(wifi_hotspots)-1)

                            passed()
                    passed(1)

                    # Start hostapd service for use Secret Hat as AP
                    while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 1:
                        show_message_break("2:Hotspot", color1, speed)
                        get_joystick()
                        if globals.direction == 'middle':
                            passed()

                            while (globals.direction != 'middle' and globals.direction != 'up'):
                                show_message_break("This action require reboot. Continue?", color2, speed)
                                get_joystick()
                            passed()

                            if yes_no(color2):
                                if os.system('systemctl is-active hostapd') == 0:
                                    wireless_ap(color2, speed, False)
                                else:
                                    wireless_ap(color2, speed, True)

                    passed(1)

                passed()
        passed(7)

        # Iptables Rules
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 1:
            show_message_break("2:Iptables rules", color1, speed)
            get_joystick()
            if globals.direction == 'middle':
                passed()

                with open('iptables_rules','r') as iptables:
                    iptables = iptables.read()

                while globals.run:

                    while (globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left'):
                        try:
                            rule = iptables.replace('# ', '#').replace('\n','|').replace('||','').split('#')[globals.section+1].split('|')      # Read iptables_rules file
                            show_message_break("{}:{}".format(globals.section+1, rule[0]), color2, speed)
                            get_joystick()

                        except:
                            while globals.direction != 'middle':
                               show_message_break("Error in iptables_rules! Press ok", color2, speed)
                               get_joystick()
                            passed()
                            break

                        if globals.direction == 'middle':
                            passed()
                            for i in range(1, len(rule)):
                                os.system(rule[i])

                            while globals.direction != 'middle':
                               show_message_break("Rule added to iptables! Press ok", color2, speed)
                               get_joystick()
                            passed()
                    passed(len(iptables.replace('# ', '#').replace('\n','|').replace('||','').split('#'))-2)

                passed()
                while globals.direction != 'middle':
                   show_message_break("Save rules?", color2, speed)
                   get_joystick()
                passed()
                if yes_no(color2):
                    os.system('iptables-save > /etc/iptables.ipv4.nat')     # Set rules as persistent
        passed(7)

        # Set up the main password
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 2:
            show_message_break("3:Main password", color1, speed)
            get_joystick()
            if globals.direction == 'middle':
                passed()
                password_hash = password_config['main_password']['password_hash']
                encrypt_random_a = password_config['main_password']['encrypt_random_a']
                encrypt_random_b = password_config['main_password']['encrypt_random_b']
                tries = int(password_config['main_password']['tries'])
                remaining_tries = int(password_config['main_password']['remaining_tries'])
                reset_mode = int(password_config['main_password']['reset_mode'])

                if remaining_tries is -1:
                    while globals.direction != 'middle' :
                        show_message_break("Blocked", color2, speed)
                        get_joystick()
                    passed()
                    os.system('halt')

                if password_hash is not None:
                    password = askpassword(color1, color2, speed)
                    loading_process = Process(target = loading, args = (color1,))
                    loading_process.start()
                    verify = verify_pass(password, password_hash, encrypt_random_a, encrypt_random_b)

                else:
                    verify = True

                while not verify and globals.direction != 'left':
                     loading_process.terminate()
                     if tries == 0:
                         show_message_break("Incorrect", color2, speed)
                     elif remaining_tries > 0:
                         remaining_tries -= 1
                         show_message_break("Incorrect, {} tries left".format(remaining_tries), color2, speed)
                         password_config.set('main_password', 'remaining_tries', str(remaining_tries))
                         with open('./password_config.ini', 'w') as configfile:
                             password_config.write(configfile)
                     else:
                         if reset_mode == 1:
                             os.system('rm -r -f ./*.ini')
                             while globals.direction != 'middle' :
                                 show_message_break("No tries left. Press ok", color2, speed)
                                 get_joystick()
                             passed()
                             os.system('halt')
                         elif reset_mode == 2:
                             os.system('rm -d -r -f ../secret_hat')
                             while globals.direction != 'middle' :
                                 show_message_break("No tries left. Press ok", color2, speed)
                                 get_joystick()
                             passed()
                             os.system('halt')
                         elif reset_mode == 3:
                            password_config.set('main_password', 'remaining_tries', str(-1))
                            with open('password_config.ini', 'w') as configfile:
                                password_config.write(configfile)

                     get_joystick()

                     if globals.direction == 'middle'  and (remaining_tries > 0 or tries == 0 ):
                         passed()
                         password = askpassword(color1, color2, speed)
                         print(password)
                         loading_process = Process(target = loading, args = (color1,))
                         loading_process.start()
                         verify = verify_pass(password, password_hash, encrypt_random_a, encrypt_random_b)
                passed()

                if verify:
                    try:
                        loading_process.terminate()
                    except:
                        pass

                    while (globals.direction != 'middle' ):
                        show_message_break("Passed! Press ok", color2, speed)
                        get_joystick()
                    passed()

                    clear_password = askpassword(color1, color2, speed)
                    passed()

                    if not clear_password == None:
                        pass2 = 0
                        while clear_password != pass2:
                            show_message_break("Reenter password", color2, speed)
                            get_joystick()
                            if globals.direction == 'middle':
                                pass2 = askpassword(color1, color2, speed)
                        passed()

                        print('ok this a clear password')
                        print(clear_password)
                        passed()
                        while (globals.direction != 'middle' ):
                            show_message_break("Tries(0 to disabled)?", color2, speed)
                            get_joystick()
                        passed()
                        tries = askmessage(color2, speed)
                        tries = int(tries.replace('[', '').replace(']', '').replace(',', '').replace(' ', ''))
                        if not tries == 0:
                            while (globals.direction != 'middle' ):
                                show_message_break("Reset mode? 1 to reset password_config, 2 to delete all secret_hat, 3 to block", color2, speed)
                                get_joystick()
                            passed()
                            reset_mode = askmessage(color2, speed)
                            while reset_mode != '[1]' and reset_mode != '[2]' and reset_mode != '[3]':
                                while (globals.direction != 'middle' ):
                                    show_message_break("Please select 1, 2 or 3", color2, speed)
                                    get_joystick()
                                passed()
                                reset_mode = askmessage(color2, speed)
                            reset_mode = int(reset_mode.replace('[', '').replace(']', '').replace(',', '').replace(' ', ''))

                            while (globals.direction != 'middle' ):
                                show_message_break("Infos:", color1, speed)
                                get_joystick()
                            passed()
                            if tries == 0:
                                show = 'none'
                            else:
                                show = tries
                                while (globals.direction != 'middle' ):
                                    show_message_break("reset mode:{}".format(reset_mode), color2, speed)
                                    get_joystick()
                                passed()

                            while (globals.direction != 'middle' ):
                                show_message_break("tries:{}".format(show), color2, speed)
                                get_joystick()
                            passed()

                    else:
                        tries = 0
                        reset_mode = 0

                    while globals.direction != 'middle' :
                        show_message_break("Confirmation?", color1, speed)
                        get_joystick()
                    passed()

                    if yes_no(color2):
                        if clear_password == None:
                            password_config.set('main_password', 'password_hash', None)
                        else:
                            loading_process = Process(target = loading, args = (color1,))
                            loading_process.start()
                            encrypt_all = hash_password(clear_password)
                            remaining_tries = tries
                            password_config.set('main_password', 'password_hash', str(encrypt_all.split("|")[0]))
                            password_config.set('main_password', 'tries', str(tries))
                            password_config.set('main_password', 'remaining_tries', str(remaining_tries))
                            password_config.set('main_password', 'encrypt_random_a', str(encrypt_all.split("|")[1]))
                            password_config.set('main_password', 'encrypt_random_b', str(encrypt_all.split("|")[2]))
                            password_config.set('main_password', 'reset_mode', str(reset_mode))
                            loading_process.terminate()

                        with open('password_config.ini', 'w') as configfile:
                            password_config.write(configfile)

                        while (globals.direction != 'middle' ):
                            show_message_break("Saved! Press ok", color2, speed)
                            get_joystick()
                        passed()

                    else:
                        while (globals.direction != 'middle' ):
                            show_message_break("Cancelled! Press ok", color2, speed)
                            get_joystick()
                        passed()
        passed(7)

        # Set up the brightness
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 3:
            show_message_break("4:Brightness", color1, speed)
            get_joystick()
            if globals.direction == 'middle':
                passed()
                if sense.low_light:
                    sense.low_light = False
                    config.set('personalization', 'low_light', '0')
                else:
                    sense.low_light = True
                    config.set('personalization', 'low_light', '1')
                with open('./config.ini', 'w') as configfile:
                    config.write(configfile)
        passed(7)

        # Password precision, 1 is very very precise (too in fact)
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 4:
            show_message_break("5:Passowrd precision", color1, speed)
            get_joystick()
            if globals.direction == 'middle':
                passed()
                password_precision = askmessage(color2, speed)
                while int(password_precision.replace('[', '').replace(']', '').replace(',', '').replace(' ', '')) == 0:
                    while (globals.direction != 'middle' ):
                        show_message_break("Can't set to 0! Press ok", color2, speed)
                        get_joystick()
                    passed()
                    password_precision = askmessage(color2, speed)
                password_precision = int(password_precision.replace('[', '').replace(']', '').replace(',', '').replace(' ', ''))
                try:
                    config.set('other', 'password_precision', str(password_precision))
                except:
                    config.add_section('other')
                    config.set('other', 'password_precision', str(password_precision))
                with open('./config.ini', 'w') as configfile:
                    config.write(configfile)
        passed(7)

        # Shutdown Secret Hat
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 5:
            show_message_break("6:Shutdown", color1, speed)
            get_joystick()
            if globals.direction == 'middle':
                passed()
                if yes_no(color2):
                    os.system('halt')
        passed(7)

        #Reboot
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 6:
            show_message_break("7:Reboot", color1, speed)
            get_joystick()
            if globals.direction == 'middle':
                passed()
                if yes_no(color2):
                    os.system('reboot')
        passed(7)

        # Reset
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 7:
            show_message_break("8:Reset", color1, speed)
            get_joystick()
            if globals.direction == 'middle':
                passed()
                while (globals.direction != 'middle' and globals.direction != 'up'):
                    show_message_break("This action will halt system. Continue?", color2, speed)
                    get_joystick()
                passed()

                if yes_no(color2):

                    while globals.run:

                        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 0:
                            show_message_break("1:Reset config and delete messages", color1, speed)
                            get_joystick()
                            if globals.direction == 'middle':
                                passed()
                                if yes_no(color2):
                                    os.system('rm -r -f ./*.ini')
                                    while (globals.direction != 'middle' ):
                                        show_message_break("Resetted! Press ok", color2, speed)
                                        get_joystick()
                                    passed()
                                    os.system('halt')
                        passed(1)

                        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 1:
                            show_message_break("2:Delete all Secret Hat", color1, speed)
                            get_joystick()
                            if globals.direction == 'middle':
                                passed()
                                if yes_no(color2):
                                    os.system('rm -d -r -f ../secret_hat')
                                    while (globals.direction != 'middle' ):
                                        show_message_break("Deleted! Press ok", color2, speed)
                                        get_joystick()
                                    passed()
                                    os.system('halt')

                        passed(1)


                passed()
        passed(7)

    passed()


def wireless_ap(color, speed, action):

    """Start or stop the AP. Require reboot to initialize dhcpcd

    Args:
        color (list or tuple) : rbg color code for messages
        action (bool) : True to start AP
    """

    if action:
        os.system('cp /etc/dhcpcd.conf.activate /etc/dhcpcd.conf')          # Set static ip for wlan0
        os.system('systemctl enable hostapd')                               # Enable hostapd at boot
        while globals.direction != 'middle':
            show_message_break("AP started! Please reboot", color, speed)
            get_joystick()
        passed()
        #os.system('reboot')
    else:
        os.system('systemctl disable hostapd')             # Disable hostapd at boot
        os.system('cp /etc/dhcpcd.conf.desactivate /etc/dhcpcd.conf')               # Remove static ip
        while globals.direction != 'middle':
            show_message_break("AP stopped! Please reboot", color, speed)
            get_joystick()
        passed()
        #os.system('reboot')
