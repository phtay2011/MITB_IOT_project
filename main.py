from flask import Flask, request

import gmap_api
from utils import get_geo_loc
import mqtt_module
from flask_cors import CORS, cross_origin

# Pre defined nodes
ambulance_node = (1.290081, 103.845511)
hospital_node = (1.33553, 103.74387)

server = Flask(__name__)
CORS(server, support_credentials=True)

# api 1 - to generate the starting route
@server.route("/generate_starting_route")
def generate_starting_route():
    dd = gmap_api.distance_duration_calculator(
        node1=ambulance_node, node2=hospital_node
    )
    get_result = dd.get_distance_duration()
    traffic_light_color_str = "".join(get_result["traffic_light_color"])
    mqtt_module.publish_gateway_to_broker(traffic_light_color_str)
    return get_result


@server.route("/generate_starting_route_with_origin_destination", methods=["POST"])
def generate_starting_route_with_origin_destination():
    requester_input = request.json
    origin_node = tuple(requester_input["origin_node"])
    destination_node = tuple(requester_input["destination_node"])
    dd = gmap_api.distance_duration_calculator(
        node1=origin_node, node2=destination_node
    )
    get_result = dd.get_distance_duration()
    traffic_light_color_str = "".join(get_result["traffic_light_color"])
    mqtt_module.publish_gateway_to_broker(traffic_light_color_str)
    return get_result


@server.route("/get_geo_location", methods=["POST"])
def generate_geo_location():
    requester_input = request.json
    node = tuple(requester_input["node"])
    geo = get_geo_loc(node)
    return f"{geo[0]},{geo[1]}"


# api 2 - When uesr click the next button, FE needs to take the xth index of the `traffic_light_nodes` list
# Input will be next_node
# eg.
# lat= 1.2910724
# long = 103.8463383


@server.route("/generate_route_from_next_node", methods=["POST"])
def generate_route_from_next_node():
    requester_input = request.json
    next_node = tuple(requester_input["node"])
    next_button = gmap_api.distance_duration_calculator(
        node1=next_node, node2=hospital_node
    )
    get_result = next_button.get_distance_duration()

    # save traffic light colors as a string
    traffic_light_color_str = "".join(get_result["traffic_light_color"])
    # publish to mqtt
    mqtt_module.publish_gateway_to_broker(traffic_light_color_str)

    return get_result


if __name__ == "__main__":
    server.run(debug=True)
