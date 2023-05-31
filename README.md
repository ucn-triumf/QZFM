# QuSpin Zero Field Magnetometer DAQ

<img src="https://img.shields.io/pypi/v/QZFM?style=flat-square"/> <img src="https://img.shields.io/pypi/format/QZFM?style=flat-square"/> <img src="https://img.shields.io/github/languages/top/ucn-triumf/QZFM?style=flat-square"/> <img src="https://img.shields.io/github/languages/code-size/ucn-triumf/QZFM?style=flat-square"/> <img src="https://img.shields.io/pypi/l/QZFM?style=flat-square"/> <img src="https://img.shields.io/github/last-commit/ucn-triumf/QZFM?style=flat-square"/>

Read and control QuSpin magnetometer (unofficial)

Uses [QZFM commands] to send/receive signals via the [pySerial](https://pyserial.readthedocs.io/) module. See also [this guide](https://quspin.com/products-qzfm-gen2-arxiv/qzfm-quick-start-guide/) for more info on setup for the QuSpin.

This has been tested on the QuSpin Triaxial sensor.

---
## Installation

Install is accomplished with [`pip`](https://pypi.org/project/QZFM/):

```
pip install --user QZFM
```

If you wish to install from source, clone this repository then do

```
cd path/QZFM
pip install --user -e .
```

---
## [See API documentation here.](./docs/src/QZFM.md)

Documentation generated with [`handsdown`](https://github.com/vemel/handsdown)

---

## Debugging Issues

Known issues with connecting to QuSpin:

### 1. Lacking permissions to access USB device [LINUX]

If your user lacks permissions to read/write from the USB device follow the below:

```bash
# check which group can use the USB device
# in the below example, we need to make sure the user is a part of the group "dialout"
$ ls -l /dev | grep USB
crw-rw----   1 root      dialout 188,   0 May 30 18:18 ttyUSB0

# check which users are in the group dialout
$ getent group dialout
dialout:x:20:dfujimoto

# if your user is listed above, then you have a different problem. If not then add your user to the group
$ sudo usermod -a -G dialout yourusername

# then logout to have the changes take effect
```

### 2. Cannot find device

If one cannot find the device you can look at the list of available ports and devices using the following python script:

```python
from serial.tools import list_ports

for port in list_ports.comports():
    print(port)
```

On linux you should see something like `ttyUSB0` listed next to a device which has the QuSpin ID (i.e. something like `Z3T0`). Update your connection string as needed.

In windows you're likely to see something like `COM3` or `COM5`. Use the relevant `COM` device as the connection string.

[QZFM commands]:https://quspin.com/products-qzfm-gen2-arxiv/qzfm-command-list/

