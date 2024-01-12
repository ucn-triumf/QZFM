"""
Control and read analog output from QuSpin using a LabJack device
Derek Fujimoto
Sep 2023

Requires install of the following:
    Labjack
        LJM software for T7 devices: https://labjack.com/pages/support?doc=%2Fsoftware-driver%2Finstaller-downloads%2Fljm-software-installers-t4-t7-digit%2F
        LJM python package: python -m pip install labjack-ljm
"""

import numpy as np
import pandas as pd
import time
from QZFM import QZFM
from datetime import datetime

# import labjack-ljm
try:
    from labjack import ljm
except ModuleNotFoundError:
    pass

class QZFMlj(QZFM):
    """Low-level readback from Labjack DAQ module via USB

    Attributes:

        ch: (tuple): channel addresses for analog inputs
        handle (int): handle for sending info to labjack. Output of ljm.openS
    """

    def __init__(self, QZFM_name=None, LJ_type='T7', LJ_connection='USB', LJ_id='ANY',
                 QZFM_nbytes=1000):
        """Initialize object: connect

        Args:
            QZFM_name (str): name of device to look for (connection)
                             for windows this is likely COM3 or COM5
                             for linux, search Z3T0 or similar
            LJ_type (str): passed to ljm.openS, model type
            LJ_connection (str): passed to ljm.openS, connection type. USB|ANY|ETHERNET
            LJ_identifier (str): passed to ljm.openS, device id
            QZFM_nbytes (int): serial read chunk size in bytes for status updates
        """

        # get LJ handle
        self.handle = ljm.openS(deviceType=LJ_type,
                                connectionType=LJ_connection,
                                identifier=LJ_id)

        # open QuSpin
        super().__init__(device_name=QZFM_name,
                         nbytes_status=QZFM_nbytes)

    def auto_start(self, xch, ych, zch, block=True, show=True, zero_calibrate=True):
        """Initiate the automated sensor startup routines

        Args:
            x (int): AI# channel to read in Bx
            y (int): AI# channel to read in By
            z (int): AI# channel to read in Bz
            block (bool): if True, wait until laser is locked and temperature stabilized before unblocking
            show (bool): print status continuously to screen until finished
            zero_calibrate (bool): if true, also field zero and calibrate the sensor. Forces block = True
        """


        # setup labjack
        self.setup(xch, ych, zch)

        # setup quspin
        return super().auto_start(block, show, zero_calibrate)

    def setup(self, x=0, y=1, z=2):
        """Setup input channels to read from. Use AI#

        Args:
            x (int): AI# channel to read in Bx
            y (int): AI# channel to read in By
            z (int): AI# channel to read in Bz
        """

        # check inputs
        if not (type(x) is int and type(y) is int and type(z) is int):
            raise RuntimeError(f'x, y, and z must be int, not {type(x)}, {type(y)}, and {type(z)}')

        if x == y or y == z or x == z:
            raise RuntimeError('Require that x != y != z')

        # get channel addresses
        self.ch = ljm.namesToAddresses(3, (f'AIN{x}', f'AIN{y}', f'AIN{z}'))[0]

    def read_single(self):
        """Read single set of values from device. Use read_data get a longer sequence

        Returns:
            np.ndarray: fields in pT
        """
        rate = 1000
        nchannels = len(self.ch)

        # start stream
        ljm.eStreamStart(self.handle,
                         scansPerRead=1,
                         numAddresses=nchannels,
                         aScanList=self.ch,
                         scanRate=rate)

        # get data
        dat = np.array(ljm.eStreamRead(self.handle)[0])

        # stop stream
        ljm.eStreamStop(self.handle)

        return dat

    def read_data(self, seconds=1, rate=-1):
        """Read set of values from device

        Args:
            seconds (float): measurement duration in seconds
            rate (float): number of measurements to read per second

        Returns:
            pd.DataFrame denoting times and fields
        """

        nchannels = len(self.ch)

        # start stream
        rate = ljm.eStreamStart(self.handle,
                                scansPerRead=rate,
                                numAddresses=nchannels,
                                aScanList=self.ch,
                                scanRate=rate)

        # get data
        start_time = time.time()
        all_dat = []
        npts_now = 0
        npts = seconds * rate * nchannels
        while npts_now < npts:
            dat = ljm.eStreamRead(self.handle)[0]
            npts_now += len(dat)
            all_dat.append(dat)

        # stop stream
        ljm.eStreamStop(self.handle)

        # un-interweave data
        dat = np.concatenate(all_dat)
        data = {f'B{x} (nT)': dat[i::nchannels] for i, x in enumerate('xyz')}

        # add timestamps
        data['elapsed (s)'] = np.arange(len(dat)/nchannels)/rate
        data['epoch time (s)'] = data['elapsed (s)'] + start_time

        # to dataframe
        df = pd.DataFrame(data)

        # convert to nT
        for c in df.columns:
            if 'nT' in c:
                df.loc[:, c] /= self.gain

        df = df.set_index('elapsed (s)')
        self.field = df

        return df

    def to_csv(self, filename=None, *notes):
        """Write data to csv, if no filename, use default

        Args:
            filename (str): name of file to write
            notes: things to add to file header
        """

        # set default file name
        if filename is None:
            t = datetime.now()
            filename = f'qzfm_{datetime.strftime("%y%m%d%H%M%S")}.csv'

        # make dataframe
        df = self.field
        self.update_status()

        # write file header
        header = [ '# QZFM (QuSpin Zero Field Monitor) analog data',
                   '# ',
                  f'# Field zeroed:    {self.led["field zeroed (LED4)"]}',
                  f'# Laser lock:      {self.led["laser lock (LED3)"]}',
                  f'# Cell T lock:     {self.led["cell temp lock (LED2)"]}',
                  f'# Laser on:        {self.led["laser on (LED1)"]}',
                  '#',
                  f'# Cell T error:    {self.sensor_par["cell temp error"]}',
                  f'# Bz field:        {self.sensor_par["Bz field (pT)"]:.4f} pT',
                  f'# By field:        {self.sensor_par["By field (pT)"]:.4f} pT',
                  f'# B0 field:        {self.sensor_par["B0 field (pT)"]:.4f} pT',
                   '#',
                  ]

        if notes:
            notes = [f'#\t{note}' for note in notes]
            header.extend(['# Notes', *notes, '#'])

        header.extend([f'# {datetime.now()}', '# \n'])

        with open(filename, 'w') as fid:
            fid.write('\n'.join(header))

        # write data
        df.to_csv(filename, mode='a', index=False)