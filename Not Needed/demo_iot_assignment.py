#!/usr/bin/env python3

import serial
import time
import csv
import os
import subprocess
import re
import paho.mqtt.client as mqtt
import sys
import logging
import argparse
import getpass
import random

# Configure logging
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

MQTT_BROKER_HOSTNAME = "broker.mqttdashboard.com"

# Handles the case when the serial port can't be found
def handle_missing_serial_port():
    logger.error(
        "Couldn't connect to the micro:bit. Try plugging in your micro:bit, closing all apps/browser tabs using the micro:bit, and try again."
    )
    exit()


# Initializes the serial device. Tries to guess which serial port the micro:bit is connected to
def init_serial_device():
    logger.info(f"sys.platform: {sys.platform}")
    # logger.info(f"os.uname().release: {os.uname().release}")
    logger.info("")

    serial_device = None
    if "Microsoft" in os.uname().release:

        # list the serial devices available
        try:
            stdout = (
                subprocess.check_output(
                    'pwsh.exe -Command "[System.IO.Ports.SerialPort]::getportnames()"',
                    shell=True,
                )
                .decode("utf-8")
                .strip()
            )
        except subprocess.CalledProcessError:
            logger.error(
                f"Error listing serial ports: {e.output.decode('utf8').strip()}"
            )
            handle_missing_serial_port()

        # guess the serial device
        serial_device = re.search("COM([0-9]*)", stdout)
        if serial_device:
            serial_device = f"/dev/ttyS{serial_device.group(1)}"

    elif sys.platform == "linux" or sys.platform == "linux2":  # Linux

        # list the serial devices available
        try:
            stdout = (
                subprocess.check_output(
                    "ls /dev/ttyACM*", stderr=subprocess.STDOUT, shell=True
                )
                .decode("utf-8")
                .strip()
            )
        except subprocess.CalledProcessError as e:
            logger.error(
                f"Error listing serial ports: {e.output.decode('utf8').strip()}"
            )
            handle_missing_serial_port()

        # guess the serial device
        serial_device = re.search("(/dev/ttyACM[0-9]*)", stdout)
        if serial_device:
            serial_device = serial_device.group(1)

    elif sys.platform == "darwin":  # OS X

        # list the serial devices available
        try:
            stdout = (
                subprocess.check_output(
                    "ls /dev/cu.usbmodem*", stderr=subprocess.STDOUT, shell=True
                )
                .decode("utf-8")
                .strip()
            )
        except subprocess.CalledProcessError:
            logger.error(
                f"Error listing serial ports: {e.output.decode('utf8').strip()}"
            )
            handle_missing_serial_port()

        # guess the serial device
        serial_device = re.search("(/dev/cu.usbmodem[0-9]*)", stdout)
        if serial_device:
            serial_device = serial_device.group(1)

    else:
        logger.error(f"Unknown sys.platform: {sys.platform}")

    logger.info("Serial ports available:")
    logger.info(stdout)
    logger.info(f"serial_device: {serial_device}")

    return serial_device


# serial communications, sensor node → gateway
def demo_serial_s2g():
    serial_device = init_serial_device()
    with serial.Serial(serial_device, 115200, timeout=10) as s:
        time.sleep(
            1
        )  # sleep to make sure serialport has been opened, before doing anything else
        s.reset_input_buffer()
        while True:
            # read a line from the serial port, and display it
            line = s.readline().decode("utf-8").strip()
            print(line)


# serial communications, gateway → sensor node
def demo_serial_g2s():
    serial_device = init_serial_device()
    with serial.Serial(serial_device, 115200, timeout=10) as s:
        time.sleep(
            1
        )  # sleep to make sure serialport has been opened, before doing anything else
        s.reset_input_buffer()

        # write data to the serial port, sleeping 1s between writes
        logger.info("writing to serial port: set,5")
        s.write(f"set,5\n".encode())
        time.sleep(1)
        logger.info("writing to serial port: set,3")
        s.write(f"set,3\n".encode())
        time.sleep(1)
        logger.info("writing to serial port: set,1")
        s.write(f"set,1\n".encode())
        time.sleep(1)
        logger.info("writing to serial port: inc")
        s.write(f"inc\n".encode())
        time.sleep(1)
        logger.info("writing to serial port: inc")
        s.write(f"inc\n".encode())
        time.sleep(1)
        logger.info("writing to serial port: dec")
        s.write(f"dec\n".encode())
        time.sleep(1)
        logger.info("writing to serial port: dec")
        s.write(f"dec\n".encode())
        time.sleep(1)


