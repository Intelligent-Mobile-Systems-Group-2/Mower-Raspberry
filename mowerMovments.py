import serial
import time
from picamera import PiCamera
import asyncio
import json
import http.client
import mimetypes
from codecs import encode
import requests


camera = PiCamera()

right = b"Right\n"
back = b"Back\n"
left = b"Left\n"
forward = b"Forward\n"
goRandom = b"GoRandom\n"

connection = "connection"

degree = 20066
random = "random"

obj_detection_interval = 100

api = "http://ims.matteobernardi.fr/boundary-collision/"
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
    ser.reset_input_buffer()
    
    
    
    while True:
        #if  degree < 135  and degree > 45:
        #    ser.write(forward)
        #if  degree < 45 and degree > 0:
         #   ser.write(right)
        #if  degree < 359 and degree > 315:
          #  ser.write(right)
        #if  degree < 315  and degree > 225:
         #   ser.write(back)
        #if  degree < 225  and degree > 135:
           # ser.write(left)
        #if  random == "random":
        ser.write(goRandom)
        
        
        
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            data = line.split(",")
            detected = data[0]
            x = data[1]
            y = data[2]
            
            detected_x = 0
            detected_y = 0
            
            # if same coordinates as obj or line detected, skip this iteration
            if detected_x == x and detected_y == y or detected == "NothingDetected":
                continue
            
            data = len(data)
            
            if data == 3:
                detected_x = x
                detected_x = y
                coord_obj = {
                    "x": x,
                    "y": y
                }
                
                print(detected, coord_obj)
                
                if detected == "objectDetected":
                    camera.capture("/home/pi/Pictures/img.jpg")
                    image_fd = open('/home/pi/Pictures/img.jpg', 'rb')
                    image_bin = image_fd.read()
                    image_fd.close()
                    image_obj = {
                        "photo": image_bin
                    }
                    
                    try:
                        response = requests.post("http://ims.matteobernardi.fr/object-collision", data=coord_obj, files=image_obj)
                        print(response.text)
                        print(response.status_code)
                    except Exception as e:
                          print("Error", e)
            
                elif detected == "lineDetected":
                    try:
                        response = requests.post("http://ims.matteobernardi.fr/boundary-collision", json=coord_obj)
                        print(response.text)
                        print(response.status_code)
                    except Exception as e:
                          print("Error", e)

