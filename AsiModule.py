from calendar import day_name
import zwoasi
import cv2
import numpy
import json
import Motor
import Photodiode

with open("COC_HASP\\config.json",'r') as f:
    config=json.load(f) #exposure units in ms
    

def init_zwo_library(self):
        zwoasi.init("C:\\Users\\guhao\\OneDrive\\Desktop\\HASP\\ASICamera2.dll")
        return 0

def get_num_cameras(self):
        return zwoasi.get_num_cameras()

def get_guide_image(self,type="guide")->tuple:
    match type:
        case "guide":
            type="ZWO ASI678MC" #camera name for guide
            gain=config[0]["gain"] #get gain for guide
            exposure=config[0]["exposure"] #get exposure for guide
            resx=config[0]["resx"] #get x resolution
            resy=config[0]["resy"] #get y resolution
        case "science": #same as guide but for science camera
            type="ZWO ASI585MC"
            gain=config[1]["gain"]
            exposure=config[1]["exposure"]
            resx=config[1]["resx"]
            resy=config[1]["resy"]
        case _:
            return 0, 1
    camera_id=zwoasi.list_cameras().index(type)
    camera = zwoasi.Camera(camera_id)
    camera.set_image_type(zwoasi.ASI_IMG_RAW8)
    #camera.set_control_value(zwoasi.ASI_GAIN, gain) #set gain
    #camera.set_control_value(zwoasi.ASI_EXPOSURE, exposure) #set exposure
    camera.start_exposure()
    camera_status = camera.get_exposure_status()
    while camera_status == 1:
        camera_status = camera.get_exposure_status()
    if camera_status == 2:
        img_array = camera.get_data_after_exposure()
        from PIL import Image
        img_from_guide_camera = Image.frombuffer("L", (resx, resy), img_array)
        ocv_image = cv2.cvtColor(numpy.array(img_from_guide_camera), cv2.COLOR_RGB2BGR)
        camera.close()
        return ocv_image, 0
    elif  camera_status == 3:
        camera.close()
        return 0, 1
    else:
        camera.close()
        return 0, 1

def get_guide_image_from_file(self):
    img_array = cv2.imread("SunPic01.jpg")
    from PIL import Image
    img_from_guide_camera = Image.frombuffer("L", (3840, 2160), img_array)
    ocv_image = cv2.cvtColor(numpy.array(img_from_guide_camera), cv2.COLOR_RGB2BGR)
    return ocv_image, 0
