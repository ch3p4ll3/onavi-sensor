try:
    import serial
except ImportError:
    raise ImportError("You need to install pyserial to make ONavi work")
import time

from out import Output


class ONavi:
    def __init__(self, port, log=False, scaled_values=True,
                 split_every=1800, real_time_plot=False) -> None:
        self.port = port
        self.start_time = time.time()
        self.log = log
        self.scaled_values = scaled_values
        self.real_time_plot = real_time_plot

        if split_every <= 0 and log:
            raise ValueError("split_every must be greater than 0!")
        self.split_every = split_every

        self.__log_file_name = ""
        self.__x_offset = 0
        self.__y_offset = 0
        self.__z_offset = 0

        self.__out_obj = Output(self)

        try:
            self.__ser = serial.Serial(port=self.port, baudrate=115200)
            self.__ser.rts = True
            self.__ser.dtr = True
            self.__ser.flush()
            if self.scaled_values:
                self.__calibration()
                self.start_time = time.time()
        except serial.SerialException as e:
            print(e)
            self.__ser = None

    def __calibration(self) -> None:
        print("Calibration in progress, don't touch the sensor")
        counter = 0
        x = []
        y = []
        z = []

        while counter <= 100:
            reading = self.read()
            x.append(reading.x)
            y.append(reading.y)
            z.append(reading.z)
            counter += 1

        self.__x_offset = sum(x) / len(x)
        self.__y_offset = sum(y) / len(y)
        self.__z_offset = sum(z) / len(z)

        print("Calibration succesfull")

    def __parse_input(self, incoming) -> Output:
        FLOAT_ONAVI_FACTOR = 7.629394531250e-05
        EARTH_G = 9.78033

        x = (incoming[2] * 255) + incoming[3]
        y = (incoming[4] * 255) + incoming[5]
        z = (incoming[6] * 255) + incoming[7]

        x1 = (x - 32768.0) * FLOAT_ONAVI_FACTOR * EARTH_G
        y1 = (y - 32768.0) * FLOAT_ONAVI_FACTOR * EARTH_G
        z1 = (z - 32768.0) * FLOAT_ONAVI_FACTOR * EARTH_G
        time_passed = time.time() - self.start_time

        if self.__out_obj is not None:
            self.__out_obj.x = x1 - self.__x_offset
            self.__out_obj.y = y1 - self.__y_offset
            self.__out_obj.z = z1 - self.__z_offset
            self.__out_obj.time = time_passed

        return self.__out_obj

    def read(self) -> Output:
        if self.__ser is not None:
            self.__ser.write(b'\x2a')
            incoming = self.__ser.read(9)
            parsed = self.__parse_input(incoming)
            time.sleep(.019)

            return parsed

    def close(self) -> None:
        if self.__ser is not None:
            if self.log:
                self.__out_obj.log_file()
            self.__ser.close()
