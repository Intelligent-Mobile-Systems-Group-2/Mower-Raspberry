import serial
import time
from picamera import PiCamera
import asyncio
import json
import http.client
import mimetypes
from codecs import encode
import requests


def sendRequest():

    conn = http.client.HTTPConnection("ims.matteobernardi.fr")
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=x;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("5"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=y;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("53"))
    dataList.append(encode('--'+boundary+'--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
      'Accept-Encoding': 'gzip,deflate,sdch',
      'Accept-Charset': 'UTF-8',
      'Content-Type': 'application/json',
      'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    conn.request("POST", "/boundary-collision", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    


camera = PiCamera()

right = b"Right\n"
back = b"Back\n"
left = b"Left\n"
forward = b"Forward\n"
goRandom = b"GoRandom\n"

connection = "connection"

degree = 20066
random = "random"

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
            print(line)
            coordinates = line.split(",")
            data = len(coordinates)
            
            if data == 2:
                x = coordinates[0]
                y = coordinates[1]
                print(x + "," + y)
                
            if data == 3:
                if coordinates[0] == "objectDetected":
                    camera.capture("/home/pi/Pictures/img.jpg")
                    image = '/home/pi/Pictures/img.jpg'
                    detected = coordinates[0]
                    x = coordinates[1]
                    y = coordinates[2]
                    print(detected+ "," + x + "," + y )
                    imageRequest = requests.post("http://ims.matteobernardi.fr/object-collision/", data={"x": x, "y": y, "photo": image})
                    try:
                        print(imageRequest.text)
                        print(imageRequest.status_code)
                    except:
                          print("Error")
            
                if coordinates[0] == "lineDetected":
                    detected = coordinates[0]
                    x = coordinates[1]
                    y = coordinates[2]
                    print(detected + "," + x + "," + y)
                    
                    lineRequest = requests.post("http://ims.matteobernardi.fr/boundary-collision/", data={"x": x, "y": y})
                    try:
                        print(lineRequest.text)
                        print(lineRequest.status_code)
                    except:
                          print("Error")

