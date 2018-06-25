import platform
import sys

import subprocess
import re
import time
import datetime

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

# Default MAC Address
defaultMACAddress = "20:16:12:21:98:56"

# Parsing Arguments
if len(sys.argv) == 1:
    print("Run with flag '--help' or '-h' for instructions.")
    print("Now using default settings.\n")
    macAddress = defaultMACAddress
    acqChannels = [0, 1, 2, 3, 4, 5]
    samplingRate = 100
    print("Please type the path to the video here:")
    vidPath = sys.stdin.readline().rstrip()
elif any(s in ["--help", "-h"] for s in sys.argv):
    print("\nThis script connects to a BITalino device via Bluetooth, get readings for 1 min for baseline, then plays a video and records the readings during the video.")
    print("\nRun without flags to use default settings.\n")
    print("Flags:\n")
    print("\t--mac-address [MAC Address of the device]")
    print("\t\t If '--mac-address' is not set, default MAC Address " + defaultMACAddress + " will be used.\n")
    print("\t--channels [Comma seperated list of integers from 0 - 5, representing channels]")
    print("\t\t If '--channels' is not set, all channels [0,1,2,3,4,5] will be monitored")
    print("\t\t Example: 0,2,3 to monitor channels A1, A3, A4\n")
    print("\t--sampling-rate [Sampling Rate in Hz]")
    print("\t\tIf '--sampling-rate' is not set, default sampling rate of 100 Hz will be used.")
    print("\t\tSampling Rate can be 1, 10, 100 or 100 Hz.\n")
    print("\t--video [Path to video file]")
    print("\t\tIf '--video' flag is not set, the script will ask you for video during execution\n")
    print("\t--output (-o)")
    print("\t\tSets the output filename")
    print("\t\tIf '--output' flag is not set, default output filename 'PyBitSignals_<MAC Address>_<date>_<time>' will be used\n")
    print("\t--help (-h)")
    print("\t\tShow this screen.\n")
    exit()
else:
    # --mac-address flag
    try:
        i = sys.argv.index("--mac-address")
        macAddress = sys.argv[i+1]
    except:
        macAddress = defaultMACAddress
        print("No MAC Address set, using default MAC Address: " + macAddress)
    # --channels flag
    try:
        i = sys.argv.index("--channels")
        channels = sys.argv[i+1]
        acqChannels = map(int, channels.split(','))
    except:
        acqChannels = [0, 1, 2, 3, 4, 5]
        print("No channels set, monitoring all channels.")
    # --sampling-rate flag
    try:
        i = sys.argv.index("--sampling-rate")
        samplingRate = int(sys.argv[i+1])
    except:
        samplingRate = 100
        print("No sampling rate set, using default sampling rate of 100 Hz.")
    # --video flag
    try:
        i = sys.argv.index("--video")
        vidPath = sys.argv[i+1]
    except:
        print("Please type the path to the video here:")
        vidPath = sys.stdin.readline().rstrip()
    # --output flag
    try:
        i = sys.argv.index("--output")
        filename = sys.argv[i+1]
    except:
        try:
            i = sys.argv.index("-o")
            filename = sys.argv[i+1]
        except:
            filename = "PyBitSignals_" + re.sub(':', '', macAddress) + "_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
            print("Using default filename:\n" + filename)

# Setting other attributes
batteryThreshold = 30

# Connect to BITalino
print("\nConnecting to BITalino using MAC Address: " + macAddress)
device = BITalino(macAddress)
print("\nDevice Connected.\n")

# Set battery threshold
device.battery(batteryThreshold)

# Read BITalino version
print("Device Version: " + str(device.version()))

# Show channels monitored
print("Monitoring channels: " + str(acqChannels))

# Show sampling rate
print("Sampling Rate: " + str(samplingRate) + " Hz.\n")

# Start Acquisition
device.start(samplingRate, acqChannels)

# Sample for baseline: 1 min
outputFile = dc.initOutput(filename, macAddress, acqChannels, samplingRate)
dc.writeOutTimed(outputFile, device, acqChannels, samplingRate, 60)

# Open Video and record data
print("Get video length")
ffprobe = subprocess.Popen(["ffprobe", vidPath],stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
result = str([x for x in ffprobe.stdout.readlines() if "Duration" in x]).split(',')[0].split()
vidDuration = time.strptime(result[2], "%H:%M:%S.%f")
seconds = datetime.timedelta(hours=vidDuration.tm_hour,minutes=vidDuration.tm_min,seconds=vidDuration.tm_sec).total_seconds()+1
print("Video Duration: " + str(seconds))
print("Play video and record data...")
try:
    vidProc = subprocess.Popen(["mplayer","-fs", vidPath])
    vidStartTime = time.time()
    while(vidProc.poll() == None):
        sample = device.read(100)
        outputFile.write(dc.matToString(sample))
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
vidEndTime = time.time()
print("Video finished.\n")
print("Video started at " + str(vidStartTime) + " or in human language: " + str(time.ctime(vidStartTime)))
print("Video ended at " + str(vidEndTime) + " or in human language: " + str(time.ctime(vidEndTime)))
print("Video duration: " + str(vidEndTime - vidStartTime))
print("Data has been saved in " + filename)
print("Done")

device.stop()
device.close()
