from onavi import ONavi
import time

sensor = ONavi("/dev/ttyACM0", scaled_values=True, log=True, real_time_plot=False)
while True:
    try:
        reading = sensor.read()  # reads the values returned by the sensor and converts them to m/s/s
        print(reading.to_tuple())
        time.sleep(.019)
    except KeyboardInterrupt:
        sensor.close()
        break
