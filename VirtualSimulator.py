""" This module allows to create a virtual device with sensors and actuators,
and connected to the cloud through MQTT. It has three parts :
    Part 1 instantiates virtual sensors and actuators + automation possibilities (flags)
    Part 2 defines the GUI that uses those instances
    Part 3 defines MQTT commands and main loop starts the GUI
"""

import cmd, sys
import logging
import VirtualSensorsActuators
from Tkinter import *
import json
import paho.mqtt.client as paho
import random

# To show less info during execution, set myLogger.setLevel() to 20 or 30...
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
myLogger = logging.getLogger("myLogger")
myLogger.setLevel(10)

## Part 1 ##
# Instantiate default sensors and actuators.
waterSensor = VirtualSensorsActuators.DigitalSensor('water1')
motionSensor = VirtualSensorsActuators.DigitalSensor('motion1')
luminositySensor = VirtualSensorsActuators.AnalogSensor('lum1')
buzzer = VirtualSensorsActuators.DigitalActuator('buzz1')

# Flags keep track of user commands like automation.
# For now there is only one type of flag,
# that is in charge of automating changes of luminosity sensor values.
class Flags:
    def __init__(self):
        self.automationFlag = False

flags = Flags()

def toggleAutomation():
    """ Raise or shut the automation flag """
    flags.automationFlag = not flags.automationFlag

## Part 2 ##
mainWindow = Tk()
mainWindow.wm_title("This is a virtual board")
mainWindow['bg']='lightgrey'

# Let's define main frames, for digital sensors, analog sensors and digital actuators.
digitalSensorFrame = Frame(mainWindow, bg="darkgrey", borderwidth=2, relief=GROOVE)
digitalSensorFrame.pack(fill=BOTH, side=TOP, padx=30, pady=30)
Label(digitalSensorFrame, text="Digital sensors", font="-weight bold").pack(side=TOP, padx=10, pady=10)

analogSensorFrame = Frame(mainWindow, bg="darkgrey", borderwidth=2, relief=GROOVE)
analogSensorFrame.pack(fill=BOTH, side=TOP, padx=30, pady=30)
Label(analogSensorFrame, text="Analog sensors", font="-weight bold").pack(side=TOP, padx=10, pady=10)

digitalActuatorFrame = Frame(mainWindow, bg="darkgrey", borderwidth=2, relief=GROOVE)
digitalActuatorFrame.pack(fill=BOTH, side=TOP, padx=30, pady=30)
Label(digitalActuatorFrame, text="Digital actuators", font="-weight bold").pack(side=TOP, padx=10, pady=10)

# Let's define subframes, corresponding to sensors and actuators.
# Subframes are embedded in main frames and have to be associated with an instance of sensor/actuator
# For example, the motionSensorFrame is embedded in digitalSensorFrame, and is associated to motionSensor, an instance of DigitalSensor().
# Subrames representing :
    # digital sensors have On Off radiobuttons,
    # analog sensors have an entry value for the user to change, or automate
    # digital actuators only display info : they are commanded from cloud, not GUI !

# Motion Frame
motionSensorFrame = Frame(digitalSensorFrame, borderwidth=2, relief=GROOVE)
motionSensorFrame.pack(side=RIGHT, padx=5, pady=5)
Label(motionSensorFrame, text="Motion sensor", bg="white").pack(side=TOP, padx=10, pady=10)
value = StringVar()
boutonOn = Radiobutton(motionSensorFrame, text="On", variable=value, value=1, command=lambda: VirtualSensorsActuators.turnDigitalOnOff(motionSensor)).pack(side=BOTTOM)
boutonOff = Radiobutton(motionSensorFrame, text="Off", variable=value, value=2, command=lambda: VirtualSensorsActuators.turnDigitalOnOff(motionSensor)).pack(side=BOTTOM)

# Water Frame
waterSensorFrame = Frame(digitalSensorFrame, borderwidth=2, relief=GROOVE)
waterSensorFrame.pack(side=RIGHT, padx=5, pady=5)
Label(waterSensorFrame, text="Water sensor",bg="white").pack(side=TOP, padx=10, pady=10)
value2 = StringVar()
boutonOn = Radiobutton(waterSensorFrame, text="On", variable=value2, value=1, command= lambda: VirtualSensorsActuators.turnDigitalOnOff(waterSensor)).pack(side=BOTTOM)
boutonOff = Radiobutton(waterSensorFrame, text="Off", variable=value2, value=2, command= lambda: VirtualSensorsActuators.turnDigitalOnOff(waterSensor)).pack(side=BOTTOM)

