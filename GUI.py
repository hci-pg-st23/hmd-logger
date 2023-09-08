import time
import keyboard
import threading
import PySimpleGUI as Sg

import OpenVR_Logger

### Config ###
# Set how many milliseconds the GUI waits before updating again
gui_update_frequency = 100
# Set list of conditions that can be selected and are part of the log filename
conditions = ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4"]
##############

logger = OpenVR_Logger
condition = conditions[0]
participantID = 0
starttime = 0
thread = None
first = False

# Setup GUI layout
layout = [
    [
        Sg.Text("Condition: "),
        Sg.Combo(
            conditions,
            default_value=conditions[0],
            key="combo_condition",
            enable_events=True,
        ),
    ],
    [
        Sg.Text("Please input Participant ID: "),
        Sg.In(size=(25, 1), enable_events=True, key="input_pid"),
        Sg.Button("Confirm", key="button_confirm"),
    ],
    [Sg.Button("Start Logger", key="button_start_logger")],
    [Sg.Text("", key="text_status")],
    [Sg.Text("", key="text_marker")],
    [Sg.Text("", key="text_loggingtime", font=("Arial Bold", 24))],
    [Sg.Text("", key="text_unixtime", font=("Arial Bold", 54))],
]
layout = [
    [Sg.Text(key="-EXPAND-", pad=(0, 0))],  # for vertical centering
    [
        Sg.Text(key="-EXPAND2-", pad=(0, 0)),  # for horizontal centering
        Sg.Column(layout, vertical_alignment="center",
                  justification="center", k="-C-"),
    ],
]

# Setup GUI window
window = Sg.Window(
    title="Logger", layout=layout, margins=(10, 10), resizable=False, finalize=True
)
window["-C-"].expand(True, True, True)
window["-EXPAND-"].expand(True, True, True)
window["-EXPAND2-"].expand(True, False, True)


def changeMarker(num):
    if logger.logging:
        logger.marker = num
        window["text_marker"].update(f"Marker: {logger.marker}")


# Setup keyboard listener
for num in range(10):
    keyboard.add_hotkey(str(num), changeMarker, args=[num])


# Event loop
while True:
    event, values = window.read(gui_update_frequency)
    if event == Sg.WINDOW_CLOSED:
        break

    # Update timestamps
    window["text_unixtime"].update(f"{time.time():.4f}")
    if logger.marker == 7:
        window["text_unixtime"].update(text_color="red")
    else:
        window["text_unixtime"].update(text_color="white")
    if logger.logging:
        window["text_loggingtime"].update(f"{time.time() - starttime:.4f}")

    # Handle events
    if event == "button_confirm":
        if values["input_pid"] == "":
            continue
        participantID = values["input_pid"]
        logger.initLogger(participantID, condition)
        window["text_status"].update(
            f"Participant {participantID} will be logged.")
    if event == "button_start_logger":
        logger.logging = not logger.logging
        if logger.logging:
            window["text_status"].update(
                f"Logging for Participant {participantID} started!"
            )
            window["button_start_logger"].update("Stop Logger")
            starttime = time.time()
            thread = threading.Thread(target=logger.startLogger)
            thread.start()
        else:
            window["text_status"].update(
                f"Logging for Participant {participantID} stopped!"
            )
            window["button_start_logger"].update("Start Logger")
            thread.join()
            starttime = 0
    if event == "combo_condition":
        if logger.logging:
            raise Exception("Cannot change condition while logging is active")
        condition = values["combo_condition"]

window.close()
