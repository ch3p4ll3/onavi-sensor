# onavi-sensor
Python library for reading and logging data read by an ONAVI seismic sensor

## How it works
The library opens a serial communication with the sensor(115.2K baud, 8 bytes, no parity, 1 sto bt, dtr control enable, rts control enable, flow control disable) and by sending 0x2a the sensor returns raw data.
The subsequent read from the COM port should yield the ONavi data as a string formatted \**XXYYZZC, the first two characters are \** for the 12-bit sensor and ## for the 16-bit sensor and $$ for 24-bit sensor.  
