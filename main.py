import os
import PySimpleGUI as sg
from PIL import Image, ImageTk
import multiprocessing

import DiscordController
import SteamController
import InstragramController

def main():
    print("Starting Main Function!")

    sg.theme('DarkAmber')

    # Load our images
    images = {'discord': Image.open('Images/discord.png'), 'battlenet': Image.open('Images/battlenet.png'),
              'steam': Image.open('Images/steam.png'), 'instragram': Image.open('Images/instagram.png')}

    for key, value in images.items():
        value.thumbnail((50,50))

    layout = [
        [sg.Checkbox('', key='__chk1__', default=False), sg.Image(key='__discord__', size=(2, 2)), sg.Text(text='Status: ', key='__txt1__', size=(50, 1))],
        [sg.Checkbox('', key='__chk2__', default=False), sg.Image(key='__battlenet__', size=(2, 2)), sg.Text(text='Status: ', key='__txt2__')],
        [sg.Checkbox('', key='__chk3__', default=False), sg.Image(key='__steam__', size=(2, 2)), sg.Text(text='Status: ', key='__txt3__', size=(50, 1))],
        [sg.Checkbox('', key='__chk4__', default=False), sg.Image(key='__instagram__', size=(2, 2)),
         sg.Text(text='Status: ', key='__txt4__', size=(50, 1))],
        [sg.Button('Select All'), sg.Button('Unselect All')],
        [sg.Button('Appear Online'), sg.Button('Appear Offline'), sg.Button('Exit')]
    ]

    window = sg.Window('Main Menu', layout, size=(600,600), finalize=True, resizable=True)
    # window.maximize()
    # Add all the icons
    print(sg.theme_text_color())

    window['__discord__'](data=(ImageTk.PhotoImage(images['discord'])))
    window['__battlenet__'](data=(ImageTk.PhotoImage(images['battlenet'])))
    window['__steam__'](data=(ImageTk.PhotoImage(images['steam'])))
    window['__instagram__'](data=(ImageTk.PhotoImage(images['instragram'])))


    checkbox_keys = ['__chk1__', '__chk2__', '__chk3__', '__chk4__']


    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            exit()

        # If the user presses select all
        elif event == 'Select All':
            for each_checkbox in checkbox_keys:
                window[each_checkbox].update(True)

        # And if the user presses unselect all
        elif event == 'Unselect All':
            for each_checkbox in checkbox_keys:
                window[each_checkbox].update(False)

        # Now for the meat and potatoes, if the user selects appear offline
        elif event == 'Appear Offline':

            # First create an empty list to hold all of the selected programs
            true_checkboxes = []

            # Then iterate the checkboxes and find which ones are active
            for each_checkbox in checkbox_keys:
                if values[each_checkbox] is True:
                    true_checkboxes.append(each_checkbox)

            toggle_offline(window, true_checkboxes)

        elif event == 'Appear Online':

            # First create an empty list to hold all of the selected programs
            true_checkboxes = []

            # Then iterate the checkboxes and find which ones are active
            for each_checkbox in checkbox_keys:
                if values[each_checkbox] is True:
                    true_checkboxes.append(each_checkbox)

            toggle_online(window, true_checkboxes)
            

def toggle_offline(window, list_of_programs):

    # Check if Discord was selected
    if '__chk1__' in list_of_programs:
        status = DiscordController.set_offline()
        print(f'Discord Status: {status}')

        # If everything went okay!
        if status == 0:
            window['__txt1__'].update('Status: Offline', text_color='#fdcb52')
        else:
            window['__txt1__'].update('Status: Unable to successfully toggle Offline!', text_color='red')

    # Check if Steam was selected
    if '__chk3__' in list_of_programs:
        status = SteamController.set_offline()

        # If everything went okay!
        if status == 0:
            window['__txt3__'].update('Status: Offline', text_color='#fdcb52')
        else:
            window['__txt3__'].update('Status: Unable to successfully toggle Offline!', text_color='red')

    # Check if Instagram was selected
    if '__chk4__' in list_of_programs:
        status = InstragramController.set_offline()

        # If everything went okay!
        if status == 0:
            window['__txt4__'].update('Status: Offline', text_color='#fdcb52')
        else:
            window['__txt4__'].update('Status: Unable to successfully toggle Offline!', text_color='red')

    return


def toggle_online(window, list_of_programs):

    # Create our manager and our return dictionary
    # manager = multiprocessing.Manager()
    # status_dictionary = manager.dict()

    # Check if Discord was selected
    if '__chk1__' in list_of_programs:
        # process_discord = multiprocessing.Process(target=DiscordController.set_online, args=(status_dictionary,))
        status = DiscordController.set_online()
        print(f'Discord Status: {status}')

        # If everything went okay!
        if status == 0:
            window['__txt1__'].update('Status: Online', text_color='#fdcb52')
        else:
            window['__txt1__'].update('Status: Unable to successfully toggle Online!', text_color='red')

    # Check if Steam was selected
    if '__chk3__' in list_of_programs:
        status = SteamController.set_online()

        # If everything went okay!
        if status == 0:
            window['__txt3__'].update('Status: Online', text_color='#fdcb52')
        else:
            window['__txt3__'].update('Status: Unable to successfully toggle Online!', text_color='red')

    # Check if Instagram was selected
    if '__chk4__' in list_of_programs:
        status = InstragramController.set_online()

        # If everything went okay!
        if status == 0:
            window['__txt4__'].update('Status: Online', text_color='#fdcb52')
        else:
            window['__txt4__'].update('Status: Unable to successfully toggle Online!', text_color='red')


if __name__ == '__main__':
    main()