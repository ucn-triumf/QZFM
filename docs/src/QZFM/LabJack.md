# Labjack

[Qzfm Index](../../README.md#qzfm-index) / `src` / [Qzfm](./index.md#qzfm) / Labjack

> Auto-generated documentation for [src.QZFM.LabJack](../../../src/QZFM/LabJack.py) module.

- [Labjack](#labjack)
  - [QZFMlj](#qzfmlj)
    - [QZFMlj.read\_data](#qzfmljread_data)
    - [QZFMlj.read\_single](#qzfmljread_single)
    - [QZFMlj.setup](#qzfmljsetup)

## QZFMlj

[Show source in LabJack.py:25](../../../src/QZFM/LabJack.py#L25)

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

### QZFMlj.read_data

[Show source in LabJack.py:100](../../../src/QZFM/LabJack.py#L100)

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

[Show source in LabJack.py:76](../../../src/QZFM/LabJack.py#L76)

Read single set of values from device. Use read_stream get a longer sequence

#### Returns

- `np.ndarray` - fields in pT

#### Signature

```python
def read_single(self): ...
```

### QZFMlj.setup

[Show source in LabJack.py:57](../../../src/QZFM/LabJack.py#L57)

Setup input channels to read from. Use AI#

#### Arguments

- `x` *int* - AI# channel to read in Bx
- `y` *int* - AI# channel to read in By
- `z` *int* - AI# channel to read in Bz

#### Signature

```python
def setup(self, x=0, y=1, z=2): ...
```