from sense_hat import SenseHat
from lib.init import passed, show_message_break, loading, get_joystick, askmessage, askpassword, is_alive, yes_no
from lib.encrypt import encode, decode, verify_pass
from lib import globals


from configparser import RawConfigParser
from multiprocessing import Process
import os
from time import localtime, sleep
import glob
import ast


sense = SenseHat()

config = RawConfigParser(allow_no_value = True)
config.optionxform = str
config.optionxform = lambda option: option


# It's a shame copy from https://github.com/SteveAmor/Raspberry-Pi-Sense-Hat-Clock/blob/master/clock.py
color1 = [100,0,0]
color2 = [100,100,0]

def clock(color1, color2):
    sense.low_light = True
    number = [
    0,1,1,1, #zero
    0,1,0,1,
    0,1,0,1,
    0,1,1,1,
    0,0,1,0, #one
    0,1,1,0,
    0,0,1,0,
    0,1,1,1,
    0,1,1,1, #two
    0,0,1,1,
    0,1,1,0,
    0,1,1,1,
    0,1,1,1, #three
    0,0,1,1,
    0,0,1,1,
    0,1,1,1,
    0,1,0,1, #four
    0,1,1,1,
    0,0,0,1,
    0,0,0,1,
    0,1,1,1, #five
    0,1,1,0,
    0,0,1,1,
    0,1,1,1,
    0,1,0,0, #six
    0,1,1,1,
    0,1,0,1,
    0,1,1,1,
    0,1,1,1, #seven
    0,0,0,1,
    0,0,1,0,
    0,1,0,0,
    0,1,1,1, #eight
    0,1,1,1,
    0,1,1,1,
    0,1,1,1,
    0,1,1,1, #nine
    0,1,0,1,
    0,1,1,1,
    0,0,0,1
    ]


    hour_color   = color1# red
    minute_color = color2 # cyan
    empty        = [0,0,0] # off / black

    clock_image = [
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0
    ]


    while True:
        hour = localtime().tm_hour
        minute = localtime().tm_min

        # Map digits to the clock_image array
        pixel_offset = 0
        index = 0
        for index_loop in range(0, 4):
            for counter_loop in range(0, 4):
                if (hour >= 10):
                    clock_image[index] = number[int(hour/10)*16+pixel_offset]
                clock_image[index+4] = number[int(hour%10)*16+pixel_offset]
                clock_image[index+32] = number[int(minute/10)*16+pixel_offset]
                clock_image[index+36] = number[int(minute%10)*16+pixel_offset]
                pixel_offset = pixel_offset + 1
                index = index + 1
            index = index + 4

    # Color the hours and minutes
        for index in range(0, 64):
            if (clock_image[index]):
                if index < 32:
                    clock_image[index] = hour_color
                else:
                    clock_image[index] = minute_color
            else:
                clock_image[index] = empty

        # Display the time
        # sense.low_light = True # Optional
        sense.set_pixels(clock_image)
        sleep(1)

        # Display the time


        #sense.low_light = True # Optional
        sense.set_pixels(clock_image)

# End of shame copy


