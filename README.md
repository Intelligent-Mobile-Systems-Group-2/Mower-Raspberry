# Mower-Raspberry-Documentaion

Setting up the Raspberry Pi:

Install the operative system 32-bit of the Raspberry Pi on an SD card.
Put the SD card into the Raspberry Pi.
Connect the Raspberry Pi to a screen via an HDMI cable.
Connect a power supply to the Raspberry Pi.
Connect the mouse, keyboard, and the mower to the Raspberry pi's USB ports.

Setting up the camera on the Raspberry Pi:

Open the Raspberry Pi terminal and run "sudo raspi-config".
Select interface options and select the camera to enable it. 
Select Finish, and reboot the Raspberry Pi.
From the terminal again, you need to write the following commands:
sudo apt-get update
sudo apt-get upgrade
pip3 install picamera
Import picamera in your code.

Setting up Bluetooth:

Open preferences → Rasspberry Configuration → Interfaces → enable Serial Port → Reboot
After rebooting:
Open the terminal and type the following command:
  sudo nano /etc/systemd/system/dbus-org.bluez.service
    Add -C in the end of the following line
    ExecStart=/usr/lib/bluetooth/bluetoothd 
    Add the following line:
    ExecStartPost=/usr/bin/sdptool add SP
    Then save the file and exit, by pressing CTRL x then CTRL s. 
  sudo systemctl daemon-reload
  sudo systemctl restart bluetooth.service
  sudo pip3 install bluedot
import the following:
from bluedot.btcomm import BluetoothServer
from signal import pause
