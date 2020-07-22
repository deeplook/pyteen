# pip install geojson, ipyleaflet

from geojson import Feature
from geojson.geometry import MultiLineString
from ipyleaflet import GeoJSON, Map

def make_grid(step):
    return Feature(
        geometry=MultiLineString(
            coordinates=[[( lon, -90), (lon,  90)] for lon in range(-180, 180 + step, step)] + \
                        [[(-180, lat), (180, lat)] for lat in range( -90,  90 + step, step)] ))

my_map = Map(zoom=1)
my_map.add_layer(GeoJSON(data=make_grid(30)))