while True:
    error = True
    while error is not None:
        # Initialize configuration

        try:
            config = RawConfigParser(allow_no_value = True)
            config.read('config.ini')
            color1 = ast.literal_eval(config['personalization']['color1'])
            color2 = ast.literal_eval(config['personalization']['color2'])
            speed = float(config['personalization']['speed'])
            brightness = bool(int(config['personalization']['low_light']))

            password_precision = int(config['other']['password_precision'])

            wifi = config['wifi_keys']

            try:
                timer_configuration = RawConfigParser(allow_no_value = True)
                timer_configuration.read('apps/timer.ini')
                time_left = timer_configuration['timer']['time']
                list_gpio = timer_configuration['timer']['gpio']
                shutdown = bool(timer_configuration['timer']['shutdown'])

                try:
                    track_infos = RawConfigParser(allow_no_value = True)
                    track_infos.read('apps/track_infos.ini')
                    update_time = track_infos['logs']['update_time']

                    try:
                        password_config = RawConfigParser(allow_no_value = True)
                        password_config.read('password_config.ini')
                        password_hash = password_config['main_password']['password_hash']
                        print(type(password_hash))
                        print(password_hash)
                        encrypt_random_a = password_config['main_password']['encrypt_random_a']
                        encrypt_random_b = password_config['main_password']['encrypt_random_b']
                        tries = int(password_config['main_password']['tries'])
                        remaining_tries = int(password_config['main_password']['remaining_tries'])
                        reset_mode = int(password_config['main_password']['reset_mode'])
                        error = None

                    except Exception as e:
                        error = e
                        while globals.direction != 'middle' :
                            show_message_break('Error:{}'.format(error), [100,100,100], .05)
                            get_joystick()
                        passed()
                        while globals.direction != 'middle' :
                            show_message_break("Would you like to reset config?", [100,100,100], .05)
                            get_joystick()
                        passed()
                        if yes_no([100,100,100]):
                            os.system('cp backup/password_config.ini.backup password_config.ini')


                except Exception as e:
                    error = e
                    while globals.direction != 'middle' :
                        show_message_break('Error:{}'.format(error), [100,100,100], .05)
                        get_joystick()
                    passed()
                    while globals.direction != 'middle' :
                        show_message_break("Would you like to reset config?", [100,100,100], .05)
                        get_joystick()
                    passed()
                    if yes_no([100,100,100]):
                        os.system('cp backup/track_infos.ini.backup apps/track_infos.ini')

            except Exception as e:
                error = e
                while globals.direction != 'middle' :
                    show_message_break('Error:{}'.format(error), [100,100,100], .05)
                    get_joystick()
                passed()
                while globals.direction != 'middle' :
                    show_message_break("Would you like to reset config?", [100,100,100], .05)
                    get_joystick()
                passed()
                if yes_no([100,100,100]):
                    os.system('cp backup/timer.ini.backup apps/timer.ini')

        except Exception as e:
            error = e
            while globals.direction != 'middle' :
                show_message_break('Error:{}'.format(error), [100,100,100], .05)
                get_joystick()
            passed()
            while globals.direction != 'middle' :
                show_message_break("Would you like to reset config?", [100,100,100], .05)
                get_joystick()
            passed()
            if yes_no([100,100,100]):
                os.system('cp backup/config.ini.backup config.ini')

    # Print clock waiting joystick up
    clock_process = Process(target = clock, args = (color1, color2,))
    clock_process.start()
    while globals.direction != 'left':
        get_joystick()
    passed()
    clock_process.terminate()

    if brightness:
        sense.low_light = True
    else:
        sense.low_light = False

    # Ask password if configured
    print(remaining_tries)
    if remaining_tries is -1:
        while globals.direction != 'middle' :
            show_message_break("Blocked", color2, speed)
            get_joystick()
        passed()
        os.system('halt')

    elif password_hash is not None:
        password = askpassword(color1, color2, speed)
        loading_process = Process(target = loading, args = (color1,))
        loading_process.start()
        verify = verify_pass(password, password_hash, encrypt_random_a, encrypt_random_b)

    else:
        verify = True

    # Reask if incorrect password
    while not verify and globals.direction != 'left':
         loading_process.terminate()
         # Check if there is a maximum number of tries
         if tries == 0:
             show_message_break("Incorrect", color2, speed)
         elif remaining_tries > 0:
             remaining_tries -= 1
             show_message_break("Incorrect, {} tries left".format(remaining_tries), color2, speed)
             password_config.set('main_password', 'remaining_tries', str(remaining_tries))
             with open('password_config.ini', 'w') as configfile:
                 password_config.write(configfile)
         else:                  # If no tries left, apply reset mode
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

         if globals.direction == 'middle'  and (remaining_tries > 0 or tries == 0):
             passed()
             password = askpassword(color1, color2, speed)
             print(password)
             loading_process = Process(target = loading, args = (color1,))
             loading_process.start()
             verify = verify_pass(password, password_hash, encrypt_random_a, encrypt_random_b)
             print(verify, "ok")
    passed()



    # If password is correct
    if verify and globals.run:
        try:
            globals.password = password
        except:
            globals.password = str(0)
        # Reset remaining_tries in password_config file
        config.set('main_password', 'remaining_tries', str(tries))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        try:
            loading_process.terminate()
        except:
            pass

        while (globals.direction != 'middle' ):
            show_message_break("Passed! Press ok", color2, speed)
            get_joystick()
        passed()

        # Read the main menu configuration

        apps = RawConfigParser(allow_no_value = True)
        apps.read('apps/apps_init.ini')
        print(config.options(config.sections()[0]), 12)

        # Main menu
        while globals.run:

                while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left':
                    #print(apps.sections())
                    #app_lib = config['apps']['app{}'.format(globals.section+1)].split(" | ")[0]
                    try:
                        apps.read('apps/apps_init.ini')
                        app_name = apps['apps']['app{}'.format(globals.section+1)].split(" | ")[1]
                        show_message_break("{}:{}".format(globals.section+1, app_name), color1, speed)
                        get_joystick()

                    except Exception as e:
                        print(e)
                        while (globals.direction != 'middle' ):
                            show_message_break("Error in apps_init.ini!", color2, speed)
                            get_joystick()
                        passed()
                        while (globals.direction != 'middle' ):
                            show_message_break("Would you like to reset apps_init.ini?", color2, speed)
                            get_joystick()
                        passed()
                        if yes_no(color2):
                            os.system('cp backup/apps_init.ini.backup apps/apps_init.ini')

                    if globals.direction == 'middle':
                        app_lib = apps['apps']['app{}'.format(globals.section+1)].split(" | ")[0]
                        passed()
                        print(app_lib)
                        exec('from apps.{} import *'.format(app_lib))
                        main(color1, color2, speed)


                passed(len(apps.options(apps.sections()[0]))-1)
        passed()
