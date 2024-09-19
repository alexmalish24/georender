"""Main module."""

import ipyleaflet
from ipyleaflet import basemaps

class Map(ipyleaflet.Map):
    def __init__(self, center = [20, 0], zoom = 2, **kwargs):
        super().__init__(center = center, zoom = zoom, **kwargs)
        
    def add_tile_layer(self, url, name, **kwargs):
        layer = ipyleaflet.TileLayer(url = url, name = name, **kwargs)
        self.add(layer)

    def add_basemap(self, name):
        
        if isinstance(name, str):
            url = eval(f"basemaps.{name}").build_url()
            self.add_tile_layer(url, name)
        else:
            self.add(name)
            
    def add_layer_control(self, position = 'topright'):
        self.add_control(ipyleaflet.LayersControl(position = position))

    def add_geojson(self, data, name = 'geojson', **kwargs):

        import json

        if isinstance(data, str):
            with open(data) as f:
                data = json.load(f)
        
        if 'style' not in kwargs:
            kwargs['style'] = {"color": "blue", "weight": 1, "fillColor": "blue", "fillOpacity": 0}

        if 'hover_style' not in kwargs:
            kwargs['hover_style'] = {"fillColor": "blue", "fillOpacity": 0.8}

        layer = ipyleaflet.GeoJSON(data = data, name = name, **kwargs)
        self.add(layer)

    def add_shp(self, data, name = 'shp', **kwargs):

        import geopandas as gpd

        if isinstance(data, str):
            data = gpd.read_file(data)

        if 'style' not in kwargs:
            kwargs['style'] = {"color": "blue", "weight": 1, "fillColor": "blue", "fillOpacity": 0}

        if 'hover_style' not in kwargs:
            kwargs['hover_style'] = {"fillColor": "blue", "fillOpacity": 0.8}

        layer = ipyleaflet.GeoData(geo_dataframe = data, name = name, **kwargs)
        self.add(layer)