# Read data from, and send signals to QuSpin via QZFM commands
# Derek Fujimoto
# Mar 2023

# see https://quspin.com/products-qzfm-gen2-arxiv/qzfm-command-list/
# for serial commands

# see also https://quspin.com/products-qzfm-gen2-arxiv/qzfm-quick-start-guide/
# for general usage and setup

# dependencies: pip install --user pyserial
# https://pyserial.readthedocs.io

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import serial

from serial.tools import list_ports
from time import time
from datetime import datetime

matplotlib.use('TkAgg')

class QZFM(object):
    """
        Low-level control of QuSpin magnetic sensor via QZFM serial commands via USB

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
            read_axis:          str, axis for readback
            sensor_par:         dict of sensor parameter readback values
            ser:                serial.Serial object for connection
            status_last_updated:epoch time last updated status (led, sensor_par, messages)
            time:               np.array of epoch times corresponding to field measurements 
    """

    # see https://pyserial.readthedocs.io/en/latest/pyserial_api.html#serial.Serial
    serial_settings = { 'baudrate':     115200,
                        'bytesize':     8,
                        'parity':       serial.PARITY_NONE,
                        'stopbits':     1,
                        'write_timeout':10,     # seconds
                        'xonxoff':      False,
                        'rtscts':       False,
                        'dsrdtr':       False,
                        }

    data_read_rate = 200 # Hz

    def __init__(self, nbytes_status=1000): 
        """
            nbytes_status: serial read chunk size in bytes for status updates
        """

        # bytes to read
        self.nbytes_status = nbytes_status

        # initialize data fields
        self.field = np.array([], dtype=float)
        self.time = np.array([], dtype=float)

        # initialize status
        self.status_last_updated = None
        self.led = {'laser on (LED1)':      False,
                    'cell temp lock (LED2)':False,
                    'laser lock (LED3)':    False,
                    'field zeroed (LED4)':  False,
                    'is master':            False,
                    }
        self.sensor_par = { 'cell temp error':      np.nan,
                            'cell temp voltage':    np.nan,
                            'Bz field (pT)':        np.nan, 
                            'By field (pT)':        np.nan, 
                            'B0 field (pT)':        np.nan, 
                            }
        self.messages = []
        self._reset_attributes()

    def _get_next_message(self, timeout=1):
        """
            Block until for next message, as denoted by "#" first character
            Save message to message list
            timeout: duration in s to wait until next message
        """

        # clear buffer to ensure new input
        self.ser.reset_input_buffer()

        # initialize
        mess = []
        t_start = time()

        while len(mess) == 0:

            # read output from sensor
            message = self._read_serial(self.nbytes_status)
            t = time()
            
            mess = [(m[1:], t) for m in message if m[0] == '#']

            # timeout
            if time()-t_start > timeout:
                return

        self.messages.extend(mess)

    def _read_serial(self, nbytes, clear_buffer=True):
        """
            Read a serial messsage and convert to utf-8, split by newlines
        """

        # clear buffer to ensure new input
        if clear_buffer:
            self.ser.reset_input_buffer()

        # read output from sensor
        message = self.ser.read(nbytes)

        # parse the message
        message = message.decode('utf-8')
        message = message.replace('\x00', '')
        message = message.split('\r\n')[1:-1]  # first and last element likely incomplete

        return message

    def _reset_attributes(self):
        """
            Set attributes to default values
        """
        # initialize state
        self.is_data_streaming = False
        self.is_field_zeroed = False
        self.is_xyz_zeroing = True
        self.is_calibrated = False
        
        # axis readback mode
        self.axis_mode = 'z'
        self.read_axis = 'z'

        # set default gain
        self.gain = 2.7

    def _set_data_stream(self, on=True):
        """
            Turns on/off the sensor digital data stream and stops updating sensor status information
            equivalent to the Print ON and Print OFF commands
        """
        if on:      
            self.ser.write(b'7')
            self._get_next_message()
            self.is_data_streaming = True
        else:       
            self.ser.write(b'8')
            self.is_data_streaming = False

    def _set_read_axis(self, axis):
        """
            Change the axis for measurement

            axis: str, either x, y, or z
        """

        if axis == 'x':     self.ser.write(b'G')
        elif axis == 'y':   self.ser.write(b'@')
        elif axis == 'z':   self.ser.write(b'?')
        else:
            raise RuntimeError(f'Unknown axis "{axis}"')

        self.read_axis = axis
        self._get_next_message()

    def auto_start(self, block=True, show=True):   
        """
         	Initiate the automated sensor startup routines
             
            if block, wait until laser is locked and 
            temperature stabilized before unblocking
            
            if show, monitor status
        """
        self.ser.write(b'>')
        self.update_status()
        self.print_status(overwrite_last=False)

        if block:
            while not self.led["laser lock (LED3)"] or not self.led["cell temp lock (LED2)"]:
                self.update_status()
                if show: 
                    self.print_status(overwrite_last=True)

    def calibrate(self, show=True):
        """
            Calibrate the response (field to voltage) of the magnetometer with an internal signal reference

            show: if true, print to screen
        """

        # check for field zeroing
        if not self.is_field_zeroed:

            # double check sensor light
            if not self.field_zeroed:
                raise RuntimeError('Sensors must be field zeroed first')

        # do calibration
        self.ser.write(b'9')
        self.is_calibrated = True

        # get calibration message
        self._get_next_message(timeout=100)

        # print
        if show:
            self.print_messages(1)

    def connect(self, device_name):
        """
            Connect to the QuSpin

            device_name: str, name of device (ex: "Z3T0-AAL9"), or 
                         partial name (ex: "Z3T0")
        """
        
        # list all serial ports 
        ports = [str(p) for p in list_ports.grep(device_name)]

        # error check
        if len(ports) > 1: 
            raise RuntimeError(f'Too many serial ports found. We found {ports}')

        # open serial connection
        self.ser = serial.Serial(ports[0].split()[0], **self.serial_settings)

    def disconnect(self):
        """
            Disconnect from QuSpin
        """
        self._set_data_stream(False)
        self.reboot()
        self.ser.close()

    def draw_data(self):
        """
            Draw data to window
        """
    
        # plot
        plt.figure(figsize=(10,6))
        plt.plot(self.time-self.time[0], self.field)
        
        # plot elements
        plt.ylabel('Field (pT)')
        plt.xlabel(f'Time Elapsed Since {datetime.fromtimestamp(self.time[0])} (s)',
                    fontsize='small')
        plt.tight_layout()

    def field_reset(self):
        """
            Sets the internal coil field values to zero
        """
        self.ser.write(b'V')
        self._get_next_message()
        self.sensor_par['Bz field (pT)'] = 0
        self.sensor_par['By field (pT)'] = 0
        self.sensor_par['B0 field (pT)'] = 0

        # track state
        self.is_calibrated = False
        self.is_field_zeroed = False

    def field_zero(self, on=True, axes_xyz=True, dBz=np.inf, dBy=np.inf, dB0=np.inf, dT=np.inf, show=True):
        """
            Run field zeroing procedure

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
        """

        # calibration no longer valid
        self.is_calibrated = False

        # set axes for zeroing
        if axes_xyz:    
            self.ser.write(b'i')
            self.is_xyz_zeroing = True
        else:           
            self.ser.write(b'h')
            self.is_xyz_zeroing = False

        # set field zero status
        if on:  
            self.ser.write(b'D')
            self.is_field_zeroed = False
        else:   
            self.ser.write(b'E')
            self.is_field_zeroed = True
            self.update_status()

        if on:

            # setup last setting
            Bz_last = np.inf
            By_last = np.inf
            B0_last = np.inf

            # get current setting
            self.update_status()
            Bz_now = self.sensor_par['Bz field (pT)']
            By_now = self.sensor_par['By field (pT)']
            B0_now = self.sensor_par['B0 field (pT)']
            T_now = self.sensor_par['cell temp error']
            
            if not (np.isinf(dBz) and np.isinf(dBy) and np.isinf(dB0) and np.isinf(dT)):
                print('\n'*5)

            try:
                while (abs(Bz_now - Bz_last) > dBz) or (abs(By_now - By_last) > dBy) or \
                    (abs(B0_now - B0_last) > dB0) or (abs(T_now) > dT):
                    
                    # track
                    Bz_last = Bz_now
                    By_last = By_now
                    B0_last = B0_now

                    # get new values
                    self.update_status()
                    Bz_now = self.sensor_par['Bz field (pT)']
                    By_now = self.sensor_par['By field (pT)']
                    B0_now = self.sensor_par['B0 field (pT)']
                    T_now = self.sensor_par['cell temp error']

                    # print
                    if show:
                        lines = [f'Bz = {Bz_now:.4f} pT, dBz = {abs(Bz_now-Bz_last):.4f} pT (thresh: {dBz})',
                                 f'By = {By_now:.4f} pT, dBy = {abs(By_now-By_last):.4f} pT (thresh: {dBy})',
                                 f'B0 = {B0_now:.4f} pT, dB0 = {abs(B0_now-B0_last):.4f} pT (thresh: {dB0})',
                                 '',
                                 f'T error = {T_now:.4f} (thresh: {dT})',
                                ]
                        print("\033[F"*5 + '\n'.join(lines))
            except KeyboardInterrupt:
                print()

            if not (np.isinf(dBz) and np.isinf(dBy) and np.isinf(dB0) and np.isinf(dT)):
                self.field_zero(on=False)

            self.update_status()
    
    def monitor_data(self, axis='z', window_s=5, figsize=(10, 6)):
        """
            Continuously stream data to window

            axis:     axis to read from
            window_s: show the last window_s seconds of data on the stream
            figsize:  size of display

            See https://matplotlib.org/stable/tutorials/advanced/blitting.html
        """

        # get npts to show
        npts = self.data_read_rate * window_s

        # set data to stream
        if not self.is_data_streaming:
            self._set_data_stream()

        # make figure 
        fig, ax = plt.subplots(figsize=figsize)

        # draw initial window
        x = np.linspace(-window_s, 0, npts)
        _, y = self.read_data(npts, axis=axis, clear_buffer=True)
        (line,) = plt.plot(x, y, animated=True)
        
        # plot elements
        plt.ylabel('Field (pT)')
        plt.xlabel(f'Time (s)')
        plt.tight_layout()

        # render
        plt.show(block=False)
        plt.pause(0.05)

        # get bounding box
        bg = fig.canvas.copy_from_bbox(fig.bbox)

        # draw
        ax.draw_artist(line)

        # show
        fig.canvas.blit(fig.bbox)

        # get bounds
        ylim = ax.get_ylim()

        try:
            # draw forever
            while True:
                
                # get data
                _, data = self.read_data(int(self.data_read_rate*0.05), axis=axis, clear_buffer=False)
                y = np.append(y, data)[-npts:]

                # check bounds
                if not (max(data) < ylim[1] and min(data) > ylim[0]):
                    dy = (max(y) - min(y))*0.1
                    ax.set_ylim(min(y)-dy, max(y)+dy)
                    ylim = ax.get_ylim()

                # check for figure
                if not plt.fignum_exists(fig.number):
                    break

                # reset background
                fig.canvas.restore_region(bg)

                # set y data
                line.set_ydata(y)
                ax.draw_artist(line)

                # update screen
                fig.canvas.blit(fig.bbox)
                fig.canvas.flush_events()

                # print n events in buffer
                print(f'N events remaining in buffer: {self.ser.in_waiting}', 
                      flush=True, end='\r')

        except KeyboardInterrupt:
            print()

    def monitor_status(self):
        """
            Continuously update and print status
        """

        # do first update
        self.update_status()
        self.print_status()

        # continuous
        try:
            while True:
                self.update_status(clear_buffer=False)
                self.print_status(overwrite_last=True)
        except KeyboardInterrupt:
            print()

    def print_messages(self, last_n=None):
        """
            Print messages to screen

            last_n: print the last number of messages
        """

        messages = self.messages
        
        if last_n is not None:
            messages = messages[-last_n:]

        for m, t in messages:
            print(f'{datetime.fromtimestamp(t)}  {m}')

    def print_state(self):
        """
            Print state of the python object
        """
        lines = [f'is_data_streaming:   {self.is_data_streaming}',
                 f'is_field_zeroed:     {self.is_field_zeroed}',
                 f'is_xyz_zeroing:      {self.is_xyz_zeroing}',
                 f'is_calibrated:       {self.is_calibrated}',
                 f'axis_mode:           {self.axis_mode}',
                 f'read_axis:           {self.read_axis}',
                 f'gain:                {self.gain} V/nT',
                 ]
        print('\n'.join(lines), flush=True)

    def print_status(self, update=False, overwrite_last=False):
        """
            Print status of QuSpin in a nicely formatted message

            update: if true, update before printing
            overwrite_last: if true, overwrite the last message. Used in monitor_status
        """

        # look for print before update
        if update or self.status_last_updated is None:
            self.update_status()

        # format output
        lines = ['',
                 f'Last updated: {datetime.fromtimestamp(self.status_last_updated)}',
                 '',
                 f'Field zeroed:    {self.led["field zeroed (LED4)"]}',
                 f'Laser lock:      {self.led["laser lock (LED3)"]}',
                 f'Cell T lock:     {self.led["cell temp lock (LED2)"]}',
                 f'Laser on:        {self.led["laser on (LED1)"]}',
                 '',
                 f'Cell T error:    {self.sensor_par["cell temp error"]:.5g}',
                 #f'Cell T voltage:  {self.sensor_par["cell temp voltage"]}',
                 f'Bz field:        {self.sensor_par["Bz field (pT)"]:.4f} pT',
                 f'By field:        {self.sensor_par["By field (pT)"]:.4f} pT',
                 f'B0 field:        {self.sensor_par["B0 field (pT)"]:.4f} pT',
                 ]
        
        # add white space incase overwrite has fewer characters
        lines = [line+' '*10 for line in lines]
    
        # do print
        if overwrite_last:
            print("\033[F"*(len(lines)) + '\n'.join(lines))
        else:
            print('\n'.join(lines), flush=True)

    def set_axis_mode(self, mode='z'):
        """
            Change field-sensitive axis

            Note: triaxial sensors do not respond to this command

            mode =  z       Operate the magnetometer in single Z axis mode
                    y       Operate the magnetometer in single Y axis mode
                    dual    Operate the magnetometer in dual Y and Z axis mode
        """

        mode = mode.lower().strip()
        if mode == 'z':     
            self.ser.write(b'C')
        elif mode == 'y':   self.ser.write(b'F')
        elif mode == 'dual':self.ser.write(b'B')
        else:
            raise RuntimeError('Bad mode: must be one of "z", "y", or "dual".')
        
        self.axis_mode = mode
        self.is_calibrated = False
        self.is_field_zeroed = False
        self.update_status()

    def read_data(self, npts, axis='z', clear_buffer=True):
        """
            Read data from the device 

            npts:           int, number of data points to read
            axis:           str, which axis to read from (x, y, or z)
            clear_buffer:   bool, if true, clear buffer and wait for new

            assumed readback rate based on comments from QuSpin
            time[0] is the time immediately after clearing the buffer. 
                Note that there is often an incomplete word after clear, we ignore this
                As a result the error in time is at most 1/self.data_read_rate

            returns (time, field)
        """

        # switch axis
        self._set_read_axis(axis)

        # start data stream
        if not self.is_data_streaming:
            self._set_data_stream()

        # get number of bytes to read
        # +2 bytes for \r and \n
        # +2 points since first and last are often partial
        nbytes = (self.serial_settings['bytesize']+2) * (npts+2)

        # clear buffer
        if clear_buffer:
            self.ser.reset_input_buffer()

        # take data
        time_start = time()
        message = self.ser.read(nbytes)

        # clean up message to data format
        message = message.decode('utf-8')
        message = message.replace('\x00', '')
        message = message.replace('\r', '')
        message = message.replace('!', '')
        message = message.strip().split('\n')[1:-1]
        
        # check for bad byte lengths in message
        good_data = (np.array([len(m) for m in message]) == self.serial_settings['bytesize']-1)

        # convert to numeric data
        data = np.array(message).astype(int)
        data = (data - 8388608) * 0.01

        # check number of points 
        if len(data) > npts: 
            data = data[:npts]
            good_data = good_data[:npts]

        assert npts == len(data), f"Readback data length incorrect: npts != len(data) ({npts} != {len(data)})"

        # interpolate times
        times = np.arange(npts)/self.data_read_rate + time_start

        # convert bad data to nan
        data[~good_data] = np.nan

        # save data
        self.time = times
        self.field = data

        return (self.time, self.field)
    
    def reboot(self):
        """
            Reboot the microprocessor and reloads the firmware
        """
        self.ser.write(b'e')
        self.update_status()
        self._reset_attributes()

    def set_gain(self, mode='1x'):
        """
            Set analog gain (analog output only)

            mode =  0.33x   Set the analog output gain to 0.33 times default (0.9 V/nT)
                    1x      Set the analog output gain to default (2.7 V/nT)
                    3x      Set the analog output gain to 3 times default (8.1 V/nT)
        """
        
        mode = mode.lower().strip()
        if mode == '0.33x': 
            self.ser.write(b'a')
            self.gain = 0.9     # V/nT

        elif mode == '1x':  
            self.ser.write(b'`')
            self.gain = 2.7     # V/nT

        elif mode == '3x':  
            self.ser.write(b'b')
            self.gain = 8.1     # V/nT

    def to_csv(self, filename=None):
        """
            Write data to csv, if no filename, use default
        """
        
        # set default file name
        if filename is None:
            t = datetime.now()
            filename = f'qzfm_{datetime.strftime("%y%m%d%H%M%S")}.csv'
        
        # make dataframe
        df = pd.DataFrame({'time (epoch)':self.time, f'{self.read_axis} field (pT)':self.field})
        
        self.update_status()
        
        # write file header
        header = [ '# QZFM (QuSpin Zero Field Monitor) data',
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
                  f'# {datetime.now()}',
                   '# \n',
                 ]
        with open(filename, 'w') as fid:
            fid.write('\n'.join(header))
        
        # write data
        df.to_csv(filename, mode='a', index=False)
                 

    def update_status(self, clear_buffer=True):
        """
            Clear input buffer and read status
            
            updates the following attributes: 
                self.status_last_updated
                self.led
                self.sensor_par
                self.messages
        """

        # change to status readback
        if self.is_data_streaming:
            self._set_data_stream(False)

        # set update time
        message = self._read_serial(self.nbytes_status, clear_buffer=clear_buffer)
        self.status_last_updated = time()
        
        # look for unique codes starting from the end
        codes = []
        codes_uniq = []
        for m in message[::-1]:
            if m[:3] not in codes_uniq:
                codes.append(m)
                codes_uniq.append(m[:3])

        # set values based on code types
        sp = {}
        led = {}
        for code in codes: 
            
            # code has no length
            if not code: continue

            # LED
            if code[0] == '|':
                if   code[1] == '1':  led['laser on (LED1)'] = code[2] == '1'
                elif code[1] == '2':  led['cell temp lock (LED2)'] = code[2] == '1'
                elif code[1] == '3':  led['laser lock (LED3)'] = code[2] == '1'
                elif code[1] == '4':  led['field zeroed (LED4)'] = code[2] == '1'
                elif code[1] == '5':  led['is master'] = code[2] == '1'
            
            # readback parameters
            elif code[0] == '~':
                if code[3:].replace('.', '').isnumeric():
                    if   code[1:3] == '04':   sp['cell temp error'] = (float(code[3:])-8388608)/524288
                    elif code[1:3] == '05':   sp['cell temp voltage'] = int(code[3:])
                    elif code[1:3] == '07':   sp['Bz field (pT)'] = (float(code[3:])-32768)*0.01
                    elif code[1:3] == '08':   sp['By field (pT)'] = (float(code[3:])-32768)*0.01
                    elif code[1:3] == '09':   sp['B0 field (pT)'] = (float(code[3:])-32768)*0.01

            # messages
            elif code[0] == '#':
                self.messages.append((code[1:], self.status_last_updated))

        # reset field dicts and update
        for k in self.led.keys():
            self.led[k] = led.get(k, False)
        
        for k in self.sensor_par.keys():
            if 'field' in k:
                self.sensor_par[k] = sp.get(k, self.sensor_par[k])
            else:
                self.sensor_par[k] = sp.get(k, np.nan)
        
    @property
    def laser_on(self):
        self.update_status()
        return self.led['laser on (LED1)']
    
    @property
    def cell_Tlock(self):
        self.update_status()
        return self.led['cell temp lock (LED2)']
    
    @property
    def laser_locked(self):
        self.update_status()
        return self.led['laser lock (LED3)']
    
    @property
    def field_zeroed(self):
        self.update_status()
        return self.led['field zeroed (LED4)']

    @property
    def is_master(self):
        self.update_status()
        return self.led['is_master']
