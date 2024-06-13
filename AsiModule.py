from calendar import day_name
import zwoasi
import cv2
import numpy
import json
import Motor

class AsiModule:
    def __init__(self, tol_x: int, tol_y: int, delay: int):
        self.tol_x = tol_x
        self.tol_y = tol_y
        self.delay = delay

    with open("COC_HASP\\config.json",'r') as f:
        config=json.load(f) #exposure units in ms

    def init_zwo_library(self):
        zwoasi.init("C:\\Users\\guhao\\OneDrive\\Desktop\\HASP\\ASICamera2.dll")
        return 0

    def get_num_cameras(self):
        return zwoasi.get_num_cameras()

    def get_guide_image(self,type="guide")->tuple:
        global config
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

    def calculate_error(self,img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("Image From File in Gray", img_gray)
        #cv2.waitKey()

        ret, img_thresh = cv2.threshold(img_gray, 100, 255, cv2.THRESH_TRIANGLE)
        #cv2.imshow("Threshold Image", img_thresh)
        #cv2.waitKey()

        contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1, (0, 255, 0), 1)

        # maybe use bounding box
        # loop through all contours, calculate measurements and store values in appropriate list
        areas = []
        centers = []
        moments_list = []
        largestarea = 0.0
        for c in contours:
            area = cv2.contourArea(c)
            areas.append(cv2.contourArea(c))
            if (area > largestarea):
                largestarea = area
                M_1= cv2.moments(c)
                moments_list.append(M_1)
                if M_1["m00"] == 0: M_1["m00", "m01"] = 1
                x = int(M_1["m10"] / M_1["m00"])
                y = int(M_1["m01"] / M_1["m00"])
                centers.append((x, y))

        #cv2.circle(img,(x, y), 2, (255,0,0), -1)
        
        #cv2.circle(img,(int(img.shape[1] / 2), int(img.shape[0] / 2)), 2, (0,0,255), -1)
        
        ex = x - img.shape[1] / 2
        ey = y - img.shape[0] / 2
        
        #cv2.putText(img, "x error = " + str(ex), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        #cv2.putText(img, "y error = " + str(ey), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

        #cv2.imshow('Image with Contours', img)
        #cv2.waitKey(1000)

        return ex, ey

    #ADD PID ALGORITHMS
    def move_error(self, ex: int, ey: int, motor_x: Motor, motor_y: Motor): #figure out better name
        c_x = 10 #conversion factors for x -> fix
        c_y = 10 #conversion factors for y -> fix
        if(abs(ex)<self.tol_x):
            dir_x = numpy.sign(ex) #might need to multiply by -1
            step_x = c_x*ex
            motor_x.Run(step_x, dir_x, self.delay)
        if(abs(ey)<self.tol_y):
            dir_y = numpy.sign(ey) #might need to multiply by -1
            step_y = c_y*ey
            motor_y.Run(step_y, dir_y, self.delay)
