from onavi_sensor import OnaviSensor
from onavi_sensor.measurement import MssMeasurement
from typing import Optional, List
from datetime import datetime
from pathlib import Path
from statistics import mean
import csv
import os
import time


class Logger:
    def __init__(self, sensor: OnaviSensor, scaled_values: Optional[bool] = True, split_every: Optional[int] = 1800):
        self.sensor = sensor
        self.scaled_value = scaled_values
        self.split_every = split_every
        self.__data: List[MssMeasurement] = []

    def __enter__(self):
        self.__init_folder__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.scaled_value:
            means = self.axes_mean
            self.__data = list(map(lambda x: self.__scale_values(x, means), self.__data))
        self.__save_file()

    def __save_file(self):
        with open(self.file_path, newline='', mode="w") as f:
            writer = csv.writer(f)

            writer.writerow(['time', 'x', 'y', 'z'])
            writer.writerows((x.to_list for x in self.__data))

    def __init_folder__(self):
        year = datetime.today().year
        month = f"{datetime.today().month} - {datetime.today().strftime('%B')}"
        date = datetime.today().strftime("%d-%m-%Y")

        if not os.path.exists("data"):
            os.mkdir("data")

        if not os.path.exists(f"data/{year}"):
            os.mkdir(f"data/{year}")

        if not os.path.exists(f"data/{year}/{month}"):
            os.mkdir(f"data/{year}/{month}")

        if not os.path.exists(f"data/{year}/{month}/{date}"):
            os.mkdir(f"data/{year}/{month}/{date}")

        self.file_path = Path(f"data/{year}/{month}/{date}/{datetime.now().strftime('%H-%M-%S')}.csv")
    
    @property
    def axes_mean(self) -> MssMeasurement:
        x_mean = mean((x.x for x in self.__data))
        y_mean = mean((x.y for x in self.__data))
        z_mean = mean((x.z for x in self.__data))

        return MssMeasurement(x_mean, y_mean, z_mean, 0)

    def __scale_values(self, row: MssMeasurement, means: MssMeasurement) -> MssMeasurement:
        row.x = row.x - means.x
        row.y = row.y - means.y
        row.z = row.z - means.z

        return row

    def loop(self):
        self.__start_time = time.time()

        with self.sensor as sensor:
            while True:
                if time.time() - self.__start_time >= self.split_every:
                    #reset
                    if self.scaled_value:
                        means = self.axes_mean
                        self.__data = list(map(lambda x: self.__scale_values(x, means), self.__data))

                    self.__save_file()  # <- 4/5s to save, make it async
                    self.__init_folder__()
                    self.__data = []
                    self.__start_time = time.time()

                measurement = sensor.read()

                self.__data.append(measurement)
                time.sleep(.005)
