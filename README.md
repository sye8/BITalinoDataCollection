# BITalinoDataCollection (Work In Progress)

This script connects to a BITalino device via Bluetooth, get readings for 1 min for baseline, then plays a video and records the readings during the video.

## Dependencies
* [Python >2.7](https://www.python.org/downloads/) or [Anaconda](https://www.continuum.io/downloads)
* Python-Dev `sudo apt-get install python-dev`
* [NumPy](https://pypi.python.org/pypi/numpy)
* [pySerial](https://pypi.python.org/pypi/pyserial)
* [pyBluez](https://pypi.python.org/pypi/PyBluez/) (You would also need to install BlueZ and libbluetooth-dev. Both can be installed using `apt-get`)
* [BitalinoAPI](https://github.com/BITalinoWorld/revolution-python-api) (When running, please place into the same folder as dataCollection.py)

## Flags

Run without flags to use default settings.

* `-macAddress [MAC Address of the device]`

    If '-macAddress' is not set, default MAC Address 20:16:12:21:98:56 will be used.

* `-channels [Comma seperated list of integers from 0 - 5, representing channels]`

    If '-channels' is not set, all channels [0,1,2,3,4,5] will be monitored

    Example: 0,2,3 to monitor channels A1, A3, A4

* `-samplingRate [Sampling Rate in Hz]`

    If '-samplingRate' is not set, default sampling rate of 1000 Hz will be used.
 
    Sampling Rate can be 1, 10, 100 or 1000 Hz.

* `--help (-h)`

    Show instructions.

## Note
**This python script has only been tested on Ubuntu MATE on Raspberry Pi 3 Model B**
