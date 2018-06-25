"""
License
-------
GNU GENERAL PUBLIC LICENSE v3
2018
Author
------
Sifan Ye
"""

import sys

import time

import numpy as np

if sys.version_info[0] < 3:
    from bitalino import BITalino
else:
    print("Python Version 3: Using bitalino3X.py")
    from bitalino3X import BITalino


def initOutput(filename, macAddress, acqChannels, samplingRate):
    """
    :param filename: The path to the output file
    :param macAddress: The MAC Address of the BITalino device, to be written in the header
    :param acqChannels: The monitored analog channels, to be written in the header
    :param samplingRate: The sampling rate in Hz, to be written in the header
    Creates an output file and writes the header
    """
  	# Create Output file
    file = open(filename, "w")
    
    # Write a header to output file
    file.write("# This data is acquired using the BITalino Python API.\n")
    file.write("# The script that recorded this data is written by Sifan Ye.\n")
    file.write("# Note that this is not the same as the output from OpenSignals.\n")
    file.write("# Note that all data written in this file is RAW! (Read 'RAW' like Gordon Ramsay)\n")
    file.write("# Device MAC Address: " + macAddress + "\n")
    file.write("# Date and time: " + time.strftime("%Y-%m-%d %H-%M-%S") + "\n")
    file.write("# Monitored Channels: " + str(acqChannels) + "\n")
    file.write("# Sampling Rate: " + str(samplingRate) + "\n")
    file.write("# End of header\n")
    
    file.flush()

    return file


def writeOutTimed(file, device, acqChannels, samplingRate, t):
    """
    :param filename: The output file object
    :param device: The BITalino device collecting bio-metrics data
    :param acqChannels: The monitored analog channels,in a list
    :param samplingRate: The sampling rate in Hz
    :param time: The sampling time, in seconds
    Collects data from the BITalino device for the given time duration and writes to the designated output file
    Must start the device before calling this
    """
    start = time.time()
    end = time.time()
    print("Sampling for " + str(t) + " seconds...")
    while(end - start) < t:
        sample = device.read(100)
        file.write(matToString(sample))
        end = time.time()
    file.flush()
    print("Finished.")


def matToString(matrix):
    """
    :param matrix: The matrix to be turned into string
    Returns a string of a matrix row by row, without brackets or commas
    Columns from left to right are respectively:
    - Time stamp in UNIX time
    - Time stamp in local time
    - Digital 0 - 3
    - Monitored Analog Channels
    """
    r, c = matrix.shape
    string = ""
    for row in range(0,r):
        string += str(time.time())
        string += "\t"
        string += str(time.ctime(time.time()))
        string += "\t"
        for col in range(1,c):
            string = string + str(int(matrix[row,col])) + "\t"
        string += "\n"
    return string


def videoLength(filename):
    """
    :param filename: The path to the video file
    Returns the length of the video in seconds, rounded up
    """
    ffprobe = subprocess.Popen(["ffprobe", vidPath],stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    result = str([x for x in ffprobe.stdout.readlines() if "Duration" in x]).split(',')[0].split()
    vidDuration = time.strptime(result[2], "%H:%M:%S.%f")
    ereturn datetime.timedelta(hours=vidDuration.tm_hour,minutes=vidDuration.tm_min,seconds=vidDuration.tm_sec).total_seconds()+1
