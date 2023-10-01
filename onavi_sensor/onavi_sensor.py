from typing import Optional
from .utils import Utils
import serial
from .measurement import MssMeasurement
import time


class OnaviSensor:
    def __init__(self, serial_port: Optional[str] = None):
        if serial_port is None:
            serial_port = Utils.get_sensor_serial_port()
        self.serial_port = serial_port
    
    def __enter__(self):
        self.init_serial()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__serial.close()

    def init_serial(self):
        self.__serial = serial.Serial(port=self.serial_port, baudrate=115200)
        self.__serial.rts = True
        self.__serial.dtr = True
        self.__serial.flush()
    
    def read_raw(self):
        self.__serial.write(b'\x2a')
        return self.__serial.read(9)

    def read(self) -> MssMeasurement:
        incoming = self.read_raw()

        FLOAT_ONAVI_FACTOR = 7.629394531250e-05
        EARTH_G = 9.78033

        x_axes = (incoming[2] * 255) + incoming[3]
        y_axes = (incoming[4] * 255) + incoming[5]
        z_axes = (incoming[6] * 255) + incoming[7]

        x = (x_axes - 32768.0) * FLOAT_ONAVI_FACTOR * EARTH_G
        y = (y_axes - 32768.0) * FLOAT_ONAVI_FACTOR * EARTH_G
        z = (z_axes - 32768.0) * FLOAT_ONAVI_FACTOR * EARTH_G

        return MssMeasurement(x, z, y, time.time())
