# OpenVR Logger GUI

With this application you can track the position of the HMD and both controllers of a VR headset that is connected to the PC via Quest Link and SteamVR.
The tracked positions are saved in a tsv format in the `Logs` folder.
If you press a digit key on the PC keyboard, this is also logged in the tsv files.

- Developed for usage with the Meta Quest 2
- Tested with python 3.11

## Installation

1. Make sure a recent [python](https://www.python.org/downloads/) version, [SteamVR](https://store.steampowered.com/app/250820/SteamVR) and the [Oculus application](https://store.facebook.com/quest/setup/) are installed.
2. Clone this repository and open it.
3. Run `pip install -r requirements.txt`.
4. Download the [`triad_openvr.py`](https://github.com/TriadSemi/triad_openvr/blob/d389aacf2a4caa392398613a9daddba15ee24f92/triad_openvr.py) and move it inside the repository directory.
5. Apply our changes to the `triad_openvr.py` with `git apply triad_openvr.diff`.

## Usage

Run `python3 GUI.py`.
If necessary, adjust the config variable section in `GUI.py` and `OpenVR_Logger.py`.

## Credits

This application was developed for usage in a project group of the [HCI group](https://www.hci.wiwi.uni-due.de/en/) at the University of Duisburg-Essen by:

- Jordan Hoppen
- Patrick Laskowski
- Florian Rademaker
- Leon Sabel

We use a slightly changed version of the `triad_openvr.py` from [triad_openvr](https://github.com/TriadSemi/triad_openvr) to avoid divisions by 0.
