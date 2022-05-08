import RPi.GPIO as GPIO
import json

logic={"ON" : True, "OFF" : False}

GPIO.setmode(GPIO.BOARD)

def initialize(state):
    for lvl1 in state:
        for lvl2 in state[lvl1]:
            for thing in state[lvl1][lvl2]:
                GPIO.output(pins[thing], logic[state[lvl1][lvl2][thing]])

def switch_state(thing, value):
    GPIO.output(pins[thing], logic[value])

with open("pins.json") as file:
    pins_txt = file.read()
    pins = json.loads(pins_txt)

for thing in pins:
    GPIO.setup(pins[thing], GPIO.OUT)
