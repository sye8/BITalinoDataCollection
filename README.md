# BITalinoDataCollection

This script connects to a BITalino device via Bluetooth, get readings for 1 min for baseline, then plays a video and records the readings during the video.

*Note that this script currently can only be run on Linux systems*

***Note that apparently the BitalinoAPI is written in Python 2 syntax. So if you only have Python 3, please install Python 2***

## Dependencies
* [Python >2.7](https://www.python.org/downloads/) or [Anaconda](https://www.continuum.io/downloads)
* [NumPy](https://pypi.python.org/pypi/numpy)
* [pySerial](https://pypi.python.org/pypi/pyserial)
* [pyBluez](https://pypi.python.org/pypi/PyBluez/)
* [BitalinoAPI](https://github.com/BITalinoWorld/revolution-python-api) (When running, please place into the same folder as dataCollection.py)

### To install Dependencies:
```sh
sudo apt-get install python python-dev python-pip bluez libbluetooth-dev
sudo pip install numpy pyserial pybluez bitalino
git clone https://github.com/BITalinoWorld/revolution-python-api.git
cd revolution-python-api
sudo python setup.py install
```
*(For pip2.7) Note that if your pip complains about `no module named _internal` or `no module named internal`:*

```sh
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py --force-reinstall
```

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

* `-video [Path to video file]`

    If '-video' flag is not set, the script will ask you for video during execution

* `--help (-h)`

    Show instructions.

## Note
**This python script has only been tested on Ubuntu MATE on Raspberry Pi 3 Model B**
