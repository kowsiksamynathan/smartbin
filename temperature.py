import os
import time
from firebase import firebase
firebase = firebase.FirebaseApplication('https://smartbin-4fb99.firebaseio.com/')


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_id = '28-03168afdc5ff'
device_file = base_dir + device_id + '/w1_slave'

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
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

while True:
        t=read_temp()
        print (t)
        if(t<35):
            print ("updating in firebase")
            result=firebase.put('https://smartbin-4fb99.firebaseio.com/dustbin/smartbin001','toxic','no')
            print(result)
        else:
            print ("updating in firebase")
            result=firebase.put('https://smartbin-4fb99.firebaseio.com/dustbin/smartbin001','toxic','yes')
            print(result)
        time.sleep(1)
