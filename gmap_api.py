import googlemaps
from datetime import datetime
import numpy as np
import random

googleMapKey = "AIzaSyAPldhz_3zhaTEzHdhSQ0J5HUzOVLiDmZk"

# Geocoding an address
class distance_duration_calculator:
    """
    eg.
    node1 =(1.2968599,103.852202)
    node2 = (1.299629,103.854302)
    dd=distance_duration_calculator(node1 = node1,node2 = node2)
    #Get distance
    dd.get_distance_duration()
    """

    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.time = datetime.now()

    def node_preprocessing(node):
        return str(node[0]) + "," + str(node[1])

    def get_distance_duration(self):
        gmaps = googlemaps.Client(key=googleMapKey)
        direction_results = gmaps.directions(
            distance_duration_calculator.node_preprocessing(self.node1),
            distance_duration_calculator.node_preprocessing(self.node2),
            mode="driving",
            departure_time=self.time,
        )
        total_distance = round(
            direction_results[0]["legs"][0]["distance"]["value"] / 1000, 2
        )
        total_duration = round(
            direction_results[0]["legs"][0]["duration"]["value"] / 3600, 2
        )
        total_duration_in_min = int(np.ceil(total_duration * 60))

        traffic_light_nodes_lst = []
        for i in range(len(direction_results[0]["legs"][0]["steps"])):
            lat = direction_results[0]["legs"][0]["steps"][i]["end_location"]["lat"]
            lng = direction_results[0]["legs"][0]["steps"][i]["end_location"]["lng"]
            gps_node = (lat, lng)
            traffic_light_nodes_lst.append(gps_node)

        traffic_lights_location_lst = []
        traffic_lights_location_color = []
        for i in range(len(traffic_light_nodes_lst)):
            traffic_light_1 = (
                traffic_light_nodes_lst[i][0] + 0.000015,
                traffic_light_nodes_lst[i][1] + 0.000015,
            )
            traffic_light_2 = traffic_light_nodes_lst[i]
            traffic_light_3 = (
                traffic_light_nodes_lst[i][0] - 0.000015,
                traffic_light_nodes_lst[i][1] - 0.000015,
            )
            traffic_lights_location_lst.append(traffic_light_1)
            traffic_lights_location_lst.append(traffic_light_2)
            traffic_lights_location_lst.append(traffic_light_3)
            if i <= 3:
                traffic_lights_location_color.append("R")
                traffic_lights_location_color.append("G")
                traffic_lights_location_color.append("R")
            else:
                middle_traffic_color = random.choice(["R", "G"])
                left_right_traffic_color = np.setdiff1d(
                    ["R", "G"], [middle_traffic_color]
                )[0]
                traffic_lights_location_color.append(left_right_traffic_color)
                traffic_lights_location_color.append(middle_traffic_color)
                traffic_lights_location_color.append(left_right_traffic_color)
        res = {
            "ambulance_node": self.node1,
            "hospital_node": self.node2,
            "distance_in_km": total_distance,
            "duration_in_hours": total_duration,
            "duration_in_min": total_duration_in_min,
            "road_nodes": traffic_light_nodes_lst,
            "traffic_light_nodes": traffic_lights_location_lst,
            "traffic_light_color": traffic_lights_location_color,
        }
        return res


# ambulance_node = (1.290081, 103.845511)
# hospital_node = (1.33553, 103.74387)

# dd = distance_duration_calculator(node1=ambulance_node, node2=hospital_node)
# # Get distance
# dd.get_distance_duration()
