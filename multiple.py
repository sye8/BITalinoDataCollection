import platform
import sys

import subprocess
import multiprocessing

import re
import time

import numpy as np

if sys.version_info[0] < 3:
    from bitalino import BITalino
else:
    print("Python Version 3: Using bitalino3X.py")
    from bitalino3X import BITalino

import dataCollection as dc



if platform.system() != 'Linux':
    print("Sorry, this script currently can only run linux systems.")
    print("Exiting...")

# OS Specific Initializations
#clearCmd = "cls||clear"

#if platform.system() == 'Windows':
#    clearCmd = "cls"
#    print("Using Windows default console size 80x24")
#    columns = 80
#    rows = 24
#else:
#    clearCmd = "clear"
#    rows, columns = os.popen('stty size', 'r').read().split()


macAddresses = ["20:16:12:21:98:56", "20:16:12:22:01:29"]

# Setting other attributes
batteryThreshold = 30

# Connecting to the BITalino devices
devices = []
for(addr in macAddresses):
    print("Connecting to " + addr)
    devices.append(BITalino(addr))
    print(addr + " connected.")

# Initializing Devices
for(i in range(len(devices))):
    devices[i].battery(batteryThreshold)
    print(macAddresses[i] + " version: " + str(devices[i].version))
    devices[i].start(samplingRate, acqChannels)

# Sampling for baseline
print("Sampling for baseline...")