# radio communications, gateway → sensor node
def demo_radio_g2s():
    serial_device = init_serial_device()

    # node id of the micro:bit
    node_id = 2

    with serial.Serial(serial_device, 115200, timeout=10) as s:
        time.sleep(
            1
        )  # sleep to make sure serialport has been opened before doing anything else
        s.reset_input_buffer()

        # write data to the serial port, sleeping 1s between writes
        logger.info(f"writing to serial port: {node_id},set,5")
        s.write(f"{node_id},set,5\n".encode())
        time.sleep(1)
        logger.info(f"writing to serial port: {node_id},set,3")
        s.write(f"{node_id},set,3\n".encode())
        time.sleep(1)
        logger.info(f"writing to serial port: {node_id},set,1")
        s.write(f"{node_id},set,1\n".encode())
        time.sleep(1)
        logger.info(f"writing to serial port: {node_id},inc")
        s.write(f"{node_id},inc\n".encode())
        time.sleep(1)
        logger.info(f"writing to serial port: {node_id},inc")
        s.write(f"{node_id},inc\n".encode())
        time.sleep(1)
        logger.info(f"writing to serial port: {node_id},dec")
        s.write(f"{node_id},dec\n".encode())
        time.sleep(1)
        logger.info(f"writing to serial port: {node_id},dec")
        s.write(f"{node_id},dec\n".encode())
        time.sleep(1)


# Callback for when the MQTT client connects
# This function is called once just after the mqtt client is connected to the server.
def demo_b2g_on_connect(client, userdata, flags, rc):

    # topic to subscribe to.
    # {getpass.getuser()} and {random.randint(1, 100)} are the username and a random number on your PC, independent of the MQTT client/broker
    topic = f"demo_b2g/{getpass.getuser()}-{random.randint(1, 100)}"
    print(f"Connected to {MQTT_BROKER_HOSTNAME}. Result code: {rc}")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)
    print(f"Subscribed to topic: {topic}")
    print(f"Publish something to {topic} and the messages will appear here.")


# Callback for when a message is received from the MQTT broker.
def demo_b2g_on_message(client, userdata, msg):
    print(
        f"msg.topic: {msg.topic}  msg.payload.decode('utf8'): {msg.payload.decode('utf8')}"
    )


# Broker 🠒 gateway
def demo_b2g():
    # create mqtt client and assign callback functions
    client = mqtt.Client()
    client.on_connect = demo_b2g_on_connect
    client.on_message = demo_b2g_on_message

    # connect to broker
    client.connect(MQTT_BROKER_HOSTNAME, 1883, 60)

    # loop infinitely
    while True:
        # wait for timeout=1 seconds, process any events during that 1s, then return. See https://pypi.org/project/paho-mqtt/#network-loop
        client.loop(timeout=1)


# Gateway 🠒 broker
def demo_g2b():
    # create mqtt client and assign callback functions
    client = mqtt.Client()

    # connect to broker
    client.connect(MQTT_BROKER_HOSTNAME, 1883, 60)

    # this is the message to publish
    message = 0

    # topic to publish to
    # {getpass.getuser()} and {random.randint(1, 100)} are the username and a random number on your PC, independent of the MQTT client/broker
    topic = f"demo_g2b/{getpass.getuser()}-{random.randint(1, 100)}"

    # loop infinitely
    while True:
        # publish the message
        logger.info(f"Publishing '{message}' to topic: {topic}")
        client.publish(topic=topic, payload=message, qos=0)

        # wait for timeout=1 seconds, process any events during that 1s, then return. See https://pypi.org/project/paho-mqtt/#network-loop
        client.loop(timeout=1)

        # add one to the message
        message += 1

        # sleep for 2s
        time.sleep(2)


# Sensor node 🠒  gateway 🠒 broker
def demo_s2g2b():
    # create mqtt client
    client = mqtt.Client()

    # connect to broker
    client.connect(MQTT_BROKER_HOSTNAME, 1883, 60)

    # the topic to publish to
    topic = f"demo_s2g2b/{getpass.getuser()}-{random.randint(1, 100)}"

    serial_device = init_serial_device()
    with serial.Serial(serial_device, 115200, timeout=10) as s:
        time.sleep(
            1
        )  # sleep to make sure serialport has been opened before doing anything else
        s.reset_input_buffer()

        # loop infinitely
        while True:
            # read from the serial port
            message = s.readline().decode("utf-8").strip()

            # publish the message
            logger.info(f"Publishing '{message}' to topic: {topic}")
            client.publish(topic=topic, payload=message, qos=0)

            # wait for timeout=1 seconds, process any events during that 1s, then return. See https://pypi.org/project/paho-mqtt/#network-loop
            client.loop(timeout=1)

            # sleep for 2s
            time.sleep(2)


if __name__ == "__main__":

    # table mapping arguments to functions
    dispatcher = {
        "demo_serial_s2g": demo_serial_s2g,
        "demo_serial_g2s": demo_serial_g2s,
        "demo_radio_g2s": demo_radio_g2s,
        "demo_g2b": demo_g2b,
        "demo_b2g": demo_b2g,
        "demo_s2g2b": demo_s2g2b,
    }

    logger.info("Press Ctrl-C to stop")

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("demo_name", help=f"{list(dispatcher.keys())}")
    args = parser.parse_args()

    try:
        # call function
        dispatcher[args.demo_name]()
    except KeyError:
        logger.error(f"No such demo: {args.demo_name}")
        exit()
