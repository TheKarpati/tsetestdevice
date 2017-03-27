""" This module defines what are sensors and actuators.
All hardware GPIOs are replaced by software classes that can be
automated or user commanded. Those classes can be instantiated.
All sensors/actuators have a name and a value.
At the end of the module are the basic functions to change those values.
"""

class DigitalSensor:
    """ A DigitalSensor can only be on or off. Ex: motion sensor"""
    def __init__(self, name):
        self.name = name
        self.value = False

    def __str__(self):
        return self.name

    def start(self):
        self.value = True

    def stop(self):
        self.value = False


class DigitalActuator:
    """ A DigitalActuator can only be on or off. Ex: buzzer"""
    def __init__(self, name):
        self.value = False
        self.name = name

    def __str__(self):
        return self.name

    # Actuator shouldn't be controlled from device, but from the cloud !
    def start(self):
        self.value = True

    def stop(self):
        self.value = False


class AnalogSensor:
    """ An AnalogSensor can have any numeric value. Ex: a luminosity sensor"""
    def __init__(self, name):
        self.value = 1
        self.name = name
        self.automationFlag = False # is used to automate sensor values

    def __str__(self):
        return self.name


# Here are the functions that allow us to modify states of sensors
def changeAnalogValue(analogSensor, value):
    """ It seems redundant but this function is NECESSARY for
    future lambda expressions in the GUI"""
    analogSensor.value = value

def toggleAutomation(analogSensor):
    analogSensor.automationFlag = not analogSensor.automationFlag
