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

from bitalino import BITalino

def main():

    # OS Specific Initializations
    clearCmd = "cls||clear"

    if platform.system() == 'Windows':
        clearCmd = "cls"
        print "Using Windows default console size 80x24"
        columns = 80
        rows = 24
    else:
        clearCmd = "clear"
        rows, columns = os.popen('stty size', 'r').read().split()

    # Default MAC Address
    defaultMACAddress = "20:16:12:21:98:56"

    # Parsing Arguments
    if len(sys.argv) == 1:
        print "Run with flag '--help' or '-h' for instructions."
        print "Now using default settings.\n"
        macAddress = defaultMACAddress
        acqChannels = [0, 1, 2, 3, 4, 5]
        samplingRate = 1000
    elif any(s in ["--help", "-h"] for s in sys.argv):
        print "\nThis script connects to a BITalino device via Bluetooth, get readings for 1 min for baseline, then plays a video and records the readings during the video."
        print "\nRun without flags to use default settings.\n"
        print "Flags:\n"
        print "\t-macAddress [MAC Address of the device]"
        print "\t\t If '-macAddress' is not set, default MAC Address " + defaultMACAddress + " will be used.\n"
        print "\t-channels [Comma seperated list of integers from 0 - 5, representing channels]"
        print "\t\t If '-channels' is not set, all channels [0,1,2,3,4,5] will be monitored"
        print "\t\t Example: 0,2,3 to monitor channels A1, A3, A4\n"
        print "\t-samplingRate [Sampling Rate in Hz]"
        print "\t\tIf '-samplingRate' is not set, default sampling rate of 1000 Hz will be used."
        print "\t\tSampling Rate can be 1, 10, 100 or 1000 Hz.\n"
        print "\t --help (-h)"
        print "\t\t Show this screen.\n"
        exit()
    else:
        # -macAddress flag
        try:
            i = sys.argv.index("-macAddress")
            macAddress = sys.argv[i+1]
        except:
            macAddress = defaultMACAddress
            print "No MAC Address set, using default MAC Address: " + macAddress
        # -channels flag
        try:
            i = sys.argv.index("-channels")
            channels = sys.argv[i+1]
            acqChannels = map(int, channels.split(','))
        except:
            acqChannels = [0, 1, 2, 3, 4, 5]
            print "No channels set, monitoring all channels."
        # -samplingRate
        try:
            i = sys.argv.index("-samplingRate")
            samplingRate = int(sys.argv[i+1])
        except:
            samplingRate = 1000
            print "No sampling rate set, using default sampling rate of 1000 Hz."

    # Setting other attributes
    batteryThreshold = 30
    nSamples = 100

    # Connect to BITalino
    print "\nConnecting to BITalino using MAC Address: " + macAddress
    device = BITalino(macAddress)
    print "\nDevice Connected.\n"

    # Set battery threshold
    device.battery(batteryThreshold)

    # Read BITalino version
    print "Device Version:", device.version()

    # Show channels monitored
    print "Monitoring channels: " + str(acqChannels)

    # Show sampling rate
    print "Sampling Rate: " + str(samplingRate) + " Hz."

    # Create Output file
    filename = raw_input("\nHow shall we call your output file?\nInputting an empty string here to use the default filename\n")
    if(filename == ""):
        filename = "PyBitSignals_" + re.sub(':', '', macAddress) + "_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
        print "Using default filename:\n", filename
    outputFile = open(filename, "w")

    # Write a header to output file
    outputFile.write("# This data is acquired using the BITalino Python API.\n")
    outputFile.write("# Note that this is not the same as the output from OpenSignals.\n")
    outputFile.write("# Note that all data written in this file is RAW! (Please read 'RAW' like Gordon Ramsay)\n")
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
    print "Sampling for baseline..."
    while(end - start) < 60:
        sample = device.read(nSamples)
        outputFile.write(matToString(sample))
        end = time.time()
    print "Finished sampling for baseline."

    # Open Video
    print(playVideo('test.mp4'))


def matToString(matrix):
    """
    :param matrix: The matrix to be turned into string
    Returns a string of a matrix row by row, without brackets or commas
    """
    r, c = matrix.shape
    string = ""
    for row in range(0,r):
        for col in range(0,c):
            string = string + str(int(matrix[row,col])) + "\t"
        string += "\n"
    return string


def playVideo(vidFilename):
    """
    :param vidFilename: The filename/location of the video to be played
    Plays a video in a fullscreen using mplayer/vlc
    Returns the exit code of the command
    """
    if(platform.system() == 'Linux'):
        try:
            return subprocess.call(["mplayer","-fs", "test.mp4"])
        except OSError:
            print("mplayer not found")
            try:
                print("Trying with VLC Player")
                return subprocess.call(["vlc", "-f", "test.mp4"])
            except OSError:
                print("VLC Player not found")
                option = raw_input("Would you like to install mplayer? [Y/N]\n")
                if(option == "Y"):
                    # Install mplayer using apt-get
                    print("Installing mplayer using apt-get. Will require password for sudo")
                    subprocess.call(["sudo", "apt-get", "install", "mplayer"])
                print("Exiting...")
                exit()
    else:
        print("Sorry this script currently only supports Linux systems.")
        print("Exiting...")
        exit()


if __name__ == "__main__":
    main()
