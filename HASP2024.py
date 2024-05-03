from time import sleep
import numpy
import cv2
import zwoasi
import AsiModule
import GuiderModule
import threading
import serial
import random
import struct
import ModeControl
import keyboard
from RpiMotorLib import RpiMotorLib
import RPi.GPIO
import datetime
import SunPosition

def randint (min= 0x00, max = 0xFF):
    num = random.randbytes(1)
    return num
randint()

ModeControl.init_mode_control()
print(ModeControl.get_system_mode())

def input_module():
    while True:
        #print("Input\n")
        global stop_input_thread
        global command_in
        #serialPort.write(b'A')
        #print(serialPort.read(94))
        bytesread = serialPort.readline()
        #print(bytesread)
        if ((len(bytesread) == 125)  and
            (bytesread[0]   == 0x01) and
            (bytesread[1]   == 0x30) and
            (bytesread[122] == 0x03) and
            (bytesread[123] == 0x0D) and
            (bytesread[124] == 0x0A)):
                print ("GPS Data Received")
                processbuffer = bytesread[2:]
                elements = processbuffer.decode().split(",")
                if ((len(elements) > 1) and elements[1] == "$GPGGA"):
                    #print ("Data: " + elements[2])
                    #print (elements)
                    #for item in elements:
                    #    if (len(item) != 0):
                    #        print (item)
                    localdatetime = datetime.datetime.fromtimestamp(float(elements[0]))
                    utctime = datetime.datetime.strptime(elements[2][:-3],"%H%M%S")
                    print ("Local Time: " + str(localdatetime))
                    print ("UTC Time: " + str(utctime))
                    deltagmt = localdatetime.hour - utctime.hour
                    print ("Delta GMT: " + str(deltagmt))
                    dayoftheyear = localdatetime.timetuple().tm_yday
                    print ("Day of the Year: " + str(dayoftheyear))
                    localtimehours = localdatetime.hour + localdatetime.minute / 60
                    print ("Local Hours: " + str(localtimehours))
                    longitude = float(elements[5][:3]) + float(elements[5][3:]) / 60
                    if (elements[6] == "W"):
                        longitude = -longitude
                    print ("Longitude: " + str(longitude))
                    latitude = float(elements[3][:2]) + float(elements[3][2:]) / 60
                    if (elements[4] == "S"):
                        latitude = -latitude
                    print ("Latitude: " + str(latitude))
                    sp = SunPosition.GetSunPosition(deltagmt, dayoftheyear, longitude, latitude, localtimehours)
                    print ("Sun Position (Elevation, Azimuth): " + str(sp))
                elif (elements[0] != ""):
                    print ("Command: " + str(elements[0][2:4]))
                    command_in = int(elements[0][3:4])
                    #print (str(elements[0][2:4]))
                else:
                    print ("Nothing")    
        #for item in elements:
        #    print (str(item))
        if stop_input_thread:
            serialPort.close()
            break
        #sleep(1.0)
    
def output_module():
    while True:
        print("Output\n")
        global stop_output_thread
        #ba = bytearray(struct.pack("f", randint()))
        #serialPort.write(ba)
        if (serialPort.is_open):
            serialPort.write(randint())
        if stop_output_thread:
            break
        sleep(2.0)
    
def processing_module():
    while True:
        print("Processing\n")
        global command_in
        print(ModeControl.set_system_mode(command_in))
        global stop_processing_thread
        #serialPort.write(b'C')
        if stop_processing_thread:
            break
        sleep(3.0)

command_in = 0

ModeControl.init_mode_control()
print(ModeControl.get_system_mode())

serialPort = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, bytesize=8, timeout=5, stopbits=serial.STOPBITS_ONE, parity='N')
#serialPort = serial.Serial(port='/dev/ttyUSB0')
AsiModule.init_zwo_library()
num_cameras = AsiModule.get_num_cameras()

input_thread = threading.Thread(target=input_module, args=())
processing_thraed = threading.Thread(target=processing_module, args=())
output_thread = threading.Thread(target=output_module, args=())

stop_input_thread = False
stop_output_thread = False
stop_processing_thread = False
    
input_thread.start()
processing_thraed.start()
output_thread.start()

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(16, RPi.GPIO.OUT)
RPi.GPIO.output(16, RPi.GPIO.HIGH)
GPIO_pins = (14, 15, 18)
direction = 20
step = 21
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")

while True:
    ModeControl.mode_control_logic()
    #guider_image, status = AsiModule.get_guide_image()
    guider_image, status = AsiModule.get_guide_image_from_file()
    if status == 0:
        x_err, y_err = GuiderModule.calculate_error(guider_image)
        #print(x_err, y_err)

    if ModeControl.get_system_mode() == ModeControl.SystemMode.HUNT:
        RPi.GPIO.output(16, RPi.GPIO.LOW)
        mymotortest.motor_go(True, "Full", 200, .01, False, .05)

    if ModeControl.get_system_mode() == ModeControl.SystemMode.CENTER:
        RPi.GPIO.output(16, RPi.GPIO.LOW)
        mymotortest.motor_go(True, "Full", 50, .01, False, .05)

    if ModeControl.get_system_mode() == ModeControl.SystemMode.GUIDE:
        RPi.GPIO.output(16, RPi.GPIO.LOW)
        mymotortest.motor_go(True, "Full", 5, .01, False, .05)

    if ModeControl.get_system_mode() == ModeControl.SystemMode.EXIT:
        RPi.GPIO.output(16, RPi.GPIO.HIGH)
        stop_input_thread = True
        stop_output_thread = True
        stop_processing_thread = True
        break
    
print("Done!")

#cv2.destroyAllWindows()
