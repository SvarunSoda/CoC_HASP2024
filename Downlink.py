import serial
import time

ser=serial.Serial(port="COM2", baudrate=9600, bytesize=8, timeout=5, stopbits=serial.STOPBITS_ONE, parity='N')
def output(ser, temps, num_img, stats, imgs_accquired, volts):
    b=bytearray(20)
    b[0:1]=b'\x01' #start symbol
    b[1:9]=bytes(temps) #temperature
    b[9:11]=num_img.to_bytes(2,'big') #number of images
    b[11:14]=bytes(stats) #tracking status, last command status, heartbeat
    b[14:16]=imgs_accquired.to_bytes(2,'big') #images accquired
    b[16:18]=bytes(volts) #5volt voltage, 12 volt voltage
    b[18:20]=b'\x0a\x0d' #end symbol
    ser.write(b)
    print("sent")
for _ in range(10):
    output(ser,(12,13,12,14,12,19,8,19),192,(1,2,3),67,(2,4))
    time.sleep()
ser.close()
