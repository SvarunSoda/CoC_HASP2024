import zwoasi
import cv2
import numpy

def init_zwo_library():
    zwoasi.init('/home/vahid/Downloads/ASI_Camera_SDK/ASI_linux_mac_SDK_V1.33/lib/armv8/libASICamera2.so')
    return 0

def get_num_cameras():
    return zwoasi.get_num_cameras()

def get_guide_image():
    camera = zwoasi.Camera(0)
    camera.set_image_type(zwoasi.ASI_IMG_RAW8)
    camera.start_exposure()
    camera_status = camera.get_exposure_status()
    while camera_status == 1:
        camera_status = camera.get_exposure_status()
    if camera_status == 2:
        img_array = camera.get_data_after_exposure()
        from PIL import Image
        img_from_guide_camera = Image.frombuffer("L", (1280, 960), img_array)
        ocv_image = cv2.cvtColor(numpy.array(img_from_guide_camera), cv2.COLOR_RGB2BGR)
        camera.close()
        return ocv_image, 0
    elif  camera_status == 3:
        camera.close()
        return 0, 1
    else:
        camera.close()
        return 0, 1

def get_guide_image_from_file():
    img_array = cv2.imread("SunPic01.jpg")
    from PIL import Image
    img_from_guide_camera = Image.frombuffer("L", (1280, 960), img_array)
    ocv_image = cv2.cvtColor(numpy.array(img_from_guide_camera), cv2.COLOR_RGB2BGR)
    return ocv_image, 0
