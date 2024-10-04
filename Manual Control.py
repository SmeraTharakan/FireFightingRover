from pynput import keyboard
import RPi.GPIO as GPIO
import time
import serial

GPIO.setwarnings(False)
GPIO.cleanup()
# Set up GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)  # Motor 1 (IN1)
GPIO.setup(23, GPIO.OUT)  # Motor 2 (IN2)
GPIO.setup(24, GPIO.OUT)  # Motor 3 (IN4)
GPIO.setup(25, GPIO.OUT)  # Motor 4 (IN3)
GPIO.setup(5, GPIO.OUT)  # PIN NO 29
GPIO.setup(6, GPIO.OUT)  # PIN NO 31
GPIO.setup(15, GPIO.OUT) #PIN NO 10
GPIO.setup(18, GPIO.OUT)  #PIN NO 12
#GPIO.setup(17, GPIO.IN) #PIN NO 11
#GPIO.setup(27, GPIO.IN) #PIN NO 13


def turn_right():
    GPIO.output(22, False)
    GPIO.output(23, True)
    GPIO.output(24, False)
    GPIO.output(25, True)

def turn_left():
    GPIO.output(22, True)
    GPIO.output(23, False)
    GPIO.output(24, True)
    GPIO.output(25, False)

def move_backward():
    GPIO.output(22, False)
    GPIO.output(23, True)
    GPIO.output(24, True)
    GPIO.output(25, False)

def move_forward():
    GPIO.output(22, True)
    GPIO.output(23, False)
    GPIO.output(24, False)
    GPIO.output(25, True)

def stop_motors():
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
    

def on_key_press(key):
    try:
        if key == keyboard.Key.up:
            move_forward()
        elif key == keyboard.Key.down:
            move_backward()
        elif key == keyboard.Key.left:
            turn_left()
        elif key == keyboard.Key.right:
            turn_right()
        if key == keyboard.KeyCode.from_char('z'):
            UP()
        if key == keyboard.KeyCode.from_char('x'):
            DOWN()
        if key == keyboard.KeyCode.from_char('c'):
            start_water()
    except AttributeError:
        pass

def on_key_release(key):
    if key in [keyboard.Key.up,keyboard.Key.down,keyboard.Key.left,keyboard.Key.right]:
        stop_motors()
    if key in [keyboard.KeyCode.from_char('z'),keyboard.KeyCode.from_char('x'),keyboard.Key.esc]:
        stop_arm()
    if key in [keyboard.KeyCode.from_char('c'),keyboard.Key.esc]:
        stop_water()

# Collect events until released
with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()


# Cleanup GPIO on script exit
GPIO.cleanup()