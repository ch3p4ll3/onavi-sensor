from onavi import ONavi

sensor = ONavi("/dev/ttyACM0", scaled_values=True, log=True, real_time_plot=False)
while True:
    try:
        reading = sensor.read()  # reads the values returned by the sensor and converts them to m/s/s
        mss = reading.to_tuple()  # puts the values in a tuple (time passed since the start of the readings, x, y, z)
        g = reading.to_g()  # converts values from m/s/s to g
    except KeyboardInterrupt:
        sensor.close()
        break
