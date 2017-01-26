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
    }
    return render_template('main.html', **template_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
#GPIO.cleanup()
