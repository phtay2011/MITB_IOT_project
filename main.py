# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 14:08:26 2020

@author: User
"""
import gmap_api
from flask import Flask, request

APP = Flask(__name__)


@APP.route('/')
def hello():
    return 'Hello, World!'

#Pre defined nodes
ambulance_node =(1.290081, 103.845511)
hospital_node = (1.33553,103.74387)

#api 1 - to generate the starting route 
@APP.route('/generate_starting_route')
def generate_starting_route():
    dd=gmap_api.distance_duration_calculator(node1 = ambulance_node ,node2 = hospital_node )
    #Get distance 
    return dd.get_distance_duration()

#api 2 - When uesr click the next button, FE needs to take the xth index of the `traffic_light_nodes` list
# Input will be next_node
#eg.
#lat= 1.2910724
#long = 103.8463383

@APP.route('/generate_route_from_next_node',methods=["POST"])
def generate_route_from_next_node():
    requester_input = request.json
    next_node = tuple(requester_input["node"])
    print(next_node )
    next_button=gmap_api.distance_duration_calculator(node1 = next_node ,node2 = hospital_node )
    #Get distance 
    return next_button.get_distance_duration()

if __name__ == "__main__":
    APP.run(debug=True)
    
    
