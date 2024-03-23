#### HASP 2024 TESTING CODE ####

#### IMPORTS ####

import RPi.GPIO as GPIO
import time
import os, sys
sys.path.append(os.path.dirname(__file__))

from Motor import Motor
from Photodiode import Photodiode
from TempSensors import TempSensors
from Utils import *

#### GLOBAL VARIABLES ####

PIN_MOTOR_ENA = 17
PIN_MOTOR_STEP = 27
PIN_MOTOR_DIR = 22
PIN_PHOTODIODE_A = 15
PIN_PHOTODIODE_B = 14
PIN_PHOTODIODE_C = 24
PIN_PHOTODIODE_D = 23
PIN_PHOTODIODE_CLK = 18
PIN_TEMP = 4

LoopItersMax = 10
MotorStepDelay = 1000
MotorCurrentRun = 16
MotorCurrentHold = 16
MotorMicrosteps = 4
MotorSPIBus = 0
MotorSPIDevice = 0
MotorSPISpeed = 2000000
PhotodiodeSensitivity = 0.4
PhotodiodeDelayClk = 5
TempSensorsNum = 4

# DO NOT CHANGE

LoopIters = 0

#### MAIN FUNCTIONS ####

def main() -> None:
    global LoopIters

    print("---- SCRIPT STARTED ----\n")

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    motor = Motor(PIN_MOTOR_ENA, PIN_MOTOR_STEP, PIN_MOTOR_DIR, MotorSPIBus, MotorSPIDevice, MotorSPISpeed, MotorCurrentRun, MotorCurrentHold, MotorMicrosteps)
    while (motor.Init() != 0):
        print("Failed to initialize motor! Retrying...")
        DelaySeconds(1)
    print("Successfully initialized motor!")

    photodiodes = [Photodiode(PIN_PHOTODIODE_A, PIN_PHOTODIODE_CLK, PhotodiodeDelayClk, PhotodiodeSensitivity), 
                   Photodiode(PIN_PHOTODIODE_B, PIN_PHOTODIODE_CLK, PhotodiodeDelayClk, PhotodiodeSensitivity), 
                   Photodiode(PIN_PHOTODIODE_C, PIN_PHOTODIODE_CLK, PhotodiodeDelayClk, PhotodiodeSensitivity), 
                   Photodiode(PIN_PHOTODIODE_D, PIN_PHOTODIODE_CLK, PhotodiodeDelayClk, PhotodiodeSensitivity)]
    while (True):
        error = False
        for photodiode in photodiodes:
            if (photodiode.IsInitialized() is False):
                if (photodiode.Init() is False):
                    print("Failed to initialize a photodiode! Retrying...")
                    DelaySeconds(1)
                    error = True
                    break
        if (error is False):
            break
    print("Successfully initialized photodiodes!")

    tempSensors = TempSensors(PIN_TEMP, TempSensorsNum)
    while (tempSensors.Init() != 0):
        print("Failed to initialize temperature sensors! Retrying...")
        DelaySeconds(1)
    print("Successfully initialized temperature sensors!")

    while (LoopIters < LoopItersMax):
        startTime = time.time()
        temps = tempSensors.Read()
        print("Temp Sensors read time: " + str(time.time() - startTime))
        print("Temperatures: " + str(temps))

        lights = []
        for photodiode in photodiodes:
            lights.append(photodiode.Read())
        print(lights)

        print("Driver status: " + ByteToBin(motor.GetStatus()))
        print("Driver temp: " + str(motor.GetTemp()))
        motor.Run(200, 0, 1000)
        motor.Run(200, 1, 1000)

        DelaySeconds(1)
        LoopIters += 1

    print("\n---- SCRIPT FINISHED ----")

if (__name__ == "__main__"):
    main()