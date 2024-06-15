import cv2

def calculate_error(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("Image From File in Gray", img_gray)
    #cv2.waitKey()

    ret, img_thresh = cv2.threshold(img_gray, 100, 255, cv2.THRESH_TRIANGLE)
    #cv2.imshow("Threshold Image", img_thresh)
    #cv2.waitKey()

    contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 255, 0), 1)

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

    cv2.circle(img,(x, y), 2, (255,0,0), -1)
    
    cv2.circle(img,(int(img.shape[1] / 2), int(img.shape[0] / 2)), 2, (0,0,255), -1)
    
    ex = x - img.shape[1] / 2
    ey = y - img.shape[0] / 2
    
    cv2.putText(img, "x error = " + str(ex), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    cv2.putText(img, "y error = " + str(ey), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

    #cv2.imshow('Image with Contours', img)
    #cv2.waitKey(1000)

    return ex, ey

'''#PID ALGORITHMS
    def move_error(self, ex: int, ey: int): #figure out better name
        c_x = 10 #conversion factors for x -> fix
        c_y = 10 #conversion factors for y -> fix
        if(abs(ex)<self.tol_x):
            dir_x = numpy.sign(ex) #might need to multiply by -1
            step_x = c_x*ex
            self.motor_x.Run(step_x, dir_x, self.delay)
        if(abs(ey)<self.tol_y):
            dir_y = numpy.sign(ey) #might need to multiply by -1
            step_y = c_y*ey
            self.motor_y.Run(step_y, dir_y, self.delay)
    
    def move_diode(self):
        step = 10 # FIX
        dir = 1 # FIX
        self.motors_x.Run(step,dir,self.delay)'''