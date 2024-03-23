#### HASP 2024 TEMPERATURE SENSORS CODE ####

#### IMPORTS ####

import RPi.GPIO as GPIO
import w1thermsensor as W1
import os, sys
sys.path.append(os.path.dirname(__file__))

from Utils import *

#### CLASSES ####

class TempSensors:
    def __init__(self, pinValue: int, numValue: int) -> None:
        self.pin = pinValue
        self.num = numValue
        self.__type = W1.Sensor.DS18B20
        self.__sensors = None
        self.__initialized = False

    def Read(self) -> list[float]:
        if (self.__initialized is False): 
            raise Exception("ERROR: Attempting to read temperature sensor(s) that have not been initialized!")
        sensorList = self.__sensors.get_available_sensors([self.__type])
        temps = [-999] * self.num
        for i in range(len(sensorList)):
            if (i >= self.num): 
                break
            try: 
                temps[i] = sensorList[i].get_temperature()
            except W1.SensorNotReadyError: 
                continue
        return temps

    def Init(self) -> int:
        try: 
            self.__sensors = W1.W1ThermSensor()
        except W1.NoSensorFoundError: 
            return 1
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        self.__initialized = True
        return 0

    def IsInitialized(self) -> bool:
        return self.__initialized
