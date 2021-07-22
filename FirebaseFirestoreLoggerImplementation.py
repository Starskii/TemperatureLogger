import os
import glob
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime as dt


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

db = firestore.client()


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
    print("What is the ID of this device?");
    deviceID = input("Enter Device ID: ");
    print("What is the name of this logger? \n")
    name = input("Enter Name: ")
    print("Take temperature read every (how many seconds?)")
    delay = input("Enter Delay Time: ")
    while True:
        now = dt.now()
        temp_c = read_temp()
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        data = {
            'name': str(name),
            'datetime': str(now),
            'celsius': float(temp_c),
            'fahrenheit': float(temp_f)
        }
        db.collection('temperature-logs/' + deviceID).add(data)
        time.sleep(int(delay))


run_app()

