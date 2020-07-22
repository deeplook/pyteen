# pip install ipyleaflet

import ipyleaflet
from pyteen.snippets.maps.map_grid import my_map

def test_map_grid():
    assert my_map.center == [0, 0]
    assert set(map(type, my_map.layers)) == {ipyleaflet.leaflet.GeoJSON, ipyleaflet.leaflet.TileLayer}
    geojson_layer = [l for l in my_map.layers if type(l)==ipyleaflet.leaflet.GeoJSON][0]
    assert geojson_layer.data["geometry"]["type"] == "MultiLineString"
