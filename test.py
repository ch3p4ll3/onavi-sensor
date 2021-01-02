from onavi import ONavi
import time
from get_port import get_sensor_path


dev_path = get_sensor_path()

if dev_path is not None:
    sensor = ONavi(dev_path, scaled_values=True,
                   log=True, real_time_plot=False)
else:
    exit()

while True:
    try:
        reading = sensor.read()
        # reads the values returned
        # by the sensor and converts them to m/s/s
        reading.to_tuple()
        time.sleep(.019)
    except KeyboardInterrupt:
        sensor.close()
        break
