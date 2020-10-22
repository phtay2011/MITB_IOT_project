# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 12:48:30 2020

@author: Paul
"""
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
import platform

# Configure logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S',  level=logging.DEBUG)
logger = logging.getLogger(__name__)

MQTT_BROKER_HOSTNAME="broker.mqttdashboard.com"

'''
SECTION 1
This section will be responsible to receive the information via MQTT
'''
def demo_b2g_on_connect(client, userdata, flags, rc):

    # topic to subscribe to.
    # {getpass.getuser()} and {random.randint(1, 100)} are the username and a random number on your PC, independent of the MQTT client/broker
    topic = f"demo_g2b/{getpass.getuser()}-280490"
    print(f"Connected to {MQTT_BROKER_HOSTNAME}. Result code: {rc}")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)
    print(f"Subscribed to topic: {topic}")
    print(f"Publish something to {topic} and the messages will appear here.")


# Callback for when a message is received from the MQTT broker.
def demo_b2g_on_message(client, userdata, msg):
    print(f"msg.topic: {msg.topic}  msg.payload.decode('utf8'): {msg.payload.decode('utf8')}")

# To receive info via mqtt and print the output
def subscribe_broker_to_gatewy():
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
#subscribe_broker_to_gatewy()

'''
SECTION 2
This section will be responsible take the information from SECTION 1 and send it via serial to the gateway microbit 
'''
# Handles the case when the serial port can't be found
def handle_missing_serial_port():
    logger.error("Couldn't connect to the micro:bit. Try plugging in your micro:bit, closing all apps/browser tabs using the micro:bit, and try again.")
    exit()
    
# Initializes the serial device. Tries to guess which serial port the micro:bit is connected to
def init_serial_device():
    logger.info(f"sys.platform: {sys.platform}")
    logger.info("")

    serial_device = None
    if 'win' in sys.platform:

        # list the serial devices available
        try:
            stdout = subprocess.check_output('pwsh.exe -Command "[System.IO.Ports.SerialPort]::getportnames()"', shell = True).decode("utf-8").strip()
        except subprocess.CalledProcessError:
            logger.error(f"Error listing serial ports: {e.output.decode('utf8').strip()}")
            handle_missing_serial_port()

        # guess the serial device
        serial_device = re.search('COM([0-9]*)', stdout)
        if serial_device:
            serial_device = f"/dev/ttyS{serial_device.group(1)}"

    elif sys.platform == "linux" or sys.platform == "linux2": # Linux

        # list the serial devices available
        try:
            stdout = subprocess.check_output('ls /dev/ttyACM*', stderr=subprocess.STDOUT, shell = True).decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Error listing serial ports: {e.output.decode('utf8').strip()}")
            handle_missing_serial_port()

        # guess the serial device
        serial_device = re.search('(/dev/ttyACM[0-9]*)', stdout)
        if serial_device:
            serial_device = serial_device.group(1)

    elif sys.platform == "darwin": # OS X
        
        # list the serial devices available
        try:
            stdout = subprocess.check_output('ls /dev/cu.usbmodem*', stderr=subprocess.STDOUT, shell = True).decode("utf-8").strip()
        except subprocess.CalledProcessError:
            logger.error(f"Error listing serial ports: {e.output.decode('utf8').strip()}")
            handle_missing_serial_port()

        # guess the serial device
        serial_device = re.search('(/dev/cu.usbmodem[0-9]*)', stdout)
        if serial_device:
            serial_device = serial_device.group(1)

    else:
        logger.error(f"Unknown sys.platform: {sys.platform}")

    logger.info("Serial ports available:")
    logger.info(stdout)
    logger.info(f"serial_device: {serial_device}")

    return serial_device

# To publish from gateway to microbit_gateway via serial 
def demo_serial_g2s():
    serial_device = init_serial_device()
    with serial.Serial(serial_device, 115200, timeout=10) as s:
        time.sleep(1) # sleep to make sure serialport has been opened, before doing anything else
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
        
if __name__ == "__main__":

    # table mapping arguments to functions
    dispatcher = {
        'demo_serial_s2g' : demo_serial_s2g,
        'demo_serial_g2s' : demo_serial_g2s,
        'demo_radio_g2s' : demo_radio_g2s,
        'demo_g2b' : demo_g2b,
        'demo_b2g' : demo_b2g,
        'demo_s2g2b' : demo_s2g2b,
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
