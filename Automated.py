import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

GPIO.setwarnings(False)
GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)  # Motor 1 (IN1)
GPIO.setup(23, GPIO.OUT)  # Motor 2 (IN2)
GPIO.setup(24, GPIO.OUT)  # Motor 3 (IN4)
GPIO.setup(25, GPIO.OUT)  # Motor 4 (IN3)
GPIO.setup(5, GPIO.OUT)  # PIN NO 29
GPIO.setup(6, GPIO.OUT)  # PIN NO 31
GPIO.setup(15, GPIO.OUT) #PIN NO 10
GPIO.setup(18, GPIO.OUT)  #PIN NO 12
GPIO.setup(4, GPIO.OUT)  #PIN NO 7
GPIO.setup(17, GPIO.IN)  #PIN NO 11
GPIO.setup(14, GPIO.IN)  #PIN NO 8
GPIO.setup(27, GPIO.IN)  #PIN NO 13

def to_fire(k):
    forward()
    while k<322 and k>317:
        (grabbed, frame) = video.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray_frame)
        k,l = max_loc
        
        dist = get_dist()
        fire_cond = ir_config()
        if dist < 25:
            stop()
            time.sleep(0.5)
            back()
            time.sleep(3)
            stop()
            return 'stop'
        elif dist < 50:
            obj_avoid()
            return 'again'
        if fire_cond:
            stop()
            xxxtinguish()
            return 'complete'
        
        

def xxxtinguish():
    start_water()
    UP()
    right()
    time.sleep(1)
    for i in range (3):
        DOWN()
        left()
        time.sleep(2)
        UP()
        right()
        time.sleep(2)
    stop_arm()
    stop_water()
    stop()

        

def ir_config():
    ir_state1 = GPIO.input(14)
    ir_state2 = GPIO.input(27)
    if ir_state1 == GPIO.LOW or ir_state2 == GPIO.LOW:
        return True
    else:
        return False


def obj_avoid():
    right()
    time.sleep(5)
    forward()
    time.sleep(5)
    left()
    time.sleep(5)
    stop()
    dist = get_dist()
    if dist < 50 and dist >25:
        return obj_avoid()
    

def get_dist():
    # Set trigger to HIGH
    GPIO.output(4, True)
    # Wait 0.01ms
    time.sleep(0.00001)
    # Set trigger to LOW
    GPIO.output(4, False)
    # Record the last LOW timestamp for ECHO
    while GPIO.input(17) == 0:
        pulse_start = time.time()
    # Record the last HIGH timestamp for ECHO
    while GPIO.input(17) == 1:
        pulse_end = time.time()
    # Calculate pulse duration
    pulse_duration = pulse_end - pulse_start
    # Convert pulse duration to distance (in cm)
    distance = pulse_duration * 17150
    # Round distance to 2 decimal places
    distance = round(distance, 2)
    time.sleep(0.5)
    print(distance)
    return distance

def back():
    GPIO.output(22, False)
    GPIO.output(23, True)
    GPIO.output(24, True)
    GPIO.output(25, False)
    
def forward():
    GPIO.output(22, True)
    GPIO.output(23, False)
    GPIO.output(24, False)
    GPIO.output(25, True)
    
def left():
    GPIO.output(22, True)
    GPIO.output(23, False)
    GPIO.output(24, True)
    GPIO.output(25, False)
    
def right():
    GPIO.output(22, False)
    GPIO.output(23, True)
    GPIO.output(24, False)
    GPIO.output(25, True)
    
def stop():
    GPIO.output(22, False)
    GPIO.output(23, False)
    GPIO.output(24, False)
    GPIO.output(25, False)
    
def DOWN():
    
    GPIO.output(5, False)
    GPIO.output(6, True)
    
def UP():
    
    GPIO.output(6, False)
    GPIO.output(5, True)
    
def stop_arm():
    GPIO.output(5, False)
    GPIO.output(6, False)
    
def stop_water():
    GPIO.output(15, False)
    GPIO.output(18, False)
    
def start_water():
    GPIO.output(15, True)
    GPIO.output(18, False)




video = cv2.VideoCapture(0)  

while True:
    fire_cond = ir_config()
    if fire_cond:
        stop()
        xxxtinguish()
        
    
    (grabbed, frame) = video.read()

    frame = cv2.resize(frame, (640, 480))

    # Find brightest location
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray_frame)
    x,y = max_loc
    #print(x)
    cv2.circle(frame, max_loc, 20, (0, 0, 255), 2)

    cv2.imshow('livefeed', frame)
    
    if x<327 and x>313:
        value = to_fire(x)
        if value == 'stop':
            break
        
    dist = get_dist()
    if dist < 25:
        stop()
        break
    
    if x>322:#rotate right
        k=x
        while k>322:
            (grabbed, frame) = video.read()
            frame = cv2.resize(frame, (640, 480))
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray_frame)
            k,l = max_loc
            #print(k)
            right()
        stop()
        #time.sleep(2)
        
    if x<317:#rotate left
        k=x
        while k<317:
            (grabbed, frame) = video.read()
            frame = cv2.resize(frame, (640, 480))
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray_frame)
            k,l = max_loc
            #print(k)
            left()
        stop()
        #time.sleep(2)
        
        

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
stop()
video.release()




