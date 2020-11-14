import googlemaps

googleMapKey = "AIzaSyAPldhz_3zhaTEzHdhSQ0J5HUzOVLiDmZk"


def get_geo_loc(node):
    gmaps_client = googlemaps.Client(key=googleMapKey)
    geocode_result = gmaps_client.geocode(node)
    loc = geocode_result[0]["geometry"]["location"]
    geo_loc = (loc["lat"], loc["lng"])
    return geo_loc

def get_geo_loc_v2(node):
    hospital_dic = {
    "378 Alexandra Rd, Singapore 159964": (1.286490,103.801270),
    "38 Irrawaddy Rd, Singapore 329563":(1.322110,103.844307),
    "1 Jurong East Street 21, Singapore 609606":(1.333300,103.745850),
    "5 Lower Kent Ridge Rd, Singapore 119074":(1.294970,103.782944),
    "81 Victoria St, Singapore 188065":(1.2968599, 103.852202),
    "585 North Bridge Road Raffles Hospital, 188770":(1.3011894, 103.8572771),
    "11 Jln Tan Tock Seng, Singapore 308433":(1.320966,103.846626)
    }
    geo_loc = hospital_dic[node]
    result = {"result":geo_loc}
    return result
