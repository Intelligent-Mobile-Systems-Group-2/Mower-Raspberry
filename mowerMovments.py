import serial
import time
from picamera import PiCamera


file_name = "/home/pi/Pictures/img_" + str(time.time()) + ".jpg"
camera = PiCamera()
action = b"goForward\n"

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
    ser.reset_input_buffer()
    while True:
        ser.write(action)
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            coordinates = line.split(",")
            x = coordinates[0]
            y = coordinates[1]
            z = coordinates[2]
            print(x + "," + y + ","+ z)
            