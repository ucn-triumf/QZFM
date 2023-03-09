# QuSpin DAQ

Read and control QuSpin magnetometer

Uses [QZFM commands] to send/receive signals via the [pySerial](https://pyserial.readthedocs.io/) module. See also [this guide](https://quspin.com/products-qzfm-gen2-arxiv/qzfm-quick-start-guide/) for more info on setup for the QuSpin.

## Contents

`QZFM` : Class for low-level control of the QuSpin. Handles connections and a mapping of the [QZFM commands].

## Usage

Install dependencies: 
   ```bash
   pip install --user -r requirements.txt
   ```

Module QZFM
===========

Classes
-------

`QZFM(nbytes_status=1000)`
:   Low-level control of QuSpin magnetic sensor via QZFM serial commands via USB

Attributes: 

    axis_mode:          str, readback mode for daq
    field:              np.array of magnetic fields (pT)
    gain:               float, V/nT from setting analog gain
    is_calibrated:      True if calibration is ok
    is_data_streaming:  True if data streaming mode   
    is_field_zeroed:    True if field zeroing is maintained
    is_xyz_zeroing:     True if field zeroing applied to all axes, else only y and z
    led:                dict of led status on/off
    messages:           list of tuples (message, epoch time)
    nbytes_status:      serial read chunk size in bytes for status updates
    sensor_par:         dict of sensor parameter readback values
    ser:                serial.Serial object for connection
    status_last_updated:epoch time last updated status (led, sensor_par, messages)
    time:               np.array of epoch times corresponding to field measurements 

nbytes_status: serial read chunk size in bytes for status updates

### Class variables

`data_read_rate`
:

`serial_settings`
:

### Instance variables

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

`auto_start(self, block=True)`
:   Initiate the automated sensor startup routines
      
    if block, wait until laser is locked and 
    temperature stabilized before unblocking

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

`field_zero(self, on=True, axes_xyz=True, dBz=inf, dBy=inf, dB0=inf, show=True)`
:   Run field zeroing procedure
    
    if on: 
        Start sensor field zeroing procedure to apply a compensation field using the internal sensor coils to null background fields 
    
    if axes_xyz: Field Zeroing is applied to all three axes (default)
    else:        Field Zeroing is applied only to Y & Z axes
    
    dBz, dBy, dB0:  field step thresholds in pT. 
                    if step is smaller than this, stop zeroing procedure.
                    All conditions must be satisfied for field zero stop
                    Set to inf to disable
    
    show: if true write diagnostic to stdout

`monitor_data(self, window_s=5)`
:   Continuously stream data to window
    
    window_s: show the last window_s seconds of data on the stream
    
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

`read_data(self, npts, clear_buffer=True)`
:   Read data from the device 
    
    npts: number of data points to read
    clear_buffer: if true, clear buffer and wait for new
    
    assumed readback rate based on comments from QuSpin
    time[0] is the time immediately after clearing the buffer. 
        Note that there is often an incomplete word after clear, we ignore this
        As a result the error in time is at most 1/self.data_read_rate
    
    returns (time, field)

`reboot(self)`
:   Reboot the microprocessor and reloads the firmware

`set_axis_mode(self, mode='z')`
:   Change field-sensitive axis
    
    mode =  z       Operate the magnetometer in single Z axis mode
            y       Operate the magnetometer in single Y axis mode
            dual    Operate the magnetometer in dual Y and Z axis mode

`set_gain(self, mode='1x')`
:   Set analog gain (analog output only)
    
    mode =  0.33x   Set the analog output gain to 0.33 times default (0.9 V/nT)
            1x      Set the analog output gain to default (2.7 V/nT)
            3x      Set the analog output gain to 3 times default (8.1 V/nT)

`update_status(self, clear_buffer=True)`
:   Clear input buffer and read status
    
    updates the following attributes: 
        self.status_last_updated
        self.led
        self.sensor_par
        self.messages


[QZFM commands]:https://quspin.com/products-qzfm-gen2-arxiv/qzfm-command-list/