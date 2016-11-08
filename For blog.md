# Connect a virtual board with sensors and actuators to the RelayR cloud (Python Edition)

## Introduction

Want to test different scenarios before you get hands dirty on *physical* sensors and boards ?

Want to get familiar with the cloud before learning how to configure your Arduino / Rasberry Pi / Weemos or other device is ?

You just want to try the cloud but don't know where to start ?

This is the tutorial you need !

This document will allow you to ***simulate*** some hardware sensors and actuators and connect them to the [Relayr cloud and dashboard](https://dev.relayr.io/) through an intuitive GUI that looks like this :

![Virtual Board](/assets/VirtualBoard.png)


## Requirements

The following hardware is required:

 * Nothing ! It's all virtual !

On the software side, you need to be able to run [Python 2.7.x](https://www.python.org/downloads/), and you need an account on the [RelayR website for developers](https://dev.relayr.io/).

## Installation & configuration

Two things we need to get set :

1. On the dashboard side, we need a device that corresponds to our Virtual Board.
2. On our computer, we want to run the Virtual Board.


### Create a Device in the developer dashboard

So first step is to get a representation of our Virtual Board in the relayr Cloud. The simplest way is to create a device running on the **Intel Edison Model**, because we will be simulating similar sensors. Through this entity we will manage sent/received data, MQTT credentials and UI interface of the relayr Dashboard. To create a device on relayr Dashboard follow the [**Devices Guide**](http://docs.relayr.io/getting-started/devices-guide/) and select the **Intel Edison (IoT Acceleration Starter Kit)** as a *Device Model*.

If you prefer to create your own model to get more advanced feature, log in to the Developer Dashboard and follow the instructions of [this tutorial](http://docs.relayr.io/getting-started/device-models-guide/).

But for now let's assume we are running the *Intel Edison (IoT Acceleration Starter Kit)* model.


###Paho MQTT

In order to run the Python examples provided in this repository, we need to install the [`paho-mqtt`](https://pypi.python.org/pypi/paho-mqtt/1.1) package,
which provides a MQTT client library and enables sending/receiving of messages to/from a MQTT broker. [MQTT](https://en.wikipedia.org/wiki/MQTT) is a lightweight messaging protocol built on top of TCP/IP. We chose it for exchanging messages between the cloud and the Virtual Board because of its simplicity and low overhead.

To install `paho-mqtt`  with `pip`, run:

```shell
pip install paho-mqtt
```

Once installed, we can use `paho-mqtt` classes by importing the module into our script, as we will see later in our code examples.

To learn more about the functionalities of the `paho-mqtt` Python client, see the
[official documentation](https://pypi.python.org/pypi/paho-mqtt/1.1).

We are now ready to make use of MQTT and run the Virtual Board !

## Starting the GUI and using the Virtual Board

### Starting the GUI (`VirtualSimulator.py`)


The only thing we need to do now is link our Virtual Board to our dashboard device. In order to do so, paste the device's credentials from the relayr Dashboard into the appropriate place of the `VirtualSimulator.py`.

```python
# MQTT credentials.
mqtt_credentials = {
    "user": "<your user ID>",
    "password": "<your password>",
    "clientId": "<your client ID>",
    "topic": "<your MQTT topic>"
}
```

Run the Virtual Board by executing the following Linux shell command to the directory where you stored the file:

```shell
python path/to/VirtualSimulator.py
```

Executing the `VirtualSimulator.py` code should immediately start the GUI.

If you are able to see the Virtual Board, then you are sending data to the Cloud already ! Login to your dashboard and let's check out how changing your sensor states is reflected on the dashboard !

### Play around with the Virtual Board

Digital sensors on the GUI can be toggled on and off and should immediately show results on the RelayR Dashboard.
![Digital Sensors](/assets/DigitalSensors.png)

Analog sensors, in our case a Luminosity sensor, can be set to user-defined values by clicking **Change Value**.
![Analog Sensors](/assets/AnalogSensor.png)

Checking the **Enable automation** box will throw random values between 0 and 100.
![Analog Sensors Automation](/assets/AnalogAutomation.png)

The digital actuator on our GUI is a virtual buzzer. Try activating the buzzer from the Dashboard with the **True** and **False** buttons and check out how your GUI reacts to cloud instructions !
![Digital Actuator](/assets/DigitalActuator.png)

### Further Steps

You want to create new devices ? Add other digital and analog sensors or actuators ?
Go ahead, explore the commented code and make sure your new instances of sensors and actuators are also added to the Dashboard model so you can see them change states !

## License

Copyright (C) 2016 relayr GmbH, Camille Feghali <camille.feghali@relayr.io>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

Except as contained in this notice, the name(s) of the above copyright holders shall not be used in advertising or otherwise to promote the sale, use or other dealings in this Software without prior written authorization.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
