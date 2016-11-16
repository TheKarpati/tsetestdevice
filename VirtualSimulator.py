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
import ast

# To show less info during execution, set myLogger.setLevel() to 20 or 30...
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
myLogger = logging.getLogger("myLogger")
myLogger.setLevel(10)

## Part 1 ##
# Instantiate default sensors and actuators.
waterSensor = VirtualSensorsActuators.DigitalSensor('water1')
motionSensor = VirtualSensorsActuators.DigitalSensor('motion1')
luminositySensor = VirtualSensorsActuators.AnalogSensor('lum1')
thermometerSensor = VirtualSensorsActuators.AnalogSensor('therm1')
buzzer = VirtualSensorsActuators.DigitalActuator('buzz1')

class Credentials:
    # MQTT server address.
    mqtt_server = "mqtt.relayr.io"

    # MQTT credentials.
    mqtt_credentials = """{
    "user": "insert userId",
    "password": "insert user password",
    "clientId": "insert client ID",
    "topic": "insert topic"
    }"""

## Part 2 ##
class CredentialsWindow:
    """ This window gets user's credentials """
    def __init__(self, master):
        self.master = master
        self.credentialsFrame = Frame(self.master, bg="darkgrey", borderwidth=2, relief=GROOVE)
        Label(self.credentialsFrame, text="Insert your device's credentials here", font="-weight bold").pack(side=TOP, padx=10, pady=10)
        self.credentialsFrame.pack(fill=BOTH, side=TOP, padx=20, pady=20)

        self.credValue = Text(self.credentialsFrame, height=6, font="Helvetica 13 italic")
        self.credValue.insert(INSERT, Credentials.mqtt_credentials)
        self.credValue.pack(side=TOP)

        self.button = Button(self.credentialsFrame, text ="Let's go!", command = lambda: self.defineCredentials(self.credValue.get("1.0",END)) )
        self.button.pack(side=BOTTOM)

    def defineCredentials(self, newCreds):
        Credentials.mqtt_credentials = ast.literal_eval(newCreds) #Turns the dictionnary-like string into a real dict
        self.master.destroy()


class VirtualBoard:
    """ This is the main GUI """
    def __init__(self, master):
        self.master = master

        # Let's define main frames, for digital sensors, analog sensors and digital actuators.
        self.digitalSensorFrame = Frame(self.master, bg="darkgrey", borderwidth=2, relief=GROOVE)
        self.analogSensorFrame = Frame(self.master, bg="darkgrey", borderwidth=2, relief=GROOVE)
        self.digitalActuatorFrame = Frame(self.master, bg="darkgrey", borderwidth=2, relief=GROOVE)
        Label(self.digitalSensorFrame, text="Digital Sensors", font="-weight bold").pack(side=TOP, padx=10, pady=10)
        Label(self.analogSensorFrame, text="Analog Sensors", font="-weight bold").pack(side=TOP, padx=10, pady=10)
        Label(self.digitalActuatorFrame, text="Digital Actuator", font="-weight bold").pack(side=TOP, padx=10, pady=10)
        self.digitalSensorFrame.pack(fill=BOTH, side=TOP, padx=30, pady=30)
        self.analogSensorFrame.pack(fill=BOTH, side=TOP, padx=30, pady=30)
        self.digitalActuatorFrame.pack(fill=BOTH, side=TOP, padx=30, pady=30)

        # Let's define subframes, embedded in main frames
        # Subframes have to be associated with an instance of sensor/actuator
        # For example, the motionSensorFrame is embedded in digitalSensorFrame, and is associated to motionSensor, an instance of DigitalSensor().
        # Subrames representing :
            # digital sensors have On Off radiobuttons,
            # analog sensors have an entry value for the user to change, or automate
            # digital actuators only display info : they ought to be commanded from the cloud, not the GUI !
        self.motionSensorFrame = self.newDigitalSensorFrame(self.digitalSensorFrame, "Motion sensor", motionSensor)
        self.waterSensorFrame = self.newDigitalSensorFrame(self.digitalSensorFrame, "Water sensor", waterSensor)
        self.luminositySensorFrame = self.newAnalogSensorFrame(self.analogSensorFrame, "Luminosity sensor", luminositySensor)
        self.temperatureSensorFrame = self.newAnalogSensorFrame(self.analogSensorFrame, "Temperature", thermometerSensor)
        # buzzerFrame doesn't need a function, it's only 3 lines...
        self.buzzerFrame = Frame(self.digitalActuatorFrame, borderwidth=2, relief=GROOVE)
        self.buzzerFrame.pack(side=RIGHT, padx=5, pady=5)
        Label(self.buzzerFrame, text="Buzzer\n(on if red)", bg="white").pack(side=TOP, padx=10, pady=10)


    def newDigitalSensorFrame(self, masterFrame, label, digitalSensor):
        frame = Frame(masterFrame, borderwidth=2, relief=GROOVE)
        Label(frame, text=label, bg="white").pack(side=TOP, padx=10, pady=10)
        value = IntVar()
        value.set(1)
        buttonOff = Radiobutton(frame, text="Off", variable=value, value=1, command=lambda: digitalSensor.stop()).pack(side=BOTTOM)
        buttonOn = Radiobutton(frame, text="On", variable=value, value=2, command=lambda: digitalSensor.start()).pack(side=BOTTOM)
        frame.pack(side=RIGHT, padx=5, pady=5)

    def newAnalogSensorFrame(self, masterFrame, label, analogSensor):
        frame = Frame(masterFrame, borderwidth=2, relief=GROOVE)
        Label(frame, text=label, bg="white").pack(side=TOP, padx=10, pady=10)
        value = IntVar()
        value.set("0")
        analogValue = Entry(frame, textvariable=value, width=20, font="Helvetica 13 italic")
        analogValue.pack(side=BOTTOM)
        button = Button(frame, text ='Change value', command = lambda: VirtualSensorsActuators.changeAnalogValue(analogSensor, analogValue.get()) )
        button.pack(side=BOTTOM)
        # Automation button
        button = Checkbutton(frame, text='Enable automation', command = lambda: VirtualSensorsActuators.toggleAutomation(analogSensor))
        button.pack(side=BOTTOM)
        frame.pack(side=RIGHT, padx=5, pady=5)


