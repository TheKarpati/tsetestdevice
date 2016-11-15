# Getting started without getting hands dirty: a ready-to-use virtual board connected to the relayr cloud (Python Edition)

Difficulty: easy (1 star out of 5). Addressed to people who very little programming experience.

Time required: max. 2 hours

## Your first steps to the cloud

As you may know, relayr provides a cloud where you can store and visualize data [in a pleasant way](https://dev.relayr.io/). From the cloud, you can also take actions according to the data coming up, and put in some logic for what you want to do and when.

But... where does this data come from?

In the IoT world, it comes from *sensors*. Connected objects are filled with it: light sensors, thermometers, motion or pressure sensors... A smartphone itself is the easiest example to think of! There are tons of different types of sensors, and they can be wired to [constrained devices](http://www.igi-global.com/dictionary/resource-constrained-device/42838). Those devices get the sensor data as electrical impulse and send in turn this data to the cloud via internet. Arduinos are the most popular example of constrained device but there are many, many others.

Now what if you don't have those sensors and that hardware? What if you want to try the relayr cloud and see how its widgets work, but have no sensors to connect it to?

This is what this post is for: help you ***simulate*** a board with sensors and connect it to the cloud. All of this from your computer, it's that simple!

No hardware, no circuit board, we want an introduction to the cloud before the electronics.

Now if you already got your hands dirty with hardware in the past, but have little to no experience with clouds, this post might still help you learn how to test some cloud logic and get inspired to take your projects to the next level. By taking out almost any hardware-related issue, this post is a convenient way to test the [Developer Dashboard](https://dev.relayr.io/) from home. For instance you can test how to send data from a luminosity sensor and receive the instruction to trigger a buzzer, but without actually wiring any electronic board. All the sensors and actuators are virtually simulated in your laptop, but communicate ***real*** messages to the relayr cloud.

Ok, want to get started already? Follow [this link](https://github.com/relayr/python-virtual-device) and ***connect your first virtual board*** to the [cloud](https://dev.relayr.io/)!