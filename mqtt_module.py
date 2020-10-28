# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 11:17:17 2020

@author: User
"""

import paho.mqtt.client as mqtt
import logging
import random
import getpass
import time

# Configure logging
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

MQTT_BROKER_HOSTNAME = "broker.mqttdashboard.com"


def publish_gateway_to_broker(message):
    # create mqtt client and assign callback functions
    client = mqtt.Client()

    # connect to broker
    client.connect(MQTT_BROKER_HOSTNAME, 1883, 60)

    # topic to publish to
    # {getpass.getuser()} and {random.randint(1, 100)} are the username and a random number on your PC, independent of the MQTT client/broker
    # topic = f"demo_g2b/{getpass.getuser()}-{random.randint(1, 100)}"
    topic = f"demo_g2b/{getpass.getuser()}-280490"
    """
    # publish the message
    logger.info(f"Publishing '{message}' to topic: {topic}")
    client.publish(topic=topic, payload=message, qos=0)
    
    """
    # loop infinitely
    counter = 0
    while counter < 5:
        # publish the message
        logger.info(f"Publishing '{message}' to topic: {topic}")
        client.publish(topic=topic, payload=message, qos=0)

        # wait for timeout=1 seconds, process any events during that 1s, then return. See https://pypi.org/project/paho-mqtt/#network-loop
        client.loop(timeout=1)

        # sleep for 2s
        time.sleep(0.5)

        # add 1 to counter
        counter += 1
