# pip install geopy

from itertools import combinations
from os import environ

from geopy.distance import great_circle
from geopy.geocoders import Here, Nominatim

from .compare_geolocators import multi_geocode


def test_geolocators():
    """Test if locations from various geolocators are more than 1km apart.
    """
    geocoders = [Nominatim(user_agent="pyteen")]
    try:
        apikey = environ["HEREMAPS_API_KEY"]
        geocoders.append(Here(apikey=apikey))
    except KeyError:
        pass
    query = "Berlin, Germany"
    locations = list(multi_geocode(query, geocoders=geocoders))
    for (p, q) in combinations(locations, 2):
        dist = great_circle((p["lat"], p["lon"]), (q["lat"], q["lon"]))
        msg = f"Geocoders {p['name']} and {q['name']} return locations {dist} km apart."
        assert dist <= 1, msg
