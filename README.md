# Connect a virtual board with sensors and actuators to the relayr cloud (Python Edition)

*OMG AWESOME*

## Introduction

This post is addressed to users who want to send and receive data from the relayr cloud without any hardware.

It is a convenient way to test the [Developer Dashboard](https://dev.relayr.io/) and software logic by separating it from any hardware-related issue. For instance you can test how to send data from a luminosity sensor and receive the instruction to trigger a buzzer, but without actually wiring any electronic board. All the sensors and actuators are virtually simulated in your laptop, but communicate ***real*** messages to the relayr cloud.

This post will show you how to ***create this virtual simulation*** of hardware sensors and actuators and connect them to the [Developer Dashboard](https://dev.relayr.io/) using an intuitive GUI:

![Virtual Board](/assets/VirtualBoard.png)


## Requirements

No hardware is required.

On the software side, you need to be able to run Python 2.7.x, and you need an account on the [Developer Dashboard](https://dev.relayr.io/). If you have a Mac or Linux machine, you ought to have Python built-in. If you run on Windows, just download the latest [Python 2.7.x](https://www.python.org/downloads/).

## Installation & configuration

The tutorial is divided in two steps:

1. On the dashboard side, the creation of a device that corresponds to our Virtual Board.
2. On our computer, setup and run the Virtual Board.


### Create a Device in the [developer dashboard](https://dev.relayr.io/)

The first step is to create a representation of our Virtual Board in the relayr Cloud. The simplest way is to create a device running on the **Intel Edison Model**, because we will be simulating similar sensors. This entity will allow you to manage sent/received data and MQTT credentials through the relayr Developer Dashboard. To create a device on the Developer Dashboard follow the [**Devices Guide**](http://docs.relayr.io/getting-started/devices-guide/), filter your search "By the community" and select the **Intel Edison (IoT Acceleration Starter Kit)** as a *Device Model*.

If you prefer to create your own model in order to use more advanced features, follow the instructions of [this tutorial](http://docs.relayr.io/getting-started/device-models-guide/).

But for now, let's assume we are running the *Intel Edison (IoT Acceleration Starter Kit)* model.

### Get Paho-MQTT on your computer

In order to run the Python code provided in the github repository, we need first to install the [`paho-mqtt`](https://pypi.python.org/pypi/paho-mqtt/1.1) package, which provides a MQTT client library and enables sending/receiving of messages to/from a MQTT broker. [MQTT](https://en.wikipedia.org/wiki/MQTT) is a lightweight messaging protocol built on top of TCP/IP. We chose it for exchanging messages between the cloud and the Virtual Board because of its simplicity and low overhead.

It is often good practice to run packages on virtual environments (like a sandbox within your computer). So let's follow the following command lines to install `paho-mqtt`.

```shell
virtualenv ENV
source ENV/bin/activate
pip install paho-mqtt
```

If you are a Windows user, you can download the library [here](https://pypi.python.org/pypi/paho-mqtt/1.2) and place it in your python repository.

Once installed, we can use `paho-mqtt` classes by importing the module into our script. To learn more about the functionalities of the `paho-mqtt` Python client, see the
[official documentation](https://pypi.python.org/pypi/paho-mqtt/1.1).

We are now ready to make use of MQTT and run the Virtual Board!

## Starting the GUI and using the Virtual Board

First, clone the github repository to your prefered location on your computer.

### Starting the GUI (`VirtualSimulator.py`)

Run the Virtual Board by executing the following Linux shell command where you stored the file: 'path/to' has to be replaced by the directory you cloned the github repository to. *Note: Be sure to run it within your virtual environment ENV, to make sure you benefit from the paho-mqtt library.*

```shell
python path/to/VirtualSimulator.py
```

Executing `VirtualSimulator.py` should immediately start the following credentials GUI:
![Credentials GUI](/assets/CredentialsGUI.png)

What we need to do now is link the Virtual Board to the dashboard device. This will be done thanks to your device's unique credentials. To get them, click on the little pen next to your device's name.
![Device Credentials](/assets/DeviceCredentials.png)

*Note: whenever you create a device on the Developper Dashboard, relayr gives it unique credentials that you will need to later link any physical board to this dashboard device. In our tutorial, we link a *virtual* board to that dashboard device.*

Copy the device's credentials and paste them into the GUI. Make sure to paste the brackets too.

```python
{
    "user": "<your user ID>",
    "password": "<your password>",
    "clientId": "<your client ID>",
    "topic": "<your MQTT topic>"
}
```

Now press "Let's go!". If you see the GUI of the Virtual Board, then you are sending data to the Cloud already!

Since the Virtual Board is running *VirtualSimulator.py* with your device credentials, you can monitor it from the dashboard and see how changing your sensor states is reflected on the dashboard !

### Play around with the Virtual Board

Digital sensors on the GUI can be toggled on and off and should immediately show results on the Developer Dashboard.
![Digital Sensors](/assets/DigitalSensors.png)

Analog sensors - in our case, a luminosity sensor and a thermometer - can be set to user-defined values by clicking **Change Value**.
![Analog Sensors](/assets/AnalogSensor.png)

Checking the **Enable automation** box will throw random values between 0 and 100.
![Analog Sensors Automation](/assets/AnalogAutomation.png)

The digital actuator on our GUI is a virtual buzzer. Try activating the buzzer from the Dashboard with the **True** and **False** buttons and see how your GUI reacts to cloud instructions!
![Digital Actuator](/assets/DigitalActuator.png)

### Further Steps

If you want to create new devices, or add other digital and analog sensors or actuators, feel free to explore the commented code. Make sure your new instances of sensors and actuators are also added to the Dashboard model so you can see them change states!

## License

Copyright (C) 2016 relayr GmbH, Camille Feghali <camille.feghali@relayr.io>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

Except as contained in this notice, the name(s) of the above copyright holders shall not be used in advertising or otherwise to promote the sale, use or other dealings in this Software without prior written authorization.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
