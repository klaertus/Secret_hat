from sense_hat import SenseHat
from lib.init import *
from lib import globals


from datetime import datetime
from time import sleep, time
from multiprocessing import Process
from configparser import RawConfigParser
import netifaces as ni
import subprocess
import os

"""
This application allows to save several infos in a file, with variable update time
"""

sense = SenseHat()
track_infos = RawConfigParser(allow_no_value=True)
track_infos.read('apps/track_infos.ini')

if not os.path.isfile('./saved_logs.txt'):
    file = open('saved_logs.txt',"w+")
    file.close()


# Tracking function to start it in a parallel process
def log_track(update_sec):
        log_file_open = open('saved_logs.txt',"a")
        x=0

        while True:
            # Check ip
            try:
                ni.ifaddresses('eth0')
                iface = 'eth0'
            except:
                try:
                    ni.ifaddresses('wlan0')
                    iface = 'wlan0'
                except:
                    ni.ifaddresses('lo')
                    iface = 'lo'

            ip = ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
            try:
                ping = subprocess.check_output('ping 8.8.8.8 -c 1 -w 2', universal_newlines=True, shell=True).replace('\n', '')
                x += 1
            except:
                ping = 'Ping from 8.8.8.8 timout'

            if ping != 'Ping from 8.8.8.8 timout' and x == 10:
                x += 1
                traceroute = subprocess.check_output('traceroute 8.8.8.8', universal_newlines=True, shell=True)#.replace('\n', '')
                log_file_open.write(traceroute)
                x = 0


            log_file_open.write('time : {}, ip : {}, ping to google : {}, temperature : {}, pressure : {}, humidity : {}, orientation : {}, compass : {}, accelerometer : {}, gyroscope : {} \n'.format(datetime.now(), ip, ping, sense.get_temperature(), sense.get_pressure(), sense.get_humidity(), sense.get_orientation(), sense.get_compass_raw(), sense.get_accelerometer_raw(), sense.get_gyroscope_raw() ))

            sleep(update_sec)
        log_file_open.close()




def main(color1, color2, speed):

    passed()
    while globals.run:
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 0:
            show_message_break("1:Start/Stop", color1, speed)
            get_joystick()
            if globals.direction == 'middle':
                passed()
                if is_alive(globals.logs_process):
                    globals.logs_process.terminate()
                    while globals.direction != 'middle':
                        show_message_break('Stopped! Press ok', color2, speed)
                        get_joystick()
                    passed()
                else:
                    try:
                        update_time = int(track_infos['logs']['update_time'])
                        globals.logs_process = Process(target=log_track, args=(update_time,))
                        globals.logs_process.start()
                        globals.log_track_start_time = time()
                        while globals.direction != 'middle':
                            show_message_break('Started! Press ok', color2, speed)
                            get_joystick()
                        passed()
                    except:
                        while globals.direction != 'middle':
                            show_message_break('Track not configured! Press ok', color2, speed)
                            get_joystick()
                        passed()
        passed(2)

        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 1:
            show_message_break("2:Configuration", color1, speed)
            get_joystick()
            if globals.direction == 'middle' :
                passed()
                if is_alive(globals.logs_process):
                    while globals.direction != 'middle':
                        show_message_break('Track is started', color2, speed)
                        get_joystick()
                    passed()
                else:
                    while globals.direction != 'middle':
                        show_message_break('Update time?', color2, speed)
                        get_joystick()
                    passed()
                    update_time = int(askmessage(color2, speed).replace('[', '').replace(']', '').replace(',', '').replace(' ', ''))
                    if update_time == 0:
                        update_time = 1
                    track_infos.set('logs', 'update_time', str(update_time))
                    with open('apps/track_infos.ini', 'w') as configfile:
                        track_infos.write(configfile)
                    while globals.direction != 'middle':
                        show_message_break("Saved! Press ok", color2, speed)
                        get_joystick()
                    passed()
        passed(2)

        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 2:
            show_message_break("3:Infos", color1, speed)
            get_joystick()
            if globals.direction == 'middle' :
                passed()
                if is_alive(globals.logs_process):
                    update_time = int(track_infos['logs']['update_time'])
                    while globals.direction != 'middle':
                        show_message_break("Started:{} min".format(round((time()-globals.log_track_start_time)/60, 2)), color2, speed)
                        get_joystick()
                    passed()
                    while globals.direction != 'middle':
                        show_message_break('Update timer:{}'.format(update_time), color2, speed)
                        get_joystick()
                    passed()
                else:
                    while globals.direction != 'middle':
                        show_message_break('Track not started! Press ok', color2, speed)
                        get_joystick()
                    passed()
        passed(2)
    passed()
