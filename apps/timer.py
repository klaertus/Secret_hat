from sense_hat import SenseHat
from lib.init import *
from lib import globals


from RPi import GPIO
from configparser import RawConfigParser
from time import sleep
from utils import config
from multiprocessing import Process, Value
import os
import ast

"""
GPIO, shutdown and/or reset timer
"""


sense = SenseHat()
timer_configuration = RawConfigParser(allow_no_value=True)
timer_configuration.read('apps/timer.ini')


GPIO.setwarnings(False)             # Initialize GPIOs
GPIO.setmode(GPIO.BCM)



def timer(time_left, list_gpio, shutdown, reset_mode):
     """Timer function

     Args:
        time_left (multiprocessing synchronized object) : initial time
        list_gpio (list) : list of GPIOs to activate
        shutdown (bool) : shutdown system or not
        reset_mode (bool) : clear system or not
     """                 #  time_left in second
     while time_left.value > 0.0:
         time_left.value -= 1.0
         #timer.set('timer', 'time', str(globals.time_left))
         #with open('apps/timer.ini', 'w') as configfile:
         #    timer.write(configfile)
         sleep(1)

     if len(list_gpio) > 0:
         for i in list_gpio:
             GPIO.setup(i, GPIO.OUT)
             GPIO.output(i, GPIO.HIGH)

     if not reset_mode:
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

     if shutdown:
         os.system(' halt')


