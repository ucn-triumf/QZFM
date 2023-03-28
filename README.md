# QuSpin Zero Field Magnetometer DAQ

<img src="https://img.shields.io/pypi/v/QZFM?style=flat-square"/> <img src="https://img.shields.io/pypi/format/QZFM?style=flat-square"/> <img src="https://img.shields.io/github/languages/top/ucn-triumf/QZFM?style=flat-square"/> <img src="https://img.shields.io/github/languages/code-size/ucn-triumf/QZFM?style=flat-square"/> <img src="https://img.shields.io/pypi/l/QZFM?style=flat-square"/> <img src="https://img.shields.io/github/last-commit/ucn-triumf/QZFM?style=flat-square"/> 

Read and control QuSpin magnetometer (unofficial)

Uses [QZFM commands] to send/receive signals via the [pySerial](https://pyserial.readthedocs.io/) module. See also [this guide](https://quspin.com/products-qzfm-gen2-arxiv/qzfm-quick-start-guide/) for more info on setup for the QuSpin.

This has been tested on the QuSpin Triaxial sensor. 

## Installation

Install can be done via [pip](https://pypi.org/project/QZFM/):

```
pip install --user QZFM
```

It is helpful to also have [tkinter](https://docs.python.org/3/library/tkinter.html) installed on your machine as well. 

## Getting Started

This quick guide follows the QuSpin quick start guide on their [webpage](https://quspin.com/products-qzfm-gen2-arxiv/qzfm-quick-start-guide/)

1. With the QuSpin off, connect all hardware: connect signal cable to electronics box, and the box to a computer via USB
2. Turn QuSpin on 
3. The start procedure is as follows, in the python interpreter:

```python
from QZFM import QZFM

# Get port for connection
# On linux connect via searching for Z3T0 or similar
# On windows you're looking for COM3 or similar
from serial.tools import list_ports
for p in list_ports.comports():
    print(p)
    
# or search for a port
list_ports.grep('some string')

# if you know the port name already, make object and connect:
q = QZFM('Z3T0')

# auto start: wait until laser is locked, temperature is stable
# QZFM object will by default block further execution until these conditions are met
q.auto_start()

# zero the field: the QuSpin will automatically adjust its internal coils to zero the field about the measurement cell
# this procedure will continue until you disable it. 
q.field_zero()

# Monitor progress with the analog output or, as below, digitally
# Wait until fields and temperatures are stable to a few pT. There may be some persistant oscillations
# Use ctrl-C to exit monitor
q.monitor_status()

# Exit the zeroing procedure
q.field_zero(False)

# Do a calibration
# The resulting message tells you if it was successful. 
# From their website: "Calibration values above 1.5 indicate sub-optimal sensor performance, 
# either due to large background field (> 50 nT), or a possible sensor issue."
q.calibrate()

# We are now ready to take data
q.read_data()
q.draw_data()

# We can also livestream the data to a window
q.monitor_data()
```

See below for full API description. 

## Module QZFM API

`QZFM(device_name=None, nbytes_status=1000)`
:   Low-level control of QuSpin magnetic sensor via QZFM serial commands via USB

    device_name:    str, name of device to look for (connection)
                    for windows this is likely COM3 or COM5
                    for linux, search Z3T0 or similar    
    nbytes_status: serial read chunk size in bytes for status updates

### Class variables

`data_read_rate`
:

`serial_settings`
:

### Instance variables

`axis_mode`:          str, readback mode for daq

`field`:              np.array of magnetic fields (pT)

`gain`:               float, V/nT from setting analog gain

`is_calibrated`:      True if calibration is ok

`is_data_streaming`:  True if data streaming mode   

`is_field_zeroed`:    True if field zeroing is maintained

`is_xyz_zeroing`:     True if field zeroing applied to all axes, else only y and z

`led`:                dict of led status on/off

`messages`:           list of tuples (message, epoch time)

`nbytes_status`:      serial read chunk size in bytes for status updates

`read_axis`:          str, axis for readback

`sensor_par`:         dict of sensor parameter readback values

`ser`:                serial.Serial object for connection

`status_last_updated`:epoch time last updated status (led, sensor_par, messages)

`time`:               np.array of epoch times corresponding to field measurements 

`cell_Tlock`
:

`field_zeroed`
:

`is_master`
:

`laser_locked`
:

`laser_on`
:

### Methods

`auto_start(self, block=True, show=True)`
:   Initiate the automated sensor startup routines
        
    if block, wait until laser is locked and 
    temperature stabilized before unblocking
    
    if show, monitor status

`calibrate(self, show=True)`
:   Calibrate the response (field to voltage) of the magnetometer with an internal signal reference
    
    show: if true, print to screen

`connect(self, device_name)`
:   Connect to the QuSpin
    
    device_name: str, name of device (ex: "Z3T0-AAL9"), or 
                    partial name (ex: "Z3T0")

`disconnect(self)`
:   Disconnect from QuSpin

`draw_data(self)`
:   Draw data to window

`field_reset(self)`
:   Sets the internal coil field values to zero

`field_zero(self, on=True, axes_xyz=True, dBz=inf, dBy=inf, dB0=inf, dT=inf, show=True)`
:   Run field zeroing procedure
    
    if on: 
        Start sensor field zeroing procedure to apply a compensation field using the internal sensor coils to null background fields 
    
    if axes_xyz: Field Zeroing is applied to all three axes (default)
    else:        Field Zeroing is applied only to Y & Z axes
    
    dBz, dBy, dB0:  field step thresholds in pT. 
                    if step is smaller than this, stop zeroing procedure.
                    All conditions must be satisfied for field zero stop
                    Set to inf to disable
    
    dT:             similar to above fields, but for cell temperature
    
    show: if true write diagnostic to stdout

`monitor_cell_T_error(self, window_s=20, figsize=(10, 6))`
:   Continuously stream cell temperature to window
    
    window_s: show the last window_s seconds of data on the stream
    figsize:  size of display
    
    See https://matplotlib.org/stable/tutorials/advanced/blitting.html

`monitor_data(self, axis='z', window_s=10, figsize=(10, 6))`
:   Continuously stream data to window
    
    axis:     axis to read from
    window_s: show the last window_s seconds of data on the stream
    figsize:  size of display
    
    See https://matplotlib.org/stable/tutorials/advanced/blitting.html

`monitor_status(self)`
:   Continuously update and print status

`print_messages(self, last_n=None)`
:   Print messages to screen
    
    last_n: print the last number of messages

`print_state(self)`
:   Print state of the python object

`print_status(self, update=False, overwrite_last=False)`
:   Print status of QuSpin in a nicely formatted message
    
    update: if true, update before printing
    overwrite_last: if true, overwrite the last message. Used in monitor_status

`read_data(self, seconds, axis='z', clear_buffer=True)`
:   Read data from the device 
    
    seconds:        float, duration of measurement npts= seconds*200Hz
    axis:           str, which axis to read from (x, y, or z)
    clear_buffer:   bool, if true, clear buffer and wait for new
    
    assumed readback rate based on comments from QuSpin
    time[0] is the time immediately after clearing the buffer. 
        Note that there is often an incomplete word after clear, we ignore this
        As a result the error in time is at most 1/self.data_read_rate
    
    returns (time, field)

`read_offsets(self, npts, clear_buffer=True)`
:   Read offset data from the device in field zeroing mode 
    
    npts:           int, number of data points to read
    clear_buffer:   bool, if true, clear initial buffer and wait for new
    
    time[0] is the time immediately after clearing the buffer. 
    
    reads at approx 7.5 Hz

`reboot(self)`
:   Reboot the microprocessor and reloads the firmware

`set_axis_mode(self, mode='z')`
:   Change field-sensitive axis
    
    Note: triaxial sensors do not respond to this command
    
    mode =  z       Operate the magnetometer in single Z axis mode
            y       Operate the magnetometer in single Y axis mode
            dual    Operate the magnetometer in dual Y and Z axis mode

`set_gain(self, mode='1x')`
:   Set analog gain (analog output only)
    
    mode =  0.33x   Set the analog output gain to 0.33 times default (0.9 V/nT)
            1x      Set the analog output gain to default (2.7 V/nT)
            3x      Set the analog output gain to 3 times default (8.1 V/nT)

`to_csv(self, filename=None, *notes)`
:   Write data to csv, if no filename, use default
    
    notes: list of things to add to file header

`to_csv_fz(self, filename=None, *notes)`
:   Write field zero data to csv, if no filename, use default
    
    notes: list of things to add to file header

`update_status(self, clear_buffer=True)`
:   Clear input buffer and read status
    
    updates the following attributes: 
        self.status_last_updated
        self.led
        self.sensor_par
        self.messages



[QZFM commands]:https://quspin.com/products-qzfm-gen2-arxiv/qzfm-command-list/
