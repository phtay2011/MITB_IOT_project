# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 11:45:49 2020

@author: User
"""

import googlemaps
from datetime import datetime
import numpy as np

# Geocoding an address
class distance_duration_calculator:
    '''
    eg.
    node1 =(1.2968599,103.852202)
    node2 = (1.299629,103.854302)
    dd=distance_duration_calculator(node1 = node1,node2 = node2)
    #Get distance 
    dd.get_distance_duration()
    '''
    def __init__(self,node1,node2):
        self.node1 = node1
        self.node2 = node2
        self.time = datetime.now()
    

    def node_preprocessing(node):
        return str(node[0])+','+str(node[1])
    
    def get_distance_duration(self):
        #gmaps = googlemaps.Client(key="AIzaSyBmk1BJHzxokzHI-Sqzh-smTc1ME0GHnIU")
        gmaps = googlemaps.Client(key="AIzaSyAPldhz_3zhaTEzHdhSQ0J5HUzOVLiDmZk") 
        direction_results = gmaps.directions(distance_duration_calculator.node_preprocessing(self.node1),
                                     distance_duration_calculator.node_preprocessing(self.node2),
                                     mode="driving",
                                     departure_time = self.time )

        total_distance = round(direction_results[0]['legs'][0]['distance']['value']/1000,2)
        total_duration = round(direction_results[0]['legs'][0]['duration']['value']/3600,2)
        total_duration_in_min = int(np.ceil(total_duration*60))
        res = {'distance_in_km':total_distance,
               'duration_in_hours':total_duration,
               'duration_in_min':total_duration_in_min
               }
        return res

node1 =(1.2968599,103.852202)
node2 = (1.299629,103.854302)
dd=distance_duration_calculator(node1 = node1,node2 = node2)
#Get distance 
dd.get_distance_duration()