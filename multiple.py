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
samplingRate = 100
acqChannels = [0,1,2,3,4,5]
nSamples = 100

# Setting other attributes
batteryThreshold = 30

# Connecting to the BITalino devices
devices = []
for addr in macAddresses :
    print("Connecting to " + addr)
    devices.append(BITalino(addr))
    print(addr + " connected.")

# Initializing Devices
for i in range(len(devices)) :
    devices[i].battery(batteryThreshold)
    print(macAddresses[i] + " version: " + str(devices[i].version()))
    devices[i].start(samplingRate, acqChannels)

# Sampling for baseline
print("The data collected will be stored in PyBitSignals_<MAC Address>_<date>_<time>.txt")
outputFiles = []
processes = []
# Initialize output files, setup processes
for i in range(len(devices)) :
    filename = "PyBitSignals_" + re.sub(':', '', macAddresses[i]) + "_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    outputFile = dc.initOutput(filename, macAddresses[i], acqChannels, samplingRate)
    outputFiles.append(outputFile)
    processes.append(multiprocessing.Process(target=dc.writeOutTimed, args=(outputFile, devices[i], acqChannels, samplingRate, 60)))

# Start baseline sampling for each device
for p in processes:
    p.start()

# Exit the completed processes
for p in processes:
    p.join()

# Open Video and record data
print("Play video and record data...")
try:
    vidProc = subprocess.Popen(["mplayer","-fs", "test.mp4"])
    vidStartTime = time.time()
    processes = []
    for i in range(len(devices)):
        processes.append(multiprocessing.Process(target=dc.writeOut, args=(outputFile, devices[i], acqChannels, samplingRate)))
    while(vidProc.poll() == None):
        for p in processes:
            p.start()
        for p in processes:
            p.join()
except OSError:
    print("mplayer not found")
    print("Would you like to install mplayer? [Y/N]")
    option = sys.stdin.readline().rstrip()
    if(option == "Y"):
        # Install mplayer using apt-get
        print("Installing mplayer using apt-get. Will require password for sudo")
        subprocess.call(["sudo", "apt-get", "install", "mplayer"])
        print("Exiting...")
        exit()
print("Video finished.\n")
print("Video started at " + str(vidStartTime) + " or in human language: " + str(time.ctime(vidStartTime)))
print("Done")

device.stop()
device.close()
