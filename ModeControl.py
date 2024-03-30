from enum import Enum

class SystemMode(Enum):
    UNDEFIND = 0
    INIT = 1
    HUNT = 2
    CENTER = 3
    GUIDE = 4
    COAST = 5
    IDLE = 6
    EXIT = 9

system_mode = SystemMode.UNDEFIND

def init_mode_control():
    global system_mode
    system_mode = SystemMode.INIT

def get_system_mode():
    #global system_mode
    return system_mode

def set_system_mode(mode):
    global system_mode
    match mode:
        case 0:
            system_mode = SystemMode.INIT
        case 1:
            system_mode = SystemMode.HUNT
        case 2:
            system_mode = SystemMode.CENTER
        case 3:
            system_mode = SystemMode.GUIDE
        case 4:
            system_mode = SystemMode.COAST
        case 5:
            system_mode = SystemMode.IDLE
        case 9:
            system_mode = SystemMode.EXIT
        case _:
            system_mode = system_mode
    return system_mode

def mode_control_logic():
    global system_mode
    match system_mode:
        case SystemMode.INIT:
            system_mode = SystemMode.INIT
        case SystemMode.HUNT:
            system_mode = SystemMode.HUNT
        case SystemMode.CENTER:
            system_mode = SystemMode.CENTER
        case SystemMode.GUIDE:
            system_mode = SystemMode.GUIDE
        case SystemMode.COAST:
            system_mode = SystemMode.COAST
        case SystemMode.IDLE:
            system_mode = SystemMode.IDLE
        case SystemMode.EXIT:
            system_mode = SystemMode.EXIT
        case _:
            system_mode = system_mode
    
