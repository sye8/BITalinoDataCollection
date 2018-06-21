"""
License
-------
GNU GENERAL PUBLIC LICENSE v3
2018
Author
------
Sifan Ye
"""

import os
import platform
import sys
import subprocess

import re
import time

import numpy as np

if sys.version_info[0] < 3:
    from bitalino import BITalino
else:
    print("Python Version 3: Using bitalino3X.py")
    from bitalino3X import BITalino

def main():

    if platform.system() != 'Linux':
        print("Sorry, this script currently can only run linux systems.")
        print("Exiting...")
        exit()
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
        samplingRate = 1000
        print("Please type the path to the video here:")
        vidPath = sys.stdin.readline().rstrip()
    elif any(s in ["--help", "-h"] for s in sys.argv):
        print("\nThis script connects to a BITalino device via Bluetooth, get readings for 1 min for baseline, then plays a video and records the readings during the video.")
        print("\nRun without flags to use default settings.\n")
        print("Flags:\n")
        print("\t-macAddress [MAC Address of the device]")
        print("\t\t If '-macAddress' is not set, default MAC Address " + defaultMACAddress + " will be used.\n")
        print("\t-channels [Comma seperated list of integers from 0 - 5, representing channels]")
        print("\t\t If '-channels' is not set, all channels [0,1,2,3,4,5] will be monitored")
        print("\t\t Example: 0,2,3 to monitor channels A1, A3, A4\n")
        print("\t-samplingRate [Sampling Rate in Hz]")
        print("\t\tIf '-samplingRate' is not set, default sampling rate of 1000 Hz will be used.")
        print("\t\tSampling Rate can be 1, 10, 100 or 1000 Hz.\n")
        print("\t-video [Path to video file]")
        print("\t\tIf '-video' flag is not set, the script will ask you for video during execution\n")
        print("\t--output (-o)")
        print("\t\tSets the output filename")
        print("\t\tIf '--output' flag is not set, default output filename 'PyBitSignals_<MAC Address>_<date>_<time>' will be used\n")
        print("\t--help (-h)")
        print("\t\tShow this screen.\n")
        exit()
    else:
        # -macAddress flag
        try:
            i = sys.argv.index("-macAddress")
            macAddress = sys.argv[i+1]
        except:
            macAddress = defaultMACAddress
            print("No MAC Address set, using default MAC Address: " + macAddress)
        # -channels flag
        try:
            i = sys.argv.index("-channels")
            channels = sys.argv[i+1]
            acqChannels = map(int, channels.split(','))
        except:
            acqChannels = [0, 1, 2, 3, 4, 5]
            print("No channels set, monitoring all channels.")
        # -samplingRate flag
        try:
            i = sys.argv.index("-samplingRate")
            samplingRate = int(sys.argv[i+1])
        except:
            samplingRate = 1000
            print("No sampling rate set, using default sampling rate of 1000 Hz.")
        # -video flag
        try:
            i = sys.argv.index("-video")
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
    nSamples = 100

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
    print("Sampling Rate: " + str(samplingRate) + " Hz.")

    # Create Output file
    outputFile = open(filename, "w")

    # Write a header to output file
    outputFile.write("# This data is acquired using the BITalino Python API.\n")
    outputFile.write("# The script that recorded this data is written by Sifan Ye.\n")
    outputFile.write("# Note that this is not the same as the output from OpenSignals.\n")
    outputFile.write("# Note that all data written in this file is RAW! (Read 'RAW' like Gordon Ramsay)\n")
    outputFile.write("# Device MAC Address: " + macAddress + "\n")
    outputFile.write("# Date and time: " + time.strftime("%Y-%m-%d %H-%M-%S") + "\n")
    outputFile.write("# Monitored Channels: " + str(acqChannels) + "\n")
    outputFile.write("# Sampling Rate: " + str(samplingRate) + "\n")
    outputFile.write("# End of header\n")

    # Start Acquisition
    device.start(samplingRate, acqChannels)

    # Sample for baseline: 1 min
    start = time.time()
    end = time.time()
    print("Sampling for baseline...")
    while(end - start) < 60:
        sample = device.read(nSamples)
        outputFile.write(matToString(sample))
        end = time.time()
    print("Finished sampling for baseline.")

    # Open Video and record data
    print("Play video and record data...")
    try:
        vidProc = subprocess.Popen(["mplayer","-fs", vidPath])
        while(vidProc.poll() == None):
            sample = device.read(nSamples)
            outputFile.write(matToString(sample))
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
    print("Data has been saved in " + filename)
    print("Done")


def matToString(matrix):
    """
    :param matrix: The matrix to be turned into string
    Returns a string of a matrix row by row, without brackets or commas
    """
    r, c = matrix.shape
    string = ""
    for row in range(0,r):
        string += str(time.time())
        string += "\t"
        string += str(time.ctime(time.time()))
        string += "\t"
        for col in range(0,c):
            string = string + str(int(matrix[row,col])) + "\t"
        string += "\n"
    return string


if __name__ == "__main__":
    main()
