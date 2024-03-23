#### HASP 2024 UTILITIES CODE ####

#### IMPORTS ####

import time

#### FUNCTIONS ####

def DelayMicroseconds(us: float) -> None:
    time.sleep(us / 1000000.0)

def DelayMilliseconds(ms: float) -> None:
    time.sleep(ms / 1000.0)

def DelaySeconds(s: float) -> None:
    time.sleep(s)

def ByteToBin(num: bytes) -> str:
    return NumToBin(num, 8)

def Int32ToBin(num: int) -> str:
    return NumToBin(num, 32)

def NumToBin(num: any, size: int) -> str:
    numStr = ""
    for i in range(size):
        numStr += str((num >> (size - 1 - i)) & 1)
    return numStr