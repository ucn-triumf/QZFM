# Qzfm

[Qzfm Index](../README.md#qzfm-index) /
[Src](./index.md#src) /
Qzfm

> Auto-generated documentation for [src.QZFM](../../src/QZFM.py) module.

- [Qzfm](#qzfm)
  - [QZFM](#qzfm-1)
      - [Attributes](#attributes)
      - [Signature](#signature)
    - [QZFM.auto\_start](#qzfmauto_start)
      - [Arguments](#arguments)
      - [Signature](#signature-1)
    - [QZFM.calibrate](#qzfmcalibrate)
      - [Arguments](#arguments-1)
      - [Signature](#signature-2)
    - [QZFM.cell\_Tlock](#qzfmcell_tlock)
      - [Signature](#signature-3)
    - [QZFM.connect](#qzfmconnect)
      - [Arguments](#arguments-2)
      - [Signature](#signature-4)
    - [QZFM.disconnect](#qzfmdisconnect)
      - [Signature](#signature-5)
    - [QZFM.draw\_data](#qzfmdraw_data)
      - [Signature](#signature-6)
    - [QZFM.field\_reset](#qzfmfield_reset)
      - [Signature](#signature-7)
    - [QZFM.field\_zero](#qzfmfield_zero)
      - [Arguments](#arguments-3)
      - [Signature](#signature-8)
    - [QZFM.field\_zeroed](#qzfmfield_zeroed)
      - [Signature](#signature-9)
    - [QZFM.is\_master](#qzfmis_master)
      - [Signature](#signature-10)
    - [QZFM.laser\_locked](#qzfmlaser_locked)
      - [Signature](#signature-11)
    - [QZFM.laser\_on](#qzfmlaser_on)
      - [Signature](#signature-12)
    - [QZFM.monitor\_cell\_T\_error](#qzfmmonitor_cell_t_error)
      - [Arguments](#arguments-4)
      - [Signature](#signature-13)
    - [QZFM.monitor\_data](#qzfmmonitor_data)
      - [Arguments](#arguments-5)
      - [Signature](#signature-14)
    - [QZFM.monitor\_status](#qzfmmonitor_status)
      - [Signature](#signature-15)
    - [QZFM.print\_messages](#qzfmprint_messages)
      - [Arguments](#arguments-6)
      - [Signature](#signature-16)
    - [QZFM.print\_state](#qzfmprint_state)
      - [Signature](#signature-17)
    - [QZFM.print\_status](#qzfmprint_status)
      - [Arguments](#arguments-7)
      - [Signature](#signature-18)
    - [QZFM.read\_data](#qzfmread_data)
      - [Arguments](#arguments-8)
      - [Returns](#returns)
      - [Signature](#signature-19)
    - [QZFM.read\_offsets](#qzfmread_offsets)
      - [Arguments](#arguments-9)
      - [Returns](#returns-1)
      - [Signature](#signature-20)
    - [QZFM.reboot](#qzfmreboot)
      - [Signature](#signature-21)
    - [QZFM.set\_axis\_mode](#qzfmset_axis_mode)
      - [Arguments](#arguments-10)
      - [Signature](#signature-22)
    - [QZFM.set\_gain](#qzfmset_gain)
      - [Arguments](#arguments-11)
      - [Signature](#signature-23)
    - [QZFM.to\_csv](#qzfmto_csv)
      - [Arguments](#arguments-12)
      - [Signature](#signature-24)
    - [QZFM.to\_csv\_fz](#qzfmto_csv_fz)
      - [Arguments](#arguments-13)
      - [Signature](#signature-25)
    - [QZFM.update\_status](#qzfmupdate_status)
      - [Arguments](#arguments-14)
      - [Signature](#signature-26)

## QZFM

[Show source in QZFM.py:26](../../src/QZFM.py#L26)

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
    def __init__(self, device_name=None, nbytes_status=1000):
        ...
```

### QZFM.auto_start

[Show source in QZFM.py:207](../../src/QZFM.py#L207)

Initiate the automated sensor startup routines

#### Arguments

- `block` *bool* - if True, wait until laser is locked and temperature stabilized before unblocking
- `show` *boo* - print status continuously to screen until finished

#### Signature

```python
def auto_start(self, block: bool = True, show: bool = True):
    ...
```

### QZFM.calibrate

[Show source in QZFM.py:224](../../src/QZFM.py#L224)

Calibrate the response (field to voltage) of the magnetometer with an internal signal reference

#### Arguments

- `show` *bool* - if true, print to screen

#### Signature

```python
def calibrate(self, show: bool = True):
    ...
```

### QZFM.cell_Tlock

[Show source in QZFM.py:1030](../../src/QZFM.py#L1030)

#### Signature

```python
@property
def cell_Tlock(self):
    ...
```

### QZFM.connect

[Show source in QZFM.py:249](../../src/QZFM.py#L249)

Connect to the QuSpin device

#### Arguments

- `device_name` *str* - name of device (ex: "Z3T0-AAL9"), or partial name (ex: "Z3T0")

#### Signature

```python
def connect(self, device_name: str):
    ...
```

### QZFM.disconnect

[Show source in QZFM.py:266](../../src/QZFM.py#L266)

Disconnect from QuSpin

#### Signature

```python
def disconnect(self):
    ...
```

### QZFM.draw_data

[Show source in QZFM.py:272](../../src/QZFM.py#L272)

Draw data to window

#### Signature

```python
def draw_data(self):
    ...
```

### QZFM.field_reset

[Show source in QZFM.py:286](../../src/QZFM.py#L286)

Sets the internal coil field values to zero

#### Signature

```python
def field_reset(self):
    ...
```

### QZFM.field_zero

[Show source in QZFM.py:298](../../src/QZFM.py#L298)

Run field zeroing procedure

#### Arguments

- `on` *bool* - if True, start sensor field zeroing procedure to apply a compensation field using the internal sensor coils to null background fields.
            If False, stop zeroing procedure.

- `axes_xyz` *bool* - If True, field zeroing is applied to all three axes (default). If False, field zeroing is applied only to Y & Z axes
- `show` *float* - if True write diagnostic to stdout

#### Signature

```python
def field_zero(self, on: bool = True, axes_xyz: bool = True, show: bool = True):
    ...
```

### QZFM.field_zeroed

[Show source in QZFM.py:1040](../../src/QZFM.py#L1040)

#### Signature

```python
@property
def field_zeroed(self):
    ...
```

### QZFM.is_master

[Show source in QZFM.py:1045](../../src/QZFM.py#L1045)

#### Signature

```python
@property
def is_master(self):
    ...
```

### QZFM.laser_locked

[Show source in QZFM.py:1035](../../src/QZFM.py#L1035)

#### Signature

```python
@property
def laser_locked(self):
    ...
```

### QZFM.laser_on

[Show source in QZFM.py:1025](../../src/QZFM.py#L1025)

#### Signature

```python
@property
def laser_on(self):
    ...
```

### QZFM.monitor_cell_T_error

[Show source in QZFM.py:372](../../src/QZFM.py#L372)

Continuously stream cell temperature to figure

See https://matplotlib.org/stable/tutorials/advanced/blitting.html

#### Arguments

- `window_s` *int* - show the last window_s seconds of data on the stream
- `figsize` *tuple* - size of display

#### Signature

```python
def monitor_cell_T_error(self, window_s: int = 20, figsize=(10, 6)):
    ...
```

### QZFM.monitor_data

[Show source in QZFM.py:478](../../src/QZFM.py#L478)

Continuously stream data to window

See https://matplotlib.org/stable/tutorials/advanced/blitting.html

#### Arguments

- `axis` *str* - x|y|z
- `window_s` *int* - show the last window_s seconds of data on the stream
- `figsize` *tuple* - size of display

#### Signature

```python
def monitor_data(self, axis: str = "z", window_s: int = 10, figsize=(10, 6)):
    ...
```

### QZFM.monitor_status

[Show source in QZFM.py:578](../../src/QZFM.py#L578)

Continuously update and print status

#### Signature

```python
def monitor_status(self):
    ...
```

### QZFM.print_messages

[Show source in QZFM.py:593](../../src/QZFM.py#L593)

Print messages to screen

#### Arguments

- `last_n` *float|None* - print the last_n number of messages. If None, print all.

#### Signature

```python
def print_messages(self, last_n=None):
    ...
```

### QZFM.print_state

[Show source in QZFM.py:608](../../src/QZFM.py#L608)

Print state of the python object

#### Signature

```python
def print_state(self):
    ...
```

### QZFM.print_status

[Show source in QZFM.py:620](../../src/QZFM.py#L620)

Print status of QuSpin in a nicely formatted message

#### Arguments

- `update` *bool* - if True, update before printing. Otherwise, print prior saved values.
- `overwrite_last` *bool* - if True, overwrite the last message. Used in monitor_status

#### Signature

```python
def print_status(self, update: bool = False, overwrite_last: bool = False):
    ...
```

### QZFM.read_data

[Show source in QZFM.py:657](../../src/QZFM.py#L657)

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
def read_data(self, seconds: float, axis: str = "z", clear_buffer: bool = True):
    ...
```

### QZFM.read_offsets

[Show source in QZFM.py:733](../../src/QZFM.py#L733)

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
def read_offsets(self, npts: int, clear_buffer: bool = True):
    ...
```

### QZFM.reboot

[Show source in QZFM.py:827](../../src/QZFM.py#L827)

Reboot the microprocessor and reloads the firmware

#### Signature

```python
def reboot(self):
    ...
```

### QZFM.set_axis_mode

[Show source in QZFM.py:833](../../src/QZFM.py#L833)

Change field-sensitive axis

Note: triaxial sensors do not respond to this command

#### Arguments

- `mode` *str* - z|y|dual

#### Signature

```python
def set_axis_mode(self, mode: str = "z"):
    ...
```

### QZFM.set_gain

[Show source in QZFM.py:855](../../src/QZFM.py#L855)

Set analog gain (analog output only)

#### Arguments

- `mode` *str* - 0.33x|1x|3x
        0.33x (0.9 V/nT)
        1x (2.7 V/nT)
        3x (8.1 V/nT)

#### Signature

```python
def set_gain(self, mode: str = "1x"):
    ...
```

### QZFM.to_csv

[Show source in QZFM.py:878](../../src/QZFM.py#L878)

Write data to csv, if no filename, use default

#### Arguments

- `filename` *str* - name of file to write
- `notes` - things to add to file header

#### Signature

```python
def to_csv(self, filename=None, *notes):
    ...
```

### QZFM.to_csv_fz

[Show source in QZFM.py:923](../../src/QZFM.py#L923)

Write field zero data to csv, if no filename, use default

#### Arguments

- `filename` *str* - name of file to write
- `notes` - things to add to file header

#### Signature

```python
def to_csv_fz(self, filename=None, *notes):
    ...
```

### QZFM.update_status

[Show source in QZFM.py:957](../../src/QZFM.py#L957)

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
def update_status(self, clear_buffer: bool = True):
    ...
```
