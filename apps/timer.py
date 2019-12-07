from sense_hat import SenseHat
from .lib.init import show_message_break, passed, get_joystick, loading, askmessage, yes_no, is_alive
from .lib import globals


from RPi import GPIO
from configparser import ConfigParser
from time import sleep
from multiprocessing import Process, Value
import os

"""
GPIO, shutdown and/or reset timer
"""


sense = SenseHat()
config = ConfigParser(allow_no_value=True)

# Read confirmation, create it if doesn't exist
try:
    config.read("apps/timer.ini")
    time_left = int(config['timer']['time'])
    list_gpio = config['timer']['gpio']
    shutdown = bool(config['timer']['shutdown'])
    reset_mode = bool(config['timer']['reset_mode'])
except:
    try:
        config.read('apps/timer.ini')
        config.remove_section('timer')
    except:
        file = open('apps/timer.ini','w+')
        file.close()
        config.read('apps/timer.ini')

    config.add_section('timer')
    config.set('timer', 'time', None)
    config.set('timer', 'gpio', None)
    config.set('timer', 'shutdown', None)
    config.set('timer', 'reset_mode', None)
    with open('apps/timer.ini', 'w') as configfile:
        config.write(configfile)


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
         #config.set('timer', 'time', str(globals.time_left))
         #with open('apps/timer.ini', 'w') as configfile:
         #    config.write(configfile)
         sleep(1)

     if len(list_gpio) > 0:
         for i in list_gpio:
             GPIO.setup(i, GPIO.OUT)
             GPIO.output(i, GPIO.HIGH)

     if not reset_mode:
         if reset_mode == 1:
             try:
                 os.system('cd ..')
                 #os.system('rm **/*.ini')
             except:
                 pass
         elif reset_mode == 2:
             try:
                 #os.system('cd ..')
                 os.system('cd ..')
                 #os.sytem('rm -r secret_hat')
             except:
                 pass
         else:
             print(12)
             #os.system()

     if shutdown:
         print("shut")
         #os.system(' halt')


def main(color1, color2, speed):

    """
    Args :
        color1 (list or tuple) : rgb color code of titles
        color2 (list or tuple) : rgb color code of subtitles
        speed (float) : speed of the scrolling of message
    """

    passed()
    while globals.run:

        while globals.direction != 'down' and globals.direction != 'left' and globals.section == 0:
            show_message_break("1:Start/Stop", color1, speed)
            get_joystick()
            if globals.direction == 'middle' :
                passed()
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
                        config.set('timer', 'time', None)
                        config.set('timer', 'gpio', None)
                        config.set('timer', 'shutdown', None)
                        config.set('timer', 'reset_mode', None)
                        with open('apps/timer.ini', 'w') as configfile:
                            config.write(configfile)
                        while globals.direction != 'middle':
                            show_message_break('Config resetted', color2, speed)
                            get_joystick()
                        passed()

                elif config['timer']['time'] == None:
                    while globals.direction != 'middle':
                        show_message_break('Timer not configured! Press ok', color2, speed)
                        get_joystick()
                    passed()

                else:
                    print(float(config['timer']['time']), type(float(config['timer']['time'])))
                    time_left = Value('d',float(config['timer']['time']))

                    list_gpio = config['timer']['gpio']
                    shutdown = bool(config['timer']['shutdown'])
                    reset_mode = int(config['timer']['reset_mode'])
                    globals.timer_process = Process(target = timer, args=(time_left, list_gpio, shutdown, reset_mode,))
                    globals.timer_process.start()
                    while globals.direction != 'middle':
                        show_message_break('Timer started', color2, speed)
                        get_joystick()
                    passed()
        passed(2)


        while globals.direction != 'down' and globals.direction != 'left' and globals.section == 1:
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
                            while gpio in [2,3,4,17,27,22,14,15,18,10,9,11,23,24,25,8,7,1,0,5,6,13,19,26,16,20,21,12]:
                                while globals.direction != 'middle':
                                    show_message_break('Incorrect, retry', color2, speed)
                                    get_joystick()
                                passed()
                                gpio = int(askmessage(color2).replace('[', '').replace(']', '').replace(',', '').replace(' ', ''))
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
                        try:
                            config.set('timer', 'time', str(second))
                        except:
                            config.add_section('timer')
                        config.set('timer', 'time', str(second))
                        config.set('timer', 'gpio', str(list_gpio))
                        config.set('timer', 'shutdown', str(shutdown))
                        config.set('timer', 'reset_mode', str(reset_mode))
                        config.set('reset_mode', '', str(reset_mode))
                        with open('apps/timer.ini', 'w') as configfile:
                            config.write(configfile)
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


        while globals.direction != 'down' and globals.direction != 'left' and globals.section == 2:
            show_message_break("3:Infos", color1, speed)
            get_joystick()

            if globals.direction == 'middle' :
                passed()
                if is_alive(globals.timer_process):
                    list_gpio = config['timer']['gpio']
                    shutdown = bool(config['timer']['shutdown'])
                    reset_mode = int(config['timer']['reset_mode'])
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
                        reset_mode = none
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
