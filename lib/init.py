from lib import globals

from sense_hat import SenseHat
from multiprocessing import Process
from time import sleep, time
from math import floor
from configparser import RawConfigParser

sense = SenseHat()
config = RawConfigParser(allow_no_value=True)

def get_joystick():

    """Wait for joystick event, get the direction and save it in globals.direction

    """
    stick = sense.stick.wait_for_event()
    while stick.action != 'pressed':
        stick = sense.stick.wait_for_event()
    globals.direction = stick.direction
    print(globals.direction )




def is_alive(process):

    """Check if a process is running
    Args :
        process (Process object) : Process name

    Return:
        bool : True if process is running
    """

    try:
         if process.is_alive():
             return True
         else:
             return False
    except:
        return False




def passed(max_section = -2):

    """Stop the message display on the Sense Hat,
       Get joystick direction to navigate between sections or menu,
       Save the section number in globals.section,
       Reset the direction

    Args:
        max_section (int) : number of sections in the menu (0 is worth a section)

    Default:
        bool : set globals.run to True to stay in the section/menu
    """


    if is_alive(globals.show_process):
        globals.show_process.terminate()

    sense.clear()
    if max_section != -2:
        if globals.direction == 'up':
            globals.section -= 1
            if globals.section < 0:
                globals.section = max_section
        elif globals.direction == 'down':
            globals.section += 1
            if globals.section > max_section:
                globals.section = 0
        elif globals.direction == 'left':
            globals.run = False
    else:
        globals.section = 0
        globals.run = True
    sleep(0.1)
    globals.direction = None





def show_message_break(message, color, speed):

    """Start a parallel thread displaying a message to continue the main script

    Args:
        message (str) : message to display
        color (list or tuple) : rgb color code
        speed (float) : speed of scrolling message

    """

    def sense_message(message, color, speed):
        while True:
                sense.show_message(message, text_colour = color, scroll_speed = speed)

    if not is_alive(globals.show_process):
        globals.show_process = Process(target = sense_message, args=(message, color, speed,))
        globals.show_process.start()



def loading(color):

    """Hourglass animation

    Args:
        color (list or tuple) : rgb color code

    """
    O = [0,0,0]
    X = color
    S = [255,255,224]
    n = [0,0,0]

    timer = [X, X, X, X, X, X, X, X,
            O, X, S, S, S, S, X, O,
            O, O, X, S, S, X, O, O,
            O, O, O, X, X, O, O, O,
            O, O, O, X, X, O, O, O,
            O, O, X, O, O, X, O, O,
            O, X, O, O, O, O, X, O,
            X, X, X, X, X, X, X, X
            ]

    sense.set_pixels(timer)

    while True:
        sleep(0.5)
        sense.set_pixel(2, 1, n)
        sleep(0.1)
        sense.set_pixel(4, 5, S)
        sleep(0.1)
        sense.set_pixel(4, 5, n)
        sense.set_pixel(4, 6, S)

        sleep(0.5)
        sense.set_pixel(4, 1, n)
        sleep(0.1)
        sense.set_pixel(3, 5, S)
        sleep(0.1)
        sense.set_pixel(3, 5, n)
        sense.set_pixel(3, 6, S)

        sleep(0.5)
        sense.set_pixel(3, 1, n)
        sleep(0.1)
        sense.set_pixel(4, 5, S)
        sleep(0.1)
        sense.set_pixel(4, 5, n)
        sense.set_pixel(5, 6, S)

        sleep(0.5)
        sense.set_pixel(5, 1, n)
        sleep(0.1)
        sense.set_pixel(3, 5, S)
        sleep(0.1)
        sense.set_pixel(3, 5, n)
        sense.set_pixel(2, 6, S)

        sleep(0.5)
        sense.set_pixel(3, 2, n)
        sleep(0.1)
        sense.set_pixel(4, 5, S)

        sleep(0.5)
        sense.set_pixel(4, 2, n)
        sleep(0.1)
        sense.set_pixel(3, 5, S)

        sleep(0.5)
        sense.set_rotation(90)
        sleep(0.3)
        sense.clear()
        sense.set_rotation(0)
        sense.set_pixels(timer)








