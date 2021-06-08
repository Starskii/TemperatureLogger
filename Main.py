import os
import glob
import time
from pyrebase import pyrebase

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

config = {
  "apiKey": "cK3WiFWvH1r0CFpQtWOFQwv7Wsu939u6GPL3LAm0",
  "authDomain": "temperaturelogger-a3bf4.firebaseapp.com",
  "databaseURL": "https://temperaturelogger-a3bf4-default-rtdb.firebaseio.com/",
  "storageBucket": "temperaturelogger-a3bf4.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def run_app():
    print("What is the name of this logger? \n")
    name = input("Enter Name: ")
    print("Take temperature read every (how many seconds?)")
    delay = input("Enter Delay Time: ")
    while True:
        temp_c = read_temp()
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        data = {
            'name': str(name),
            'celsius': float(temp_c),
            'fahrenheit': float(temp_f)
        }

        db.child("mlx90614").child("1-set").set(data)
        db.child("mlx90614").child("2-push").push(data)
        time.sleep(int(delay))


run_app()

