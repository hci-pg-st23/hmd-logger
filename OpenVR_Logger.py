import os
import pandas as pd
import pathlib
import time
import triad_openvr

### Config ###
# Set how often the positions are logged per second
interval = 1 / 1000
##############

logging = False

data = {}
df = pd.DataFrame()

marker = 0
repetition = 0

txtData = []

v = triad_openvr.triad_openvr()


# First call this function to initialize the logger
def initLogger(participantID: int, condition: bool):
    global PATH
    global df
    global repetition
    PATH = str(pathlib.Path(__file__).parent.resolve())
    PATH += "/Logs/P_"
    PATH += str(participantID)
    PATH += "-" + condition
    PATH += "-Repetition_0.tsv"
    while os.path.exists(PATH):
        repetition += 1
        if repetition > 10:
            PATH = PATH[:-6]
        else:
            PATH = PATH[:-5]
        PATH += str(repetition)
        PATH += ".tsv"

    found_controllers = 0
    data["unixtime"] = []
    for device in v.devices:
        data[str(device + "_X")] = []
        data[str(device + "_Y")] = []
        data[str(device + "_Z")] = []
        data[str(device + "_Q_W")] = []
        data[str(device + "_Q_X")] = []
        data[str(device + "_Q_Y")] = []
        data[str(device + "_Q_Z")] = []
        if device.startswith("controller"):
            found_controllers += 1
            data[str(device + "_grip")] = []
            data[str(device + "_trigger")] = []
    if found_controllers != 2:
        raise RuntimeError("Missing controllers!")
    data["marker"] = []
    assert len(df.columns) != 27
    df = pd.DataFrame(data)
    df.to_csv(PATH, index=False, sep="\t")


# Call this function to start logging
def startLogger():
    global df

    while logging:
        start = time.time()
        data["unixtime"] = [start]

        for device in v.devices:
            if device.startswith("controller"):
                # Log the grip and trigger buttons of the controller
                key_inputs = v.devices[device].get_controller_inputs()
                data[str(device + "_grip")] = [1 if key_inputs["grip_button"] else 0]
                data[str(device + "_trigger")] = [key_inputs["trigger"]]

            # Log the 3D positon and quaternions for each device
            for value in v.devices[device].get_pose_quaternion():
                txtData.append(value)
            data[str(device + "_X")] = [txtData[-7]]
            data[str(device + "_Y")] = [txtData[-6]]
            data[str(device + "_Z")] = [txtData[-5]]
            data[str(device + "_Q_W")] = [txtData[-4]]
            data[str(device + "_Q_X")] = [txtData[-3]]
            data[str(device + "_Q_Y")] = [txtData[-2]]
            data[str(device + "_Q_Z")] = [txtData[-1]]
            data["marker"] = [marker]

        df = pd.DataFrame(data)
        df.to_csv(PATH, index=False, sep="\t", header=False, mode="a")
        txtData.clear()

        sleep_time = interval - (time.time() - start)
        if sleep_time > 0:
            time.sleep(sleep_time)
