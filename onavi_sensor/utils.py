import usb.core
import serial.tools.list_ports


class Utils:
    @staticmethod
    def get_sensor_serial_port() -> str:
        dev = usb.core.find(idVendor=0x04e2, idProduct=0x1410)
        port = next(iter(serial.tools.list_ports.comports(dev)), None)

        if port is not None:
            return port.device
