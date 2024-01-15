# QuSpin Zero Field Magnetometer DAQ

<img src="https://img.shields.io/pypi/v/QZFM?style=flat-square"/> <img src="https://img.shields.io/pypi/format/QZFM?style=flat-square"/> <img src="https://img.shields.io/github/languages/top/ucn-triumf/QZFM?style=flat-square"/> <img src="https://img.shields.io/github/languages/code-size/ucn-triumf/QZFM?style=flat-square"/> <img src="https://img.shields.io/pypi/l/QZFM?style=flat-square"/> <img src="https://img.shields.io/github/last-commit/ucn-triumf/QZFM?style=flat-square"/>

Read and control QuSpin magnetometer (unofficial)

Uses [QZFM commands] to send/receive signals via the [pySerial](https://pyserial.readthedocs.io/) module. See also [this guide](https://quspin.com/products-qzfm-gen2-arxiv/qzfm-quick-start-guide/) for more info on setup for the QuSpin.

This has been tested on the QuSpin Triaxial sensor.

## README Contents

- [QuSpin Zero Field Magnetometer DAQ](#quspin-zero-field-magnetometer-daq)
  - [README Contents](#readme-contents)
  - [Installation](#installation)
    - [Additional setup for LabJack DAQ](#additional-setup-for-labjack-daq)
  - [API documentation](#api-documentation)
  - [Quick Start](#quick-start)
  - [Calibration](#calibration)
  - [Noise Spikes](#noise-spikes)
  - [Digital vs Analog Output](#digital-vs-analog-output)
  - [Debugging Issues](#debugging-issues)
    - [1. Lacking permissions to access USB device \[LINUX\]](#1-lacking-permissions-to-access-usb-device-linux)
    - [2. Cannot find device](#2-cannot-find-device)

---
## Installation

Install is accomplished with [`pip`](https://pypi.org/project/QZFM/):

```
pip install QZFM
```

If you wish to install from source, clone this repository then do

```
cd path/QZFM
pip install -e .
```

### Additional setup for LabJack DAQ

Assumed T7 DAQ device.

1. Install the [LJM software](https://labjack.com/pages/support?doc=%2Fsoftware-driver%2Finstaller-downloads%2Fljm-software-installers-t4-t7-digit%2F)
2. Install the LJM python package: `pip install labjack-ljm`

---
## [API documentation](./docs/src/QZFM.md)

* [QZFM](./docs/src/QZFM/QZFM.md) Module
* [QZFMlj](./docs/src/QZFM/LabJack.md) Module (with labjack DAQ)

Documentation generated with [`handsdown`](https://github.com/vemel/handsdown)

---
## Quick Start

```python
from QZFM import QZFM

# connect to sensor
qu = QZFM('Z3T0')

# start
# this will show the laser and temperature lock status
# the command will also zero and calibrate the device
# further execution is blocked until complete
qu.auto_start()

# we are now ready to start taking data
# all front panel lights on the QuSpin electronics box should be green

# display live data from digital output
qu.monitor_data('z')
```

Note that if you disconnect from the QZFM electronics, the state of the sensor is maintained but the python script won't know the value of the zeroing fields or calibration numbers.

---
## Calibration

From a [forum discussion post with QuSpin](https://groups.google.com/g/qzfm-discussion-board/c/kv2CD-0MdWc), dated 2019:

When you press calibrate, a known magnetic field is momentarily applied with the internal coils to calibrate the magnetometer response. The calibration process yields a calibration number which is multiplied with the raw output in a way that scales the analog output to be 2.7 V/nT (in default mode) and the digital output to be represented in pT.

If the calibration number is small <1, then the magnetometer is relatively healthy, but if the displayed number is high (>1), then there is some problem, most likely residual field or the gradient field too high. The calibration number itself is arbitrary and it is capped at 15.9.

The limit for healthy performance is generally a calibration of about 1.5. If the sensor is in a low ambient magnetic field environment, the calibration factor will be lower than if the internal coils need to cancel out a large ambient field. This is usually the most significant source of large calibration values (over 1.5). Sensors can be at optimal performance with a calibration above 1.0 (lower values are generally better), but around 1.5+ the performance is almost certainly not optimal.

---
## Noise Spikes

From a [forum discussion post with QuSpin](https://groups.google.com/g/qzfm-discussion-board/c/wCxtDgivvRI), dated 2019:

The digital and the analog output is derived from the same source, so the FFT from the analog output should look the same digital output. If you see excess spikes on the analog output, something is not right.

Here are some of the sources of spikes that we or other users have experienced in the past.

1. 77 Hz spike (only seen on the analog output)

    The sinusoidal modulation field on which the QZFM relies for operation is at 923 Hz. After demodulation, we try and filter out residual 923 on the analog output as best as we can, but a tiny bit of 923 Hz modulation signal leaks out on the analog port. If you are sampling the analog output with ADC running at 1kHz (or 500 Hz), then the 1 kHz can alias with 923 Hz producing a 77 Hz spike in the FFT.

    To avoid this problem, we recommend sampling at a minimum of 2 kHz when possible. If sampling at 2 kHz is not an option, we suggest sampling at a frequency slightly higher than 1 kHz (something like 1.1 kHz for example) such that the spike is outside the 0-100 Hz band which is critical for MEG and related applications. 

2. USB Grounding

    If the USB ground is different from the power supply ground, then ground loops can form which an introduce random and sometimes inconsistent spikes. This is a design oversight at our end and we will try to fix this problem in future electronics but for now, the best option is trying to plug the USB cable elsewhere and see if that helps. If you have found some nice tricks to solve the problem, please post here to benefit the rest of the community. To identify USB cable is a source of the noise spikes, do the following: Run field zeroing and calibration, and after that unplug the USB cable and measure the noise spectrum with analog output. If you see spikes that disappear, then USB ground loop is the source of the problem.

---
## Digital vs Analog Output

From a [forum discussion post with QuSpin](https://groups.google.com/g/qzfm-discussion-board/c/apRzBBP-3xU), dated 2019:

If everything is working the way it should be, there will be no difference in the noise floor/SNR using the two data acquisition methods (in-built digital vs. 16-bit analog DAQ). Visually, it is possible for the two signals to look a little different because the digital data seen over USB has a built-in sixth-order low-pass filter at 100 Hz whereas the analog signal is sampled much faster and thus there is a possibility that a noise spike outside the 100 Hz is picked up the DAQ. One can always add a low pass filter to the analog signals and after that, I expect the signals to look more identical.

In addition, to be positively certain DAQ is working correctly, do the following:
1. Send ascii command 51 to the sensor under test (after auto-start, field zeroing, and calibration steps). This will turn off internal modulation signals in the sensor and make it insensitive to external magnetic fields. In this mode, it is easier to distinguish external noise from magnetic noise by making the sensor insensitive to the magnetic field.
2. Now take the FFT with QuSpin user interface. The FFT (power spectral density (psd)) will give you the true noise floor of the sensor in pT/rtHz.
3. Take the FFT (PSD) of the analog output with 16-bit or higher resolution DAQ.

The FFT noise floor with the two methods should match near perfectly in the DC-100 Hz band. Note: FFT with QuSpin interface is in pT/rtHz units but analog FFT is in V/rtHz units. The analog voltage to field conversion in default mode is 2.7 V/nT. Thus, to match the analog FFT with QuSpin interface units, divide the FFT of the analog output by 2.7 (default analog gain mode) and then multiply the result by 1000 to obtain numbers in the same pT/rtHz units.

4. Once your tests are completed, you can run field zeroing to make the sensor function normally again.

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

In bash you could also do

```bash
lsusb
```

On linux you should see something like `ttyUSB0` listed next to a device which has the QuSpin ID (i.e. something like `Z3T0`). Update your connection string as needed.

In windows you're likely to see something like `COM3` or `COM5`. Use the relevant `COM` device as the connection string.

[QZFM commands]:https://quspin.com/products-qzfm-gen2-arxiv/qzfm-command-list/

