import serial
import time
import asyncio
import websockets
import json
from picamera import PiCamera

camera = PiCamera()
action = "goForward\n"

async def useSocket():
    async with websockets.connect("ws://localhost:8765") as websocket:
        # await websocket.send("Hello world!")
        await websocket.send("hello nice to meet u")
        await websocket.recv()

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
    asyncio.run(useSocket());
    ser.reset_input_buffer()
    while True:
        #ser.write(action)
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            coordinates = line.split(",")
            data = len(coordinates)
            if data == 2:
                x = coordinates[0]
                y = coordinates[1]
                #z = coordinates[2]
                print(x + "," + y)
            if data == 3:
                if coordinates[0] == "takePic":
                    camera.capture("/home/pi/Pictures/img.jpg")
                    x = coordinates[1]
                    y = coordinates[2]
                    print( x + "," + y )
                    print("\ndone")