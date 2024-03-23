#### HASP 2024 PHOTODIODE CODE ####

#### IMPORTS ####

import RPi.GPIO as GPIO
import os, sys
sys.path.append(os.path.dirname(__file__))

from Utils import *

#### CLASSES ####

class Photodiode:
    def __init__(self, pinDataValue: int, pinClkValue: int, delayClkValue: float, sensitivityValue: float) -> None:
        self.pinData = pinDataValue
        self.pinClk = pinClkValue
        self.delayClk = delayClkValue
        self.sensitivity = sensitivityValue
        self.__initialized = False

    def Read(self) -> bool:
        if (self.__initialized is False): 
            raise Exception("ERROR: Attempting to read a photodiode that has not been initialized!")
        GPIO.output(self.pinClk, 0)
        DelayMilliseconds(self.delayClk)
        GPIO.output(self.pinClk, 1)
        DelayMilliseconds(self.delayClk * self.sensitivity)
        res = GPIO.input(self.pinData)
        DelayMilliseconds(self.delayClk * (1.0 - self.sensitivity))
        GPIO.output(self.pinClk, 0)
        return res

    def Init(self) -> bool:
        if (self.sensitivity < 0.0) or (self.sensitivity > 1.0): 
            return False
        GPIO.setup(self.pinData, GPIO.IN)
        GPIO.setup(self.pinClk, GPIO.OUT)
        self.__initialized = True
        return True

    def IsInitialized(self) -> bool:
        return self.__initialized