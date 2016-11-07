import cmd, sys, random

# All hardware GPIOs are replaced by software classes that can be automated or user commanded
class DigitalSensor:
    def __init__(self, name):
        self.name = name
        self.value = "false"

    def __str__(self):
        return self.name

    def start(self):
        self.value = "true"

    def stop(self):
        self.value = "false"


class DigitalActuator:
    def __init__(self, name):
        self.value = "false"
        self.name = name

    def __str__(self):
        return self.name

    # Actuator shouldn't be controlled from device, but from the cloud !
    def start(self):
        self.value = "true"

    def stop(self):
        self.value = "false"


class AnalogSensor:
    def __init__(self, name):
        self.value = 1
        self.name = name

    def __str__(self):
        return self.name


# Here are the functions that allow us to modify states of sensors !
def turnDigitalOnOff(digitalSensor):
    """ This function toggles a digital sensor on or off """
    if digitalSensor.value == "false":
        digitalSensor.start()
    else:
        digitalSensor.stop()

def changeAnalogValue(analogSensor, value): # might be useless on the long term. Unless changes need to be tracked
    analogSensor.value = value
