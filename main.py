import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask, request

import gmap_api
import mqtt_module
from dashboard.management_portal_page import Management_Portal_Layout
from dashboard.one_ambulance_route_component import One_Ambulance_Layout

# Pre defined nodes
ambulance_node = (1.290081, 103.845511)
hospital_node = (1.33553, 103.74387)

server = Flask(__name__)

external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    dbc.themes.BOOTSTRAP,
    "https://codepen.io/chriddyp/pen/brPBPO.css",
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    server=server,
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
    ]
)


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/":
        return Management_Portal_Layout
    elif pathname == "/the_ambulance_route":
        return One_Ambulance_Layout
    return Management_Portal_Layout


# api 1 - to generate the starting route
@server.route("/generate_starting_route")
def generate_starting_route():
    dd = gmap_api.distance_duration_calculator(
        node1=ambulance_node, node2=hospital_node
    )
    # Get distance
    get_result = dd.get_distance_duration()

    # save traffic light colors as a string
    traffic_light_color_str = "".join(get_result["traffic_light_color"])
    # publish to mqtt
    mqtt_module.publish_gateway_to_broker(traffic_light_color_str)
    return get_result


# api 2 - When uesr click the next button, FE needs to take the xth index of the `traffic_light_nodes` list
# Input will be next_node
# eg.
# lat= 1.2910724
# long = 103.8463383


@server.route("/generate_route_from_next_node", methods=["POST"])
def generate_route_from_next_node():
    requester_input = request.json
    next_node = tuple(requester_input["node"])
    print(next_node)
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
    app.run_server(debug=True)
