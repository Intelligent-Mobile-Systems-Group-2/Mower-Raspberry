import serial
import time
from picamera import PiCamera
import asyncio
import json
import http.client
import mimetypes
from codecs import encode
import requests
from bluedot.btcomm import BluetoothServer
from signal import pause
import threading

from requests.exceptions import ConnectionError


camera = PiCamera()

#Variables to control the Mower
right = b"Right\n"
back = b"Back\n"
left = b"Left\n"
forward = b"Forward\n"
goRandom = b"GoRandom\n"
stopMoving = b"StopMoving\n"



def sendDataToBackend():
    
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            data = line.split(",")
            detected = data[0]
            x = data[1]
            y = data[2]
            
            data = len(data)
            oldDetect = detected
            detected_x = x
            detected_x = y
            coord_obj = {
                "x": x,
                "y": y
            }
            
            if detected == "objectDetected":
                camera.capture("/home/pi/Pictures/img.jpg")
                image_fd = open('/home/pi/Pictures/img.jpg', 'rb')
                image_bin = image_fd.read()
                image_fd.close()
                image_obj = {
                    "photo": image_bin
                }
                
                try:
                    response = requests.put("http://ims.matteobernardi.fr/object-collision", data=coord_obj, files=image_obj)
                    print(response.text)
                except ConnectionError as e:
                      print("Error", e)

            elif detected == "lineDetected":
                try:
                    response = requests.put("http://ims.matteobernardi.fr/boundary-collision", json=coord_obj)
                    print(response.text)
                except ConnectionError as e:
                      print("Error", e)


def data_received(data):
    recievedData = data.split()
    selectionMode = len(recievedData) #Check for how many objects in recievedData ex. 2
    degree = int(recievedData[0]) #First value in recievedData changed to INT ex. 127
    if selectionMode == 1:
        ser.write(stopMoving)
        time.sleep(3)
        ser.write(goRandom)
       
    elif selectionMode == 2:
        if  degree < 135  and degree > 45:
            ser.write(right)
        elif  degree < 45 and degree > 0:
            ser.write(forward)
        elif  degree < 359 and degree > 315:
            ser.write(forward)
        elif  degree < 315  and degree > 225:
            ser.write(left)
        elif  degree < 225  and degree > 135:
            ser.write(back)
                  
    
   
# The Server API 
api = "http://ims.matteobernardi.fr/boundary-collision/"
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
    ser.reset_input_buffer()
    t = threading.Thread(target=sendDataToBackend)
    t.start()

    while True:
        
        s = BluetoothServer(data_received)
        pause()
        


