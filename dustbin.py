import time
from firebase import firebase
firebase = firebase.FirebaseApplication('https://smartbin-4fb99.firebaseio.com/')
import RPi.GPIO as GPIO
GPIO.cleanup()
TRIG =3
ECHO =5
while(1):
    print "Distance measurement in progress"
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT) 
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG,False)
    print "Waiting for sensor to settle down"
    time.sleep(2)
    GPIO.output(TRIG,True)
    time.sleep(0.00001) 
    GPIO.output(TRIG,False) 
    while GPIO.input(ECHO)==0:
        pulse_start=time.time()
        
    while GPIO.input(ECHO)==1:
        pulse_end=time.time()
        pulse_duration= pulse_end - pulse_start
    distance = pulse_duration*17150
    distance=round(distance,2)
    print "Distance : " ,distance ,"Cm"
    if(distance < 10):
        print "updating in firebase"
        result=firebase.put('https://smartbin-4fb99.firebaseio.com/dustbin/smartbin001','status','filled')
        print(result)
    elif(distance>10 and distance <20):
        print "updating in firebase"
        result=firebase.put('https://smartbin-4fb99.firebaseio.com/dustbin/smartbin001','status','half_filled')
        print(result)
    else:
        print "updating in firebase"
        result=firebase.put('https://smartbin-4fb99.firebaseio.com/dustbin/smartbin001','status','empty')
        print(result)
    
    time.sleep(10)
    GPIO.cleanup()
