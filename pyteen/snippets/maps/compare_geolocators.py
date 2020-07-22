# pip install geopy

from typing import List, Optional
from geopy.geocoders.base import Geocoder

def multi_geocode(query_string: str, geocoders: Optional[List[Geocoder]] = None):
    """Yield geolocated query strings using multiple geocoders for comparison.
    
    >>> list(multi_geocode("Berlin, Germany", geocoders=[HERE(...), Nominatim(...)]))
    [{'name': 'Here', 'lat': 52.51605, 'lon': 13.37691},
     {'name': 'Nominatim', 'lat': 52.5170365, 'lon': 13.3888599}]
    """
    for gc in geocoders or []:
        loc = gc.geocode(query_string)
        yield dict(name=gc.__class__.__name__,
                   lat=loc.latitude,
                   lon=loc.longitude)