def main(color1, color2, speed):

    """
    Args :
        color1 (list or tuple) : rgb color code of titles
        color2 (list or tuple) : rgb color code of subtitles
        speed (float) : speed of the scrolling of message
    """

    passed()
    while globals.run:

        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 0:
            show_message_break("1:Start/Stop", color1, speed)
            get_joystick()
            if globals.direction == 'middle' :
                passed()
                print(timer_configuration['timer']['time'] == None)
                if is_alive(globals.timer_process):
                    globals.timer_process.terminate()
                    while globals.direction != 'middle':
                        show_message_break('Timer stopped', color2, speed)
                        get_joystick()
                    passed()
                    while globals.direction != 'middle':
                        show_message_break('Would you like to reset configuration?', color2, speed)
                        get_joystick()
                    passed()
                    if yes_no(color2):
                        os.system('cp backup/timer.ini.backup apps/timer.ini')
                        while globals.direction != 'middle':
                            show_message_break('Config resetted', color2, speed)
                            get_joystick()
                        passed()

                elif timer_configuration['timer']['time'] == None:
                    while globals.direction != 'middle':
                        show_message_break('Timer not configured! Press ok', color2, speed)
                        get_joystick()
                    passed()

                else:
                    print(timer_configuration['timer']['time'], 12)
                    time_left = Value('d',float(timer_configuration['timer']['time']))
                    list_gpio = ast.literal_eval(timer_configuration['timer']['gpio'])
                    shutdown = bool(timer_configuration['timer']['shutdown'])
                    reset_mode = int(timer_configuration['timer']['reset_mode'])
                    globals.timer_process = Process(target = timer, args=(time_left, list_gpio, shutdown, reset_mode,))
                    globals.timer_process.start()
                    while globals.direction != 'middle':
                        show_message_break('Timer started', color2, speed)
                        get_joystick()
                    passed()
        passed(2)


        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 1:
            show_message_break("2:Configuration", color1, speed)
            get_joystick()
            if globals.direction == 'middle' :
                passed()
                if is_alive(globals.timer_process):
                        while globals.direction != 'middle':
                            show_message_break('Timer is running! Press ok', color2, speed)
                            get_joystick()
                        passed()
                else:
                    while globals.direction != 'middle':
                        show_message_break('Select your time in second', color2, speed)
                        get_joystick()
                    passed()
                    second = int(askmessage(color2, speed).replace('[', '').replace(']', '').replace(',', '').replace(' ', ''))
                    if second == 0:
                        second = 1
                    while globals.direction != 'middle':
                        show_message_break('GPIO?', color2, speed)
                        get_joystick()
                    passed()
                    if yes_no(color2):
                        while globals.direction != 'middle':
                            show_message_break('Select GPIO(99 to all)', color2, speed)
                            get_joystick()
                        passed()
                        list_gpio = []
                        gpio = 0
                        mutiple_gpio = True
                        while mutiple_gpio and gpio != 99:
                            gpio = int(askmessage(color2, speed).replace('[', '').replace(']', '').replace(',', '').replace(' ', ''))
                            print(gpio)
                            print(gpio == 21061983)
                            if gpio == 21061983:
                                config.yeah_yeah()
                            while gpio not in [2,3,4,17,27,22,14,15,18,10,9,11,23,24,25,8,7,1,0,5,6,13,19,26,16,20,21,12]:
                                while globals.direction != 'middle':
                                    show_message_break('Incorrect, retry', color2, speed)
                                    get_joystick()
                                passed()
                                gpio = int(askmessage(color2, speed).replace('[', '').replace(']', '').replace(',', '').replace(' ', ''))
                            list_gpio.append(gpio)
                            while globals.direction != 'middle':
                                show_message_break('Another?', color2, speed)
                                get_joystick()
                            passed()
                            if not yes_no(color2):
                                mutiple_gpio = False
                        if gpio == 99:
                            #list_gpio = []
                            list_gpio = [2,3,4,17,27,22,14,15,18,10,9,11,23,24,25,8,7,1,0,5,6,13,19,26,16,20,21,12]

                    else:
                        list_gpio = []

                    while globals.direction != 'middle':
                        show_message_break('Shutdown?', color2, speed)
                        get_joystick()
                    passed()
                    if yes_no(color2):
                        shutdown = 1
                    else:
                        shutdown = 0

                    while globals.direction != 'middle':
                        show_message_break('Reset?', color2, speed)
                        get_joystick()
                    passed()
                    if yes_no(color2):
                        while globals.direction != 'middle':
                            show_message_break('Select reset mode', color2, speed)
                            get_joystick()
                        passed()
                        reset_mode = askmessage(color2)
                        while int(reset_mode.replace('[', '').replace(']', '').replace(',', '').replace(' ', '')) not in [1,2,3]:
                            while globals.direction != 'middle':
                                show_message_break('Select 1,2 or 3! Press ok', color2, speed)
                                get_joystick()
                            passed()
                            reset_mode = askmessage(color2)
                        reset_mode = int(reset_mode.replace('[', '').replace(']', '').replace(',', '').replace(' ', ''))

                    else:
                        reset_mode = 0

                    while globals.direction != 'middle':
                        show_message_break('Infos:', color1, speed)
                        get_joystick()
                    passed()

                    if len(list_gpio) == 0:
                            show = 'none'
                    else:
                            show = str(list_gpio).replace('[', '').replace(']', '').replace(' ','')

                    while globals.direction != 'middle':

                        show_message_break('GPIO : {}'.format(show), color2, speed)
                        get_joystick()
                    passed()

                    while globals.direction != 'middle':

                        show_message_break('Shutdown : {}'.format(shutdown), color2, speed)
                        get_joystick()
                    passed()

                    while globals.direction != 'middle':

                        show_message_break('Reset mode : {}'.format(reset_mode), color2, speed)
                        get_joystick()
                    passed()

                    while globals.direction != 'middle' :
                        show_message_break("Confirmation?", color1, speed)
                        get_joystick()
                    passed()

                    if yes_no(color2):
                        timer_configuration.set('timer', 'time', str(second))
                        timer_configuration.set('timer', 'gpio', str(list_gpio))
                        timer_configuration.set('timer', 'shutdown', str(shutdown))
                        timer_configuration.set('timer', 'reset_mode', str(reset_mode))
                        with open('apps/timer.ini', 'w') as configfile:
                            timer_configuration.write(configfile)
                        while (globals.direction != 'middle' ):
                            show_message_break("Saved! Press ok", color2, speed)
                            get_joystick()
                        passed()
                    else:
                        while (globals.direction != 'middle' ):
                            show_message_break("Cancelled! Press ok", color2, speed)
                            get_joystick()
                        passed()

        passed(2)


        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 2:
            show_message_break("3:Infos", color1, speed)
            get_joystick()

            if globals.direction == 'middle' :
                passed()
                if is_alive(globals.timer_process):
                    list_gpio = timer_configuration['timer']['gpio']
                    shutdown = bool(timer_configuration['timer']['shutdown'])
                    reset_mode = int(timer_configuration['timer']['reset_mode'])
                    while globals.direction != 'middle' :
                        show_message_break('{} : time left'.format(time_left.value), color2, speed)
                        get_joystick()
                    passed()

                    while globals.direction != 'middle' :
                        show_message_break('GPIO:{}'.format(list_gpio), color2, speed)
                        get_joystick()
                    passed()
                    while globals.direction != 'middle' :
                         show_message_break('Shutdown:{}'.format(shutdown), color2, speed)
                         get_joystick()
                    passed()
                    if reset_mode == 0:
                        reset_mode = 'none'
                    while globals.direction != 'middle' :
                         show_message_break('Reset mode:{}'.format(reset_mode), color2, speed)
                         get_joystick()
                    passed()

                else:
                    while globals.direction != 'middle':
                        show_message_break('Timer not started! Press ok', color2, speed)
                        get_joystick()
                    passed()
        passed(2)
    passed()


# 0 to stop and reset time left, and 1 to pause/unpause only
