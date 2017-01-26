#!/usr/bin/python

# -----------------------
# Import required Python libraries
# -----------------------

import RPi.GPIO as GPIO
import time
from flask import Flask, render_template

GPIO.setmode(GPIO.BCM)

#Motor 1 = pins : 17 - 18

GPIO.setup(17,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)

#Motor 2 = pins : 22 - 23
GPIO.setup(22,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

# Define Ultrasonic GPIO to use on Pi
GPIO_TRIGGER = 27
GPIO_ECHO    = 24

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)


timelength = 0.2

def gauche_avant():
    print "gauche avant"
    GPIO.output(18,0)
    GPIO.output(17,1)

def gauche_arriere():
    print "gauche arriere"
    GPIO.output(18,1)
    GPIO.output(17,0)

def gauche_stop():
    print "gauche stop"
    GPIO.output(18,0)
    GPIO.output(17,0)

def droite_avant():
    print "droite avant"
    GPIO.output(22,0)
    GPIO.output(23,1)

def droite_arriere():
    print "droite arriere"
    GPIO.output(22,1)
    GPIO.output(23,0)

def droite_stop():
    print "droite stop"
    GPIO.output(22,0)
    GPIO.output(23,0)

def avant_toute():
    print "avant toute"
    gauche_avant()
    droite_avant()

def arriere_toute():
    print "arriere toute"
    gauche_arriere()
    droite_arriere()

def stop_all():
    print "stop all"
    gauche_stop()
    droite_stop()


# -----------------------
# Define some functions
# -----------------------

def measure():
  # This function measures a distance
#  print "measure()"
  GPIO.output(GPIO_TRIGGER, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()
  while GPIO.input(GPIO_ECHO)==0:
    start = time.time()
#    print "echo 0"
  while GPIO.input(GPIO_ECHO)==1:
    stop = time.time()
#    print "echo 1"
  elapsed = stop-start
  distance = (elapsed * 34300)/2
  return distance

def measure_average():
  # This function takes 3 measurements and
  # returns the average.
#  print "avg"
  distance1=measure()
  time.sleep(0.1)
  distance2=measure()
  time.sleep(0.1)
  distance3=measure()
  distance = distance1 + distance2 + distance3
  distance = distance / 3
  return distance

app = Flask(__name__)

@app.route("/")
@app.route("/<state>")
def update_robot(state=None):
    if state == 'forward':
        gauche_avant()
        droite_avant()
        time.sleep(timelength)
        stop_all()
    if state == 'back':
        gauche_arriere()
        droite_arriere()
        time.sleep(timelength)
        stop_all()
    if state == 'left':
        droite_avant()
        time.sleep(timelength)
        stop_all()
    if state == 'right':
        gauche_avant()
        time.sleep(timelength)
        stop_all()
    if state == 'stop':
        stop_all()
    if state == 'anti-clockwise':
        droite_avant()
        gauche_arriere()
        time.sleep(timelength)
        stop_all()
    if state == 'clockwise':
        gauche_avant()
        droite_arriere()
        time.sleep(timelength)
        stop_all()
    template_data = {
        'title' : state,
	'distance' : measure(),
    }
    return render_template('main.html', **template_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
#GPIO.cleanup()