## Part 3 ##
def main():
    """ The main() function has three parts
    First it gets the users credentials
    Then it sets the connection to the cloud via MQTT
    Finally it triggers the GUI of the Virtual Board
    """
    initialGUI = Tk()
    initialGUI.wm_title("Hello! Please enter your credentials!")
    initialGUI['bg']='lightgrey'
    app = CredentialsWindow(initialGUI) # creates an instance of CredentialsGUI as initialGUI
    initialGUI.mainloop()

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
        client.subscribe(Credentials.mqtt_credentials['topic']+'cmd')
        client.subscribe(Credentials.mqtt_credentials['topic']+'config')


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
                virtualBoard.buzzerFrame.config(bg="red")
                myLogger.info(buzzer.name + " is activated !")
            else: # Stop the buzzer
                buzzer.stop()
                virtualBoard.buzzerFrame.config(bg="white")
                myLogger.info(buzzer.name + " was stopped...")

    # Message publishing frequency in milliseconds.
    pub_freq_ms = 500
    # Initialize the MQTT client.
    client = paho.Client()
    # Set the MQTT username and password.
    client.username_pw_set(Credentials.mqtt_credentials['user'], Credentials.mqtt_credentials['password'])
    # Register a 'on_connect' callback.
    client.on_connect = on_connect
    # Register a callback for received messages.
    client.on_message = on_message
    # Connect to the MQTT broker through port 1883 (no SSL) and timeout of  60s.
    client.connect(Credentials.mqtt_server, 1883, 60)
    # Start a network loop on a separate thread.
    client.loop_start()

    mainGUI = Tk()
    mainGUI.wm_title("This is a virtual board")
    mainGUI['bg']='lightgrey'

    def task():
        """ Parallel task executed at a frequency of pub_freq_ms
        This allows to publish to the cloud in parallel of using the GUI
        """
        myLogger.debug("Parallel task publishing data")

        # Allows user to automate change of analogSensor.value. Set to random by default.
        if luminositySensor.automationFlag:
            luminositySensor.value = random.randint(0,100)

        if thermometerSensor.automationFlag:
            thermometerSensor.value = random.randint(0,100)

        # Form a python dictionary payload
        data = [{'meaning': 'motion', 'value': motionSensor.value},
                {'meaning': 'luminosity', 'value': luminositySensor.value},
                {'meaning': 'water', 'value': waterSensor.value},
                {'meaning': 'temperature', 'value': thermometerSensor.value}]
        # Publish the payload as a json message to the 'data' MQTT topic.
        client.publish(Credentials.mqtt_credentials['topic'] + '/data',
                           payload=json.dumps(data), qos=0, retain=False)
        # Reschedule event
        mainGUI.after(pub_freq_ms, task)

    # Trigger task() and GUI
    virtualBoard = VirtualBoard(mainGUI)
    mainGUI.after(pub_freq_ms, task)
    mainGUI.mainloop()

    myLogger.debug("This is the end.... my only friend!")

if __name__ == '__main__':
    main()