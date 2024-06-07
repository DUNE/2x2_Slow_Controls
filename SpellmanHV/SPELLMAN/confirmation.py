# Ask for confirmation before executed important Spellman Controls.
# DeMario Ross 6/4/2024

import subprocess

def ask_confirmation(command):
    while True:

        if command[1] == 'Enable':
            answer = input("Are you sure you want to turn the Spellman on? (yes/no) :")

        elif command[1] == 'Disable':
            answer = input("Are you sure you want to turn the Spellman off? (yes/no) :")

        elif command[1] == 'RampTo':
            answer = input("Are you sure you want to Ramp to {} kV? (yes/no) :".format(command[2]))

        if answer.lower() == 'yes':
            if command[1] == 'RampTo':
                print('Now ramping to {} kV.'.format(command[2]))

            elif command[1] == 'Enable':
                print('Now turning Spellman on.')

            elif command[1] == 'Disable':
                print('Now turning Spellman off.')

            return True

        if answer.lower() == 'no':
            print('Operation Aborted')
            return False

        else:
            print('Invalid input. Please enter yes or no. :)')
