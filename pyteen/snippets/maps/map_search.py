# pip install geopy, ipyleaflet

from functools import partial
from geopy.geocoders import Nominatim
from ipyleaflet import Map, Marker, WidgetControl
from ipywidgets import Layout, Text

def search(sender, m):
    loc = Nominatim(user_agent="map_search").geocode(sender.value)
    lat, lon = loc.latitude, loc.longitude
    m.center = [lat, lon]
    m += Marker(location=m.center)

m = Map(center=[0, 0], zoom=2)
tx = Text(layout=Layout(width="200px"))
tx.on_submit(partial(search, m=m))
m += WidgetControl(widget=tx, position="topright")
