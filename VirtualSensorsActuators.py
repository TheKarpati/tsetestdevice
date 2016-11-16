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
        self.automationFlag = False # is used to automation sensor values

    def __str__(self):
        return self.name


# Here are the functions that allow us to modify states of sensors !
def changeAnalogValue(analogSensor, value):
    """ Although it seems redundant, this function is NECESSARY as we use it in lambda expressions in the GUI
    """
    analogSensor.value = value

def toggleAutomation(analogSensor):
    analogSensor.automationFlag = not analogSensor.automationFlag
