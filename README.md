# onavi-sensor
Python library for reading and logging data read by an ONAVI seismic sensor

## How it works
The library opens a serial communication with the sensor(115.2K baud, 8 bytes, no parity, 1 sto bt, dtr control enable, rts control enable, flow control disable) and by sending 0x2a the sensor returns raw data.
The subsequent read from the COM port should yield the ONavi data as a string formatted **XXYYZZC, the first two characters are ** for the 12-bit sensor and ## for the 16-bit sensor and $$ for 24-bit sensor.  

### ONavi class
|   Method   |  Return type |                                                                                                                                        Description                                                                                                                                                                  |
| ---------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ONavi      | ONavi object | Constructor of the object. You can choose to scale the values (sensor calibration: reads 100 values, averages and subtracts the average from new readings), log the readings on a csv file, show the readings on a graph and finally choose every how many seconds to split the log file (default: 1800s aka 30min) |
| read       | Output       | reads the values sent by the sensors and puts them on an Output type object                                                                                                                                                                                                                                         |
| close      | None         | Close the serial and, if you log on to a file, close the file with the latest readings                                                                                                                                                                                                                              |

### Output class
|   Method   |  Return type  |                                               Description                                            |
| ---------- | ------------- | ---------------------------------------------------------------------------------------------------- |
| Output     | Output object | Constructor of the object                                                                            |
| to_tuple   | tuple         | puts the values converted in m/s/s in a tuple (time passed since the start of the readings, x, y, z) |
| to_g       | tuple         | converts values from m/s/s to g                                                                      |
| log_file   | None          | save to a file the last readings (not to use)                                                        |


For more information read [here](https://github.com/carlgt1/qcn/blob/master/doc/onavi_prog.txt)

## Example
Small example of how the code works
``` python
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
```