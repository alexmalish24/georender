"""Main module."""

import ipyleaflet
from ipyleaflet import basemaps

class Map(ipyleaflet.Map):
    """This is the map class that inherits from ipyleaflet.Map. It has the same parameters as ipyleaflet.Map.

    Args:
        ipyleaflet (Map): The map class from ipyleaflet.
    """    
      
    def __init__(self, center = [20, 0], zoom = 2, **kwargs):
        super().__init__(center = center, zoom = zoom, **kwargs)
    """This is the constructor of the class. It initializes the map with the center and zoom parameters.
    
    Ards:
        center (list, optional): The center of the map. Defaults to [20, 0].
        zoom (int, optional): The zoom of the map. Defaults to 2.
    """   
    def add_tile_layer(self, url, name, **kwargs):
        layer = ipyleaflet.TileLayer(url = url, name = name, **kwargs)
        self.add(layer)

    def add_basemap(self, name):
        """
        Adds a basemap to the map.

        Args:
            name (str or object): The name of the basemap as a string or an object representing the basemap.
        
        Raises:
            TypeError: If the name is neither a string nor an object representing a basemap.
        """ 
        if isinstance(name, str):
            url = eval(f"basemaps.{name}").build_url()
            self.add_tile_layer(url, name)
        else:
            self.add(name)
            
    def add_layer_control(self, position = 'topright'):
        """
        Adds a layer control to the map.

        Args:
            position (str, optional): The position of the layer control. Defaults to 'topright'.
        """
        self.add_control(ipyleaflet.LayersControl(position = position))

    def add_geojson(self, data, name = 'geojson', **kwargs):
        """
        Adds a GeoJSON layer to the map.

        Args:
            data (str | dict): The GeoJSON data as a string or a dictionary.
            name (str, optional): The name of the layer. Defaults to 'geojson'.
        """

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

    def add_shp(self, data, name="shp", **kwargs):
        """
        Adds a shapefile to the map.

        Args:
            data (str or dict): The path to the shapefile as a string or a dictionary containing GeoJSON data.
            name (str, optional): The name of the shapefile layer. Defaults to "shp".
            **kwargs: Additional keyword arguments to pass to the add_geojson method.

        Example:
            m.add_shp('path/to/shapefile.shp', name='My Shapefile')
        """  
        import shapefile
        import json

        if isinstance(data, str):
            with shapefile.Reader(data) as shp:
                data = shp.__geo_interface__

        self.add_geojson(data, name, **kwargs)