# Luminosity Frame
luminositySensorFrame = Frame(analogSensorFrame, borderwidth=2, relief=GROOVE)
luminositySensorFrame.pack(side=RIGHT, padx=5, pady=5)
Label(luminositySensorFrame, text="Luminosity sensor",bg="white").pack(side=TOP, padx=10, pady=10)
value3 = IntVar()
value3.set("0")
lumValue = Entry(luminositySensorFrame, textvariable=value3, width=20, font="Helvetica 13 italic")
lumValue.pack(side=BOTTOM)
bouton = Button(luminositySensorFrame, text ='Change value', command = lambda: VirtualSensorsActuators.changeAnalogValue(luminositySensor, lumValue.get()) )
bouton.pack(side=BOTTOM)
# Luminosity automation
bouton = Checkbutton(luminositySensorFrame, text='Enable automation', command = toggleAutomation)
bouton.pack(side=BOTTOM)

# Buzzer Frame
buzzerFrame = Frame(digitalActuatorFrame, borderwidth=2, relief=GROOVE)
buzzerFrame.pack(side=RIGHT, padx=5, pady=5)
Label(buzzerFrame, text="Buzzer\n(on if red)").pack(side=TOP, padx=10, pady=10)


## Part 3 ##
def on_connect(client, userdata, flags, rc):
    """ Callback triggered when connected to the MQTT broker.
    :param client: the client instance for this callback
    :param userdata: the private user data as set in Client() or userdata_set()
    :param flags: response flags sent by the broker
    :param rc: the connection result
    :return: None
    """
    print("Connected to the MQTT broker: %s" % rc)
    # Subscribe to 'cmd' (command) and 'config' (configuration) MQTT topics.
    client.subscribe(mqtt_credentials['topic']+'cmd')
    client.subscribe(mqtt_credentials['topic']+'config')


def on_message(client, userdata, msg):
    """ Callback triggered when an MQTT message is received.
    :param client: the client instance for this callback
    :param userdata: the private user data as set in Client() or userdata_set()
    :param msg: an instance of MQTTMessage. This is a class with members topic,
    payload, qos, retain.
    :return: None
    """
    # Decode the received JSON message.
    message = json.loads(msg.payload)
    # Handle the received messages with 'name':'buzzer'.
    if message['name'] == 'buzzer':
        if message['value']: # buzzer has to be triggered
            buzzer.start()
            buzzerFrame.config(bg="red")
            myLogger.info(buzzer.name + " is activated !")
        else: # Stop the buzzer
            buzzer.stop()
            buzzerFrame.config(bg="white")
            myLogger.info(buzzer.name + " was stopped...")


# MQTT server address.
mqtt_server = "mqtt.relayr.io"
# MQTT credentials.
mqtt_credentials = {
    "user": "<your user ID>",
    "password": "<your password>",
    "clientId": "<your client ID>",
    "topic": "<your MQTT topic>"
}

# Message publishing frequency in milliseconds.
pub_freq_ms = 500
# Initialize the MQTT client.
client = paho.Client()
# Set the MQTT username and password.
client.username_pw_set(mqtt_credentials['user'], mqtt_credentials['password'])
# Register a 'on_connect' callback.
client.on_connect = on_connect
# Register a callback for received messages.
client.on_message = on_message
# Connect to the MQTT broker through port 1883 (no SSL) and timeout of  60s.
client.connect(mqtt_server, 1883, 60)
# Start a network loop on a separate thread.
client.loop_start()

def task():
    """ Parallel task executed at a frequency of pub_freq_ms
    This allows to publish to the cloud in parallel of using the GUI
    """
    myLogger.debug("Parallel task publishing data")

    # Allows user to automate change of analogSensor.value. Set to random by default.
    if flags.automationFlag:
        VirtualSensorsActuators.changeAnalogValue(luminositySensor, random.randint(0,100) )

    # Form a python dictionary payload
    data = [{'meaning': 'motion', 'value': motionSensor.value},
            {'meaning': 'luminosity', 'value': luminositySensor.value},
            {'meaning': 'water', 'value': waterSensor.value}]
    # Publish the payload as a json message to the 'data' MQTT topic.
    client.publish(mqtt_credentials['topic'] + '/data',
                       payload=json.dumps(data), qos=0, retain=False)
    # Reschedule event
    mainWindow.after(pub_freq_ms, task)

# Trigger task() and GUI
mainWindow.after(pub_freq_ms, task)
mainWindow.mainloop()

myLogger.debug("This is the end.... my only friend !")