# Qzfm

[Qzfm Index](../../README.md#qzfm-index) / `src` / [Qzfm](./index.md#qzfm) / Qzfm

> Auto-generated documentation for [src.QZFM.QZFM](../../../src/QZFM/QZFM.py) module.

- [Qzfm](#qzfm)
  - [QZFM](#qzfm-1)
    - [QZFM.\_get\_next\_message](#qzfm_get_next_message)
    - [QZFM.\_read\_serial](#qzfm_read_serial)
    - [QZFM.\_reset\_attributes](#qzfm_reset_attributes)
    - [QZFM.\_set\_data\_stream](#qzfm_set_data_stream)
    - [QZFM.\_set\_read\_axis](#qzfm_set_read_axis)
    - [QZFM.auto\_start](#qzfmauto_start)
    - [QZFM.calibrate](#qzfmcalibrate)
    - [QZFM.cell\_Tlock](#qzfmcell_tlock)
    - [QZFM.connect](#qzfmconnect)
    - [QZFM.disconnect](#qzfmdisconnect)
    - [QZFM.draw\_data](#qzfmdraw_data)
    - [QZFM.field\_reset](#qzfmfield_reset)
    - [QZFM.field\_zero](#qzfmfield_zero)
    - [QZFM.field\_zeroed](#qzfmfield_zeroed)
    - [QZFM.is\_master](#qzfmis_master)
    - [QZFM.laser\_locked](#qzfmlaser_locked)
    - [QZFM.laser\_on](#qzfmlaser_on)
    - [QZFM.monitor\_cell\_T\_error](#qzfmmonitor_cell_t_error)
    - [QZFM.monitor\_data](#qzfmmonitor_data)
    - [QZFM.monitor\_status](#qzfmmonitor_status)
    - [QZFM.print\_messages](#qzfmprint_messages)
    - [QZFM.print\_state](#qzfmprint_state)
    - [QZFM.print\_status](#qzfmprint_status)
    - [QZFM.read\_data](#qzfmread_data)
    - [QZFM.read\_offsets](#qzfmread_offsets)
    - [QZFM.reboot](#qzfmreboot)
    - [QZFM.save\_state](#qzfmsave_state)
    - [QZFM.set\_axis\_mode](#qzfmset_axis_mode)
    - [QZFM.set\_gain](#qzfmset_gain)
    - [QZFM.set\_master](#qzfmset_master)
    - [QZFM.to\_csv](#qzfmto_csv)
    - [QZFM.to\_csv\_fz](#qzfmto_csv_fz)
    - [QZFM.update\_status](#qzfmupdate_status)

## QZFM

[Show source in QZFM.py:31](../../../src/QZFM/QZFM.py#L31)

Low-level control of QuSpin magnetic sensor via QZFM serial commands via USB

#### Attributes

- `axis_mode` *str* - readback mode for daq
- `data_read_rate` *int* - readback rate in Hz
- `field` *np.array* - magnetic fields (pT)
- `gain` *float* - V/nT from setting analog gain
- `is_calibrated` *bool* - True if calibration is ok
- `is_data_streaming` *bool* - True if data streaming mode
- `is_field_zeroed` *bool* - True if field zeroing is maintained
- `is_xyz_zeroing` *bool* - True if field zeroing applied to all axes, else only y and z
- `led` *dict* - led status on/off
- `messages` *list* - (message, epoch time)
- `nbytes_status` *int* - serial read chunk size in bytes for status updates
- `read_axis` *str* - axis for readback
- `sensor_par` *dict* - sensor parameter readback values
- `ser` *serial.Serial* - object for connection
- `serial_settings` *dict* - default settings. See https://pyserial.readthedocs.io/en/latest/pyserial_api.html#serial.Serial
- `status_last_updated` *int* - epoch time last updated status (led, sensor_par, messages)
- `time` *np.array* - epoch times corresponding to field measurements

#### Signature

```python
class QZFM(object):
    def __init__(self, device_name=None, nbytes_status=1000): ...
```

### QZFM._get_next_message

[Show source in QZFM.py:104](../../../src/QZFM/QZFM.py#L104)

Block until for next message, as denoted by "#" first character

Save message to message list

#### Arguments

- `timeout` *int* - duration in seconds to wait until next message
- `clear_buffer` *bool* - if true, clear input buffer

#### Signature

```python
def _get_next_message(self, timeout=1, clear_buffer=True): ...
```

### QZFM._read_serial

[Show source in QZFM.py:136](../../../src/QZFM/QZFM.py#L136)

Read a serial messsage and convert to utf-8, split by newlines

#### Arguments

- `nbytes` *int* - number of bytes to read
- `clear_buffer` *bool* - if true, clear the buffer before read

#### Returns

- `str` - message from device

#### Signature

```python
def _read_serial(self, nbytes, clear_buffer=True): ...
```

### QZFM._reset_attributes

[Show source in QZFM.py:161](../../../src/QZFM/QZFM.py#L161)

Set attributes to default values

#### Signature

```python
def _reset_attributes(self): ...
```

### QZFM._set_data_stream

[Show source in QZFM.py:176](../../../src/QZFM/QZFM.py#L176)

Turns on/off the sensor digital data stream and stops updating sensor status information

Equivalent to the Print ON and Print OFF commands

#### Arguments

- `on` *bool* - if True turn data stream on. Else turn off.

#### Signature

```python
def _set_data_stream(self, on=True): ...
```

### QZFM._set_read_axis

[Show source in QZFM.py:192](../../../src/QZFM/QZFM.py#L192)

Change the axis for measurement

#### Arguments

- `axis` *str* - x|y|z

#### Signature

```python
def _set_read_axis(self, axis): ...
```

### QZFM.auto_start

[Show source in QZFM.py:215](../../../src/QZFM/QZFM.py#L215)

Initiate the automated sensor startup routines

#### Arguments

- `block` *bool* - if True, wait until laser is locked and temperature stabilized before unblocking
- `show` *bool* - print status continuously to screen until finished
- `zero_calibrate` *bool* - if true, also field zero and calibrate the sensor. Forces block = True

#### Returns

None

#### Signature

```python
def auto_start(self, block=True, show=True, zero_calibrate=True): ...
```

### QZFM.calibrate

[Show source in QZFM.py:288](../../../src/QZFM/QZFM.py#L288)

Calibrate the response (field to voltage) of the magnetometer with an internal signal reference

#### Arguments

- `show` *bool* - if true, print to screen

#### Signature

```python
def calibrate(self, show=True): ...
```

### QZFM.cell_Tlock

[Show source in QZFM.py:1233](../../../src/QZFM/QZFM.py#L1233)

#### Signature

```python
@property
def cell_Tlock(self): ...
```

### QZFM.connect

[Show source in QZFM.py:313](../../../src/QZFM/QZFM.py#L313)

Connect to the QuSpin device

#### Arguments

- `device_name` *str* - name of device (ex: "Z3T0-AAL9"), or partial name (ex: "Z3T0")

#### Signature

```python
def connect(self, device_name): ...
```

### QZFM.disconnect

[Show source in QZFM.py:330](../../../src/QZFM/QZFM.py#L330)

Disconnect from QuSpin

#### Signature

```python
def disconnect(self): ...
```

### QZFM.draw_data

[Show source in QZFM.py:335](../../../src/QZFM/QZFM.py#L335)

Draw data to window

#### Arguments

- `ascii` *bool* - if True, draw to stdout

#### Signature

```python
def draw_data(self, ascii=False): ...
```

### QZFM.field_reset

[Show source in QZFM.py:365](../../../src/QZFM/QZFM.py#L365)

Sets the internal coil field values to zero

#### Signature

```python
def field_reset(self): ...
```

### QZFM.field_zero

[Show source in QZFM.py:377](../../../src/QZFM/QZFM.py#L377)

Run field zeroing procedure

#### Arguments

- `on` *bool* - if True, start sensor field zeroing procedure to apply a compensation field using the internal sensor coils to null background fields.
            If False, stop zeroing procedure.

- `axes_xyz` *bool* - If True, field zeroing is applied to all three axes (default). If False, field zeroing is applied only to Y & Z axes
- `show` *float* - if True write diagnostic to stdout

#### Signature

```python
def field_zero(self, on=True, axes_xyz=True, show=True): ...
```

### QZFM.field_zeroed

[Show source in QZFM.py:1243](../../../src/QZFM/QZFM.py#L1243)

#### Signature

```python
@property
def field_zeroed(self): ...
```

### QZFM.is_master

[Show source in QZFM.py:1248](../../../src/QZFM/QZFM.py#L1248)

#### Signature

```python
@property
def is_master(self): ...
```

### QZFM.laser_locked

[Show source in QZFM.py:1238](../../../src/QZFM/QZFM.py#L1238)

#### Signature

```python
@property
def laser_locked(self): ...
```

### QZFM.laser_on

[Show source in QZFM.py:1228](../../../src/QZFM/QZFM.py#L1228)

#### Signature

```python
@property
def laser_on(self): ...
```

### QZFM.monitor_cell_T_error

[Show source in QZFM.py:454](../../../src/QZFM/QZFM.py#L454)

Continuously stream cell temperature to figure

See https://matplotlib.org/stable/tutorials/advanced/blitting.html

#### Arguments

- `window_s` *int* - show the last window_s seconds of data on the stream
- `figsize` *tuple* - size of display

#### Signature

```python
def monitor_cell_T_error(self, window_s=20, figsize=(10, 6)): ...
```

### QZFM.monitor_data

[Show source in QZFM.py:560](../../../src/QZFM/QZFM.py#L560)

Continuously stream data to window

See https://matplotlib.org/stable/tutorials/advanced/blitting.html

#### Arguments

- `axis` *str* - x|y|z
- `window_s` *int* - show the last window_s seconds of data on the stream
- `figsize` *tuple* - size of display (x, y)
- `ascii` *bool* - if true, display figure in terminal window

#### Signature

```python
def monitor_data(self, axis="z", window_s=10, figsize=None, ascii=False): ...
```

### QZFM.monitor_status

[Show source in QZFM.py:700](../../../src/QZFM/QZFM.py#L700)

Continuously update and print status

#### Signature

```python
def monitor_status(self): ...
```

### QZFM.print_messages

[Show source in QZFM.py:715](../../../src/QZFM/QZFM.py#L715)

Print messages to screen

#### Arguments

- `last_n` *float|None* - print the last_n number of messages. If None, print all.

#### Signature

```python
def print_messages(self, last_n=None): ...
```

### QZFM.print_state

[Show source in QZFM.py:730](../../../src/QZFM/QZFM.py#L730)

Print state of the python object

#### Signature

```python
def print_state(self): ...
```

### QZFM.print_status

[Show source in QZFM.py:742](../../../src/QZFM/QZFM.py#L742)

Print status of QuSpin in a nicely formatted message

#### Arguments

- `update` *bool* - if True, update before printing. Otherwise, print prior saved values.
- `overwrite_last` *bool* - if True, overwrite the last message. Used in monitor_status
- `print_last_message` *bool* - if True, print last message from QZFM

#### Signature

```python
def print_status(self, update=False, overwrite_last=False, print_last_message=True): ...
```

### QZFM.read_data

[Show source in QZFM.py:786](../../../src/QZFM/QZFM.py#L786)

Read data from the device

Assumed readback rate based on comments from QuSpin:
    time[0] is the time immediately after clearing the buffer.
    Note that there is often an incomplete word after clear, we ignore this
    As a result the error in time is at most 1/self.data_read_rate

#### Arguments

- `seconds` *float* - duration of measurement npts= seconds*200Hz
- `axis` *str* - x|y|z
- `clear_buffer` *bool* - If true, clear buffer and wait for new

#### Returns

- `tuple` - np arrays (time, field)

#### Signature

```python
def read_data(self, seconds, axis="z", clear_buffer=True): ...
```

### QZFM.read_offsets

[Show source in QZFM.py:866](../../../src/QZFM/QZFM.py#L866)

Read offset data from the device in field zeroing mode

time[0] is the time immediately after clearing the buffer.
reads at approx 7.5 Hz

#### Arguments

- `npts` *int* - number of data points to read
- `clear_buffer` *bool* - if true, clear initial buffer and wait for new

#### Returns

- `pd.DataFrame` - field zeroing data and timestamps

#### Signature

```python
def read_offsets(self, npts, clear_buffer=True): ...
```

### QZFM.reboot

[Show source in QZFM.py:960](../../../src/QZFM/QZFM.py#L960)

Reboot the microprocessor and reloads the firmware

#### Signature

```python
def reboot(self): ...
```

### QZFM.save_state

[Show source in QZFM.py:966](../../../src/QZFM/QZFM.py#L966)

Write state of QZFM to file as a YAML file

#### Arguments

- `filename` *str* - path to file to write, if none, set default filename

#### Returns

None

#### Signature

```python
def save_state(self, filename=None): ...
```

### QZFM.set_axis_mode

[Show source in QZFM.py:1013](../../../src/QZFM/QZFM.py#L1013)

Change field-sensitive axis

Note: triaxial sensors do not respond to this command

#### Arguments

- `mode` *str* - z|y|dual

#### Signature

```python
def set_axis_mode(self, mode="z"): ...
```

### QZFM.set_gain

[Show source in QZFM.py:1035](../../../src/QZFM/QZFM.py#L1035)

Set analog gain (analog output only)

#### Arguments

- `mode` *str* - 0.1x|0.33x|1x|3x
        0.1x (0.27 V/nT)
        0.33x (0.9 V/nT)
        1x (2.7 V/nT)
        3x (8.1 V/nT)

#### Signature

```python
def set_gain(self, mode="1x"): ...
```

### QZFM.set_master

[Show source in QZFM.py:1070](../../../src/QZFM/QZFM.py#L1070)

Set master/slave status

#### Arguments

- `master` *bool* - If true set as master, else set as slave

#### Signature

```python
def set_master(self, master=True): ...
```

### QZFM.to_csv

[Show source in QZFM.py:1081](../../../src/QZFM/QZFM.py#L1081)

Write data to csv, if no filename, use default

#### Arguments

- `filename` *str* - name of file to write
- `notes` - things to add to file header

#### Signature

```python
def to_csv(self, filename=None, *notes): ...
```

### QZFM.to_csv_fz

[Show source in QZFM.py:1126](../../../src/QZFM/QZFM.py#L1126)

Write field zero data to csv, if no filename, use default

#### Arguments

- `filename` *str* - name of file to write
- `notes` - things to add to file header

#### Signature

```python
def to_csv_fz(self, filename=None, *notes): ...
```

### QZFM.update_status

[Show source in QZFM.py:1160](../../../src/QZFM/QZFM.py#L1160)

Clear input buffer and read status

updates the following attributes:
    self.status_last_updated
    self.led
    self.sensor_par
    self.messages

#### Arguments

- `clear_buffer` *bool* - if True clear the buffer before read attempt

#### Signature

```python
def update_status(self, clear_buffer=True): ...
```