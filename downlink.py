import serial
import struct
import time

def downlink(record_type: int,unix_time: float,port: serial.serialwin32.Serial) -> None:
    sec=int(unix_time)
    ns=int((unix_time-sec)*10**9)
    bytes=struct.pack('3i',record_type,sec,ns)
    while True:
        if(port.is_open):
            try:
                port.write(bytes)
                print('downlink sent')
                port.close()
            except:
                print('could not write to ',port)
            break
        else:
            print(port,' is not open')
            break