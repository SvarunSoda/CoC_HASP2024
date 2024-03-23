#### HASP 2024 STEPPER MOTOR CODE ####

#### IMPORTS ####

import RPi.GPIO as GPIO
import spidev
import os, sys
sys.path.append(os.path.dirname(__file__))

from Utils import *

#### CLASSES ####

class Motor:
    def __init__(self, pinEnaValue: int, pinStepValue: int, pinDirValue: int, spiBusValue: int, spiDeviceValue: int, spiSpeedValue: int, currentRunValue: int, currentHoldValue: int, microstepsValue: int) -> None:
        self.pinEna = pinEnaValue
        self.pinStep = pinStepValue
        self.pinDir = pinDirValue
        self.spiBus = spiBusValue
        self.spiDevice = spiDeviceValue
        self.spiSpeed = spiSpeedValue
        self.currentRun = currentRunValue
        self.currentHold = currentHoldValue
        self.microsteps = microstepsValue
        self.__spiLine = None
        self.__initialized = False

    def GetStatus(self) -> bytes:
        if (self.__initialized is False): 
            raise Exception("ERROR: Attempting to get status of a motor that hasn't been initialized!")
        return self.__RegRead(0x00)[0]

    def GetTemp(self) -> float:
        if (self.__initialized is False): 
            raise Exception("ERROR: Attempting to get temperature of a motor that hasn't been initialized!")
        return ((self.__RegRead(0x51)[1] & 0x00001FFF) - 2038) / 7.7 

    def Run(self, steps: int, dir: bool, stepDelay: int) -> None:
        if (self.__initialized is False): 
            raise Exception("ERROR: Attempting to run a motor that hasn't been initialized!")
        GPIO.output(self.pinDir, dir)
        for i in range(steps):
            GPIO.output(self.pinStep, 1)
            DelayMicroseconds(stepDelay)
            GPIO.output(self.pinStep, 0)
            DelayMicroseconds(stepDelay)

    def Init(self) -> int:
        try:
            self.__spiLine = spidev.SpiDev()
            self.__spiLine.open(self.spiBus, self.spiDevice)
            self.__spiLine.max_speed_hz = self.spiSpeed
            self.__spiLine.mode = 0x03
        except FileNotFoundError:
            return 1
        ms = None
        match self.microsteps:
            case 128: ms = 0x1
            case 64: ms = 0x2
            case 32: ms = 0x3
            case 16: ms = 0x4
            case 8: ms = 0x5
            case 4: ms = 0x6
            case 2: ms = 0x7
            case 1: ms = 0x8
            case _: ms = 0x0
        self.__RegWrite(0x6C, int(0x10410155 | (ms << 24)))                                                   # Setting TOFF flag & microsteps...
        self.__RegWrite(0x10, int(0x00060000 | ((self.currentRun & 0x1F) << 8) | (self.currentHold & 0x1F)))  # Setting running & holding current...
        reply = self.__RegRead(0x6C)
        if ((reply[1] & 0x0000000F) != 0x05):
            return 2
        GPIO.setup(self.pinEna, GPIO.OUT)
        GPIO.setup(self.pinStep, GPIO.OUT)
        GPIO.setup(self.pinDir, GPIO.OUT)
        GPIO.output(self.pinEna, 0)
        self.__initialized = True
        return 0

    def IsInitialized(self) -> bool:
        return self.__initialized

    def __RegWrite(self, address: bytes, data: int) -> None:
        self.__SPIExchange([address | 0x80, (data >> 24) & 0xFF, (data >> 16) & 0xFF, (data >> 8) & 0xFF, data & 0xFF])

    def __RegRead(self, address: bytes) -> list:
        self.__SPIExchange([address, 0x00, 0x00, 0x00, 0x00])
        reply = self.__SPIExchange([address, 0x00, 0x00, 0x00, 0x00])
        return [reply[0], int((reply[1] << 24) | (reply[2] << 16) | (reply[3] << 8) | reply[4])]

    def __SPIExchange(self, data: list[bytes]) -> list[bytes]:
        return self.__spiLine.xfer3(data)