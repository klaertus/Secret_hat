from lib.init import *
from lib import globals

import os



def main(color1, color2, speed):

# https://docs.dataplicity.com/docs/uninstalling
    passed()
    while globals.run:

        while (globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left'): #and globals.section == 0:
            show_message_break("1:Start/Stop", color1, speed)
            get_joystick()
            if globals.direction == 'middle':
                passed()
                if os.path.isfile('/etc/supervisor/conf.d/tuxtunnel.conf'):
                    if os.system('systemctl is-active supervisor') == 0:
                        os.system('service supervisor stop')
                        os.system('systemctl disable supervisor')
                        while globals.direction != 'middle':
                            show_message_break("Dataplicity stopped! Press ok", color2, speed)
                            get_joystick()
                        passed()
                    else:
                        os.system('service supervisor start')
                        os.system('systemctl enable supervisor')
                        while globals.direction != 'middle':
                            show_message_break("Dataplicity started! Press ok", color2, speed)
                            get_joystick()
                        passed()
                else:
                    while globals.direction != 'middle':
                        show_message_break("Dataplicity not configured! Press ok", color2, speed)
                        get_joystick()
                    passed()
        passed(0)

        #while (globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left') and globals.section == 1:
        #    show_message_break("2:Uninstall", color1, speed)
        #    get_joystick()
        #    while globals.direction != 'middle':
        #        show_message_break("This action requires a reboot! Continue?", color2, speed)
        #        get_joystick()
        #    passed()
        #    if globals.direction == 'middle':
        #        passed()
        #        if yes_no(color2):
        #            os.system('rm -r -f /opt/dataplicity')
        #            os.system('rm -r -f /etc/supervisor')
        #            os.system('rm -f /etc/supervisor/conf.d/tuxtunnel.conf')
        #            while (globals.direction != 'middle' ):
        #                show_message_break("Dataplicity uninstalled! System will reboot now! Press ok", color2, speed)
        #                get_joystick()
        #            passed()
        #            os.system('reboot')

        #passed(1)

    passed()
