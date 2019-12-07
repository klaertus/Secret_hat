from sense_hat import SenseHat
from .lib.init import show_message_break, passed, get_joystick, loading, askmessage, askpassword, yes_no
from .lib import globals
from .lib.encrypt import encode, decode, verify_pass


from configparser import ConfigParser
from multiprocessing import Process
from time import sleep

"""
Encrypt messages with position data
"""

sense = SenseHat()
config = ConfigParser()


# Read configuration, create it if doesn't exist
try:
    config.read('apps/messages.ini')
except:
    file = open('apps/messages.ini', 'w+')
    file.close()
    config.read('apps/messages.ini')



def main(color1, color2, speed):

    """
    Args :
        color1 (list or tuple) : rgb color code of titles
        color2 (list or tuple) : rgb color code of subtitles
        speed (float) : speed of the scrolling of message
    """

    passed()

    while globals.run:      # Application menu

        # Create new message
        while (globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left') and globals.section == 0:             # Section 1
            show_message_break("1:New message", color1,  speed)
            get_joystick()
            if globals.direction == 'middle' :
                passed()

                # Create new message
                while (globals.direction != 'middle' ):             # Ask message
                    show_message_break("Message?", color2, speed)
                    get_joystick()
                passed()
                message = askmessage(color2, speed)
                passed()

                clear_password = askpassword(color1, color2, speed)             # Ask password
                while clear_password != askpassword(color1, color2, speed):
                    show_message_break("Reenter password", color2, speed)
                    get_joystick()
                passed()

                if not clear_password == None:
                    while globals.direction != 'middle' :               # Ask number of tries
                        show_message_break("Tries(0 to disabled)?", color2, speed)
                        get_joystick()
                    passed()
                    tries = askmessage(color2, speed)
                    tries = int(tries.replace('[', '').replace(']', '').replace(',', '').replace(' ', ''))
                    if tries == 0:
                        tries = -99             # Set to -99 for ignore tries when the password is asked
                    passed()
                else:
                    tries = -99

                while (globals.direction != 'middle' ):             # Ask slot number
                    show_message_break("Slot number?", color2, speed)
                    get_joystick()
                passed()
                slot_number = askmessage(color2, speed)
                while (slot_number.replace('[', '').replace(']', '').replace(',', '').replace(' ', '') in str(config.sections()).replace('[', '').replace(']', '').replace('message', '')):             # If slot already exists, reask
                    while (globals.direction != 'middle' ):
                        show_message_break("Please enter a number", color2, speed)
                        get_joystick()
                    passed()
                    slot_number = askmessage(color2, speed)
                slot_number = int(slot_number.replace('[', '').replace(']', '').replace(',', '').replace(' ', ''))


                while (globals.direction != 'middle' ):             # Global informations of message before save it
                    show_message_break("Infos:", color1, speed)
                    get_joystick()
                passed()

                while (globals.direction != 'middle' ):
                    show_message_break("message:{}".format(message.replace('[', '').replace(']', '').replace(' ', '')), color2, speed)
                    get_joystick()
                passed()

                if tries == -99:
                    show = 'none'
                else:
                    show = tries
                while (globals.direction != 'middle' ):
                    show_message_break("tries:{}".format(show), color2, speed)
                    get_joystick()
                passed()

                while (globals.direction != 'middle' ):
                    show_message_break("slot:{}".format(slot_number), color2, speed)
                    get_joystick()
                passed()

                while globals.direction != 'middle' :   	           # Ask for user confirmation
                    show_message_break("Confirmation?", color1, speed)
                    get_joystick()
                passed()

                if yes_no(color2):
                    config.add_section('message{}'.format(slot_number))

                    # Save the configuration
                    if clear_password == None:
                        config.set('message{}'.format(slot_number), 'password_hash', '0')
                        config.set('message{}'.format(slot_number), 'message', message)
                    else:
                        loading_process = Process(target = loading, args = (color1,))
                        loading_process.start()
                        encrypt_all = encode(clear_password, message)
                        remaining_tries = tries
                        config.set('message{}'.format(slot_number), 'password_hash', str(encrypt_all.split("|")[1]))
                        config.set('message{}'.format(slot_number), 'message', str(encrypt_all.split("|")[0]))
                        config.set('message{}'.format(slot_number), 'tries', str(tries))
                        config.set('message{}'.format(slot_number), 'remaining_tries', str(remaining_tries))
                        config.set('message{}'.format(slot_number), 'encrypt_random_a', str(encrypt_all.split("|")[2]))
                        config.set('message{}'.format(slot_number), 'encrypt_random_b', str(encrypt_all.split("|")[3]))
                        loading_process.terminate()

                    with open('apps/messages.ini', 'w') as configfile:
                        config.write(configfile)

                    while (globals.direction != 'middle' ):
                        show_message_break("Saved! Press ok", color2, speed)
                        get_joystick()
                    passed()

                else:
                    # Ignore if cancelled
                    while (globals.direction != 'middle' ):
                        show_message_break("Cancelled! Press ok", color2, speed)
                        get_joystick()
                    passed()
        passed(1)

        # Display existing messages
        while (globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left') and globals.section == 1:
            show_message_break("2:Messages", color1,  speed)
            get_joystick()
            if globals.direction == 'middle' :
                passed()
                # Check if there are messages in messages.ini
                try:
                        msg_number = int(config.sections()[globals.section].replace('message', ''))
                        globals.run = True
                except:
                        while (globals.direction != 'middle' ):
                            show_message_break("No message! Press ok", color2, speed)
                            get_joystick()
                        passed()
                        globals.run = False

                # Submenu of the messages
                while globals.run:

                    while (globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left'):
                        msg_number = int(config.sections()[globals.section].replace('message', ''))
                        show_message_break("{}:Message".format(msg_number), color2, speed)              # Display the slot number
                        get_joystick()
                        if globals.direction == 'middle' :
                            passed()
                            # Check password's hash
                            try:
                                password_hash = config['message{}'.format(msg_number)]['password_hash']
                            except:
                                while globals.direction != 'middle' :
                                    show_message_break("Error in messages.ini!", color2, speed)
                                    get_joystick()
                                passed()
                                while globals.direction != 'middle' :
                                    show_message_break("Would you like to delete?", color2, speed)
                                    get_joystick()
                                if yes_no(color2):
                                    config.remove_section('message{}'.format(msg_number))
                                    with open('apps/messages.ini', 'w') as configfile:
                                        config.write(configfile)
                                    while globals.direction != 'middle' :
                                        show_message_break("Deleted! Press ok", color2, speed)
                                        get_joystick()
                                    passed()
                                passed()

                            if password_hash != '0':                # If password exist
                                # Check configuration
                                try:
                                    encrypt_random_a = config['message{}'.format(msg_number)]['encrypt_random_a']
                                    encrypt_random_b = config['message{}'.format(msg_number)]['encrypt_random_b']
                                    encrypt_message = config['message{}'.format(msg_number)]['message']
                                    tries = int(config['message{}'.format(msg_number)]['tries'])
                                    remaining_tries = int(config['message{}'.format(msg_number)]['remaining_tries'])
                                except:
                                    while globals.direction != 'middle' :
                                        show_message_break("Error in messages.ini! Press ok", color2, speed)
                                        get_joystick()
                                    passed()
                                    break

                                # Ask the password
                                password = askpassword(color1, color2, speed)
                                loading_process = Process(target = loading, args = (color1,))
                                loading_process.start()
                                verify = verify_pass(password, password_hash, encrypt_random_a, encrypt_random_b)

                            else:           # If no password set up
                                verify = True

                            # If the password is incorrect
                            while not verify and globals.direction != 'left':
                                 loading_process.terminate()                # Stop the loading animation

                                 if tries <= -99:               # If no tries set up
                                     show_message_break("Incorrect", color2, speed)
                                 elif remaining_tries > 0:
                                     remaining_tries -= 1
                                     show_message_break("Incorrect, {} tries left".format(remaining_tries), color2, speed)              # Display tries left
                                     config.set('message{}'.format(msg_number), 'remaining_tries', str(remaining_tries))
                                     with open('apps/messages.ini', 'w') as configfile:
                                         config.write(configfile)
                                 else:              # If there are no tries left, delete the message
                                     config.remove_section('message{}'.format(msg_number))
                                     with open('apps/messages.ini', 'w') as configfile:
                                         config.write(configfile)
                                     globals.run = False
                                     while globals.direction != 'middle' :
                                         show_message_break("No tries left. Deleted. Press ok".format(remaining_tries), color2, speed)
                                         get_joystick()
                                     passed()
                                     break
                                 get_joystick()

                                 if globals.direction == 'middle'  and (remaining_tries > 0 or tries <= -99):               # Reask password
                                     passed()
                                     password = askpassword(color1, color2, speed)
                                     print(password)
                                     lloading_process = Process(target = loading, args = (color1,))
                                     loading_process.start()
                                     verify = verify_pass(password, password_hash, encrypt_random_a, encrypt_random_b)
                            passed()


                            if verify:              # If the password is correct
                                try:
                                    config.set('message{}'.format(msg_number), 'remaining_tries', str(tries))               # Set remaining tries to default
                                    with open('apps/messages.ini', 'w') as configfile:
                                        config.write(configfile)
                                    message = decode(password, encrypt_message, encrypt_random_a)
                                    loading_process.terminate()
                                except:
                                    message = config['message{}'.format(msg_number)]['message']
                                    tries = None

                                while (globals.direction != 'middle' ):
                                    show_message_break("Passed! Press ok", color2, speed)
                                    get_joystick()
                                passed()

                                # Message submenu
                                while globals.run:


                                    # Display the message
                                    while (globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left') and globals.section == 0:
                                        show_message_break("1:Show", color1, speed)
                                        get_joystick()
                                        if globals.direction == 'middle' :
                                            passed()
                                            while (globals.direction != 'middle' ):
                                                show_message_break(str(message.replace('[', '').replace(']', '').replace(' ', '')), color2, speed)
                                                get_joystick()
                                            passed()
                                    passed(2)

                                    # Delete
                                    while (globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left') and globals.section == 1:
                                        show_message_break("2:Delete", color1, speed)
                                        get_joystick()
                                        if globals.direction == 'middle' :
                                            passed()
                                            config.remove_section('message{}'.format(msg_number))
                                            with open('apps/messages.ini', 'w') as configfile:
                                                config.write(configfile)
                                            while (globals.direction != 'middle' and globals.direction != 'up'):
                                                show_message_break("Deleted!", color2, speed)
                                                get_joystick()
                                            passed()
                                            globls.run = False
                                            break
                                    passed(2)

                                    # Display number of tries, and the slot
                                    while (globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left') and globals.section == 2:
                                        show_message_break("3:Infos", color1, speed)
                                        get_joystick()
                                        if globals.direction == 'middle' :
                                            passed()
                                            while (globals.direction != 'middle' ):
                                                show_message_break("tries:{}".format(tries), color2, speed)
                                                get_joystick()
                                            passed()
                                            while (globals.direction != 'middle' ):
                                                show_message_break("slot:{}".format(msg_number), color2, speed)
                                                get_joystick()
                                            passed()
                                    passed(2)

                                passed()

                    passed(len(config.sections())-1)

                passed()            # Section 2
        passed(1)
    passed()
