# Labjack

[Qzfm Index](../../README.md#qzfm-index) / `src` / [Qzfm](./index.md#qzfm) / Labjack

> Auto-generated documentation for [src.QZFM.LabJack](../../../src/QZFM/LabJack.py) module.

- [Labjack](#labjack)
  - [QZFMlj](#qzfmlj)
    - [QZFMlj.auto\_start](#qzfmljauto_start)
    - [QZFMlj.read\_data](#qzfmljread_data)
    - [QZFMlj.read\_single](#qzfmljread_single)
    - [QZFMlj.setup](#qzfmljsetup)
    - [QZFMlj.to\_csv](#qzfmljto_csv)

## QZFMlj

[Show source in LabJack.py:24](../../../src/QZFM/LabJack.py#L24)

Low-level readback from Labjack DAQ module via USB

#### Attributes

- `ch` - (tuple): channel addresses for analog inputs
- `handle` *int* - handle for sending info to labjack. Output of ljm.openS

#### Signature

```python
class QZFMlj(QZFM):
    def __init__(
        self,
        QZFM_name=None,
        LJ_type="T7",
        LJ_connection="USB",
        LJ_id="ANY",
        QZFM_nbytes=1000,
    ): ...
```

### QZFMlj.auto_start

[Show source in LabJack.py:56](../../../src/QZFM/LabJack.py#L56)

Initiate the automated sensor startup routines

#### Arguments

- `x` *int* - AI# channel to read in Bx
- `y` *int* - AI# channel to read in By
- `z` *int* - AI# channel to read in Bz
- `block` *bool* - if True, wait until laser is locked and temperature stabilized before unblocking
- `show` *bool* - print status continuously to screen until finished
- `zero_calibrate` *bool* - if true, also field zero and calibrate the sensor. Forces block = True

#### Signature

```python
def auto_start(self, xch, ych, zch, block=True, show=True, zero_calibrate=True): ...
```

### QZFMlj.read_data

[Show source in LabJack.py:118](../../../src/QZFM/LabJack.py#L118)

Read set of values from device

#### Arguments

- `seconds` *float* - measurement duration in seconds
- `rate` *float* - number of measurements to read per second

#### Returns

pd.DataFrame denoting times and fields

#### Signature

```python
def read_data(self, seconds=1, rate=-1): ...
```

### QZFMlj.read_single

[Show source in LabJack.py:94](../../../src/QZFM/LabJack.py#L94)

Read single set of values from device. Use read_data get a longer sequence

#### Returns

- `np.ndarray` - fields in pT

#### Signature

```python
def read_single(self): ...
```

### QZFMlj.setup

[Show source in LabJack.py:75](../../../src/QZFM/LabJack.py#L75)

Setup input channels to read from. Use AI#

#### Arguments

- `x` *int* - AI# channel to read in Bx
- `y` *int* - AI# channel to read in By
- `z` *int* - AI# channel to read in Bz

#### Signature

```python
def setup(self, x=0, y=1, z=2): ...
```

### QZFMlj.to_csv

[Show source in LabJack.py:172](../../../src/QZFM/LabJack.py#L172)

Write data to csv, if no filename, use default

#### Arguments

- `filename` *str* - name of file to write
- `notes` - things to add to file header

#### Signature

```python
def to_csv(self, filename=None, *notes): ...
```