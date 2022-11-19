import PySimpleGUI as sg # pip install PySimpleGUI
from keyboard_sim_Dict_done import keyboard_simulation
#from pynput.keyboard import Key, Controller
import time

#special_char_dict={'~': '`', '!': '1', '@': '2', '#': '3', '$': '4', '%': '5', '^': '6', '&': '7', '*': '8', '(': '9', ')': '0', '_': '-', '+': '=', '}': ']', '{': '[', '"': "'", ':': ';', '?': '/', '>': '.', '<': ',', '|': '\\'}
#keyboard = Controller()
# Define the window's contents
layout = [[sg.Text("Insert the text you want to copy")],
          [sg.Input(key='-INPUT-')],
          [sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Button('Copy'), sg.Button('Quit')]]

# Create the window
window = sg.Window('Keybord simulator', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    window['-OUTPUT-'].update("Please place the cursor where you want to copy")
    #print(f"event : {event} ,Values : {values}")
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    # Output a message to the window
    #window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")
    

    word= values['-INPUT-']
    keyboard_simulation(word)
# Finish up by removing from the screen
window.close()
