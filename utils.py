import googlemaps

googleMapKey = "AIzaSyAPldhz_3zhaTEzHdhSQ0J5HUzOVLiDmZk"


def get_geo_loc(node):
    gmaps_client = googlemaps.Client(key=googleMapKey)
    geocode_result = gmaps_client.geocode(node)
    loc = geocode_result[0]["geometry"]["location"]
    geo_loc = (loc["lat"], loc["lng"])
    return geo_loc