def askmessage(color, speed):

    """Ask numbers to user

    Args:
        color (list or tuple) : rgb color code
        speed (float) : speed of scrolling message

    Returns:
        str : numbers list
    """

    number = 0
    list_number = []
    run = True
    while run:

        while globals.direction != 'middle':
            sense.show_letter(str(number), text_colour = color)
            get_joystick()
            if globals.direction == 'down':
                passed()
                if number == 'Y':
                    number = 0
                elif number >= 9:
                    number = 'Y'
                else:
                    number += 1
            elif globals.direction == 'up':
                passed()
                if number == 'Y':
                    number = 9
                elif number <= 0:
                    number = 'Y'
                else:
                    number -= 1
        passed()
        if number == 'Y':
            if len(list_number) == 0:
                while globals.direction != 'middle':
                    show_message_break('Incorrect, retry', color, speed)
                    get_joystick()
                passed()
            else:
                run = False
        else:
            list_number.append(number)
        sense.clear()
        sleep(0.01)
    passed()        #number = 0
    return str(list_number)




def yes_no(color):

    """Ask confirmation to user

    Args:
        color (list or tuple) : rgb color code

    Returns:
        bool : True if yes, False if no
    """

    confirmation_letter = 'Y'
    confirmation = True
    while (globals.direction != 'middle' ):
        sense.show_letter(confirmation_letter, text_colour = color)
        get_joystick()
        if globals.direction == 'down':
            passed()
            if confirmation_letter == 'N':
                confirmation_letter = 'Y'
                confirmation = True
            else:
                confirmation_letter = 'N'
                confirmation = False

        elif globals.direction == 'up':
            passed()
            if confirmation_letter == 'N':
                confirmation_letter = 'Y'
                confirmation = True
            else:
                confirmation_letter = 'N'
                confirmation = False
    passed()
    return confirmation




def askpassword(color1, color2, speed):

    """Get compass, gyro and accelerometer data to calculate Secret Hat positon,
        wait for joystick direction left,
        save the pitch, yaw, roll data in list

    Args:
        color1 (list or tuple) : rgb color code for title
        color2 (list or tuple) : rgb color code for subtitle
        speed (float) : speed of scrolling message

    Returns:
        str : matrix of positions

    Exceptions:
        None : if length of matrix is equal to 0, to not set password

    """

    # Use compass, gyro and accelerometer
    sense.set_imu_config(False, False, True)


    def accelerometer(color):
        timeout = 5
        timeout_start = time()
        loading_process = Process(target = loading, args = (color2,))
        loading_process.start()

        # Wait 5 second to calibrate
        while time() < timeout_start + timeout:
            orientation = sense.get_orientation_degrees()
        loading_process.terminate()

        if orientation['pitch'] > 0 and orientation['pitch'] < 15:
           orientation['pitch'] = 360
        if orientation['yaw'] > 0 and orientation['yaw'] < 15:
            orientation['yaw'] = 360
        if orientation['roll'] > 0 and orientation['roll'] < 15:
            orientation['roll'] = 360

        print(orientation)
        # Floor to not be too precise, var precise may be modified in config.ini
        config.read('config.ini')
        try:
            precise = int(config['other']['password_precision'])
        except:
            try:
                config.remove_option('other', 'password_precision')
            except:
                config.add_section('other')
            config.set('other', 'password_precision', '50')
            with open('./config.ini', 'w') as configfile:
                config.write(configfile)
        precise = int(config['other']['password_precision'])
        x = floor(orientation['pitch']/precise)
        y = floor(orientation['roll']/precise)
        z = floor(orientation['yaw']/precise)
        print(x,y,z)
        return x, y, z

    directions = []
    while (globals.direction != 'middle' ):
         show_message_break("Password? ", color2, speed)
         get_joystick()
    passed()
    while (globals.direction != 'middle' ):
         show_message_break("Turn your SecretHat and press ok to save a position. To finish or disabled password, press right", color2, speed)
         get_joystick()
    passed()

    while True:
        while globals.direction != 'middle' and globals.direction != 'right':
            show_message_break("Position? ", [26, 0 , 255], speed)
            get_joystick()
        if globals.direction == "middle":
            passed()
            x, y, z = accelerometer(color2)
            while globals.direction != 'middle' and globals.direction != 'left':
                show_message_break('{},{},{}?'.format(x,y,z), color2, speed)
                get_joystick()
            if globals.direction == 'middle':
                directions.append([x,y,z])
            passed()
        elif globals.direction == "right":
             passed()
             if len(directions) == 0:
                 return None
             else:
                 return str(directions)
