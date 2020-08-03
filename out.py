import csv
import os
import sys
import time
from datetime import datetime

try:
    import pyqtgraph as pg
except ImportError:
    raise ImportError("install pyqtgraph to use this library")

try:
    from numpy import linspace
except ImportError:
    raise ImportError("install numpy to use this library")

from pyqtgraph.Qt import QtGui


class Output:
    def __init__(self, parent) -> None:
        self.x = .0
        self.y = .0
        self.z = .0
        self.time = .0

        self.__parent = parent
        self.__log_file_name = ""
        self.__x = []
        self.__y = []
        self.__z = []
        self.__time = []
        self._date = None

        if self.__parent.real_time_plot:
            self.app = QtGui.QApplication(sys.argv)

            self.win = pg.GraphicsWindow(title="Sensor Live Plot")
            self.win.ci.layout.setContentsMargins(0, 0, 0, 0)

            self.x_axis = self.win.addPlot(title="X", row=0, col=0)
            self.curve_x = self.x_axis.plot()

            self.y_axis = self.win.addPlot(title="Y", row=1, col=0)
            self.curve_y = self.y_axis.plot()

            self.z_axis = self.win.addPlot(title="Z", row=2, col=0)
            self.curve_z = self.z_axis.plot()

            self.windowWidth = 200
            self.Xm = linspace(0, 0, self.windowWidth)
            self.Ym = linspace(0, 0, self.windowWidth)
            self.Zm = linspace(0, 0, self.windowWidth)
            self.Timem = linspace(0, 0, self.windowWidth)
            self.ptr = -self.windowWidth

        if self.__parent.log:
            self.__init_log_file()

    def to_tuple(self) -> tuple:
        self.__x.append(self.x)
        self.__y.append(self.y)
        self.__z.append(self.z)
        self.__time.append(self.time)

        if self.__parent.real_time_plot:
            self.__real_time_plot()

        if self.__parent.log and len(self.__x) >= 50:
            self.log_file()
            self.__x = []
            self.__y = []
            self.__z = []
            self.__time = []

            if time.time() - self.__parent.start_time >= \
                    self.__parent.split_every:
                self.__init_log_file()
                self.__parent.start_time = time.time()

        return self.time, self.x, self.y, self.z

    def to_g(self) -> tuple:
        self.__x.append(self.x / 9.80665)
        self.__y.append(self.y / 9.80665)
        self.__z.append(self.z / 9.80665)
        self.__time.append(self.time)

        if self.__parent.real_time_plot:
            self.__real_time_plot()

        if self.__parent.log and \
                len(self.__x) >= 50:  # save every 50 samples +- 1s
            self.log_file()
            self.__x = []
            self.__y = []
            self.__z = []
            self.__time = []
            if time.time() - self.__parent.start_time >= \
                    self.__parent.split_every:  # split file every 1800s
                self.__init_log_file()

        return self.time, self.x / 9.80665, self.y / 9.80665, self.z / 9.80665

    def __real_time_plot(self) -> None:
        self.Timem[:-1] = self.Timem[1:]
        self.Timem[-1] = self.time

        self.Xm[:-1] = self.Xm[1:]
        self.Xm[-1] = self.x

        self.Ym[:-1] = self.Ym[1:]
        self.Ym[-1] = self.y

        self.Zm[:-1] = self.Zm[1:]
        self.Zm[-1] = self.z

        self.ptr += 1
        self.curve_x.setData(self.Timem, self.Xm)
        self.curve_x.setPos(self.ptr, 0)

        self.curve_y.setData(self.Timem, self.Ym)
        self.curve_y.setPos(self.ptr, 0)

        self.curve_z.setData(self.Timem, self.Zm)
        self.curve_z.setPos(self.ptr, 0)
        QtGui.QApplication.processEvents()

    def __init_log_file(self) -> None:
        self.__date = datetime.today().strftime("%d-%m-%Y")

        if not os.path.exists("data"):
            os.mkdir("data")

        if not os.path.exists(f"data/{self.__date}"):
            os.mkdir(f"data/{self.__date}")

        self.__log_file_name = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        self.start_time = time.time()

        with open(f'data/{self.__date}/{self.__log_file_name}.csv',
                  newline='', mode="w") as f:
            writer = csv.writer(f)
            writer.writerow(['startTime', self.start_time])
            writer.writerow(['time', 'x', 'y', 'z'])

    def log_file(self) -> None:
        if not os.path.exists(f'data/{self.__date}/{self.__log_file_name}.csv'):
            self.__init_log_file()

        with open(f'data/{self.__date}/{self.__log_file_name}.csv',
                  newline='', mode="a") as f:
            writer = csv.writer(f)
            for t, x, y, z in zip(self.__time, self.__x, self.__y, self.__z):
                writer.writerow([t, x, y, z])
