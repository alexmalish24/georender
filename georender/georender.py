"""Main module."""

import ipyleaflet
from ipyleaflet import basemaps
import ipywidgets as widgets

class Map(ipyleaflet.Map):
    """This is the map class that inherits from ipyleaflet.Map. It has the same parameters as ipyleaflet.Map.

    Args:
        ipyleaflet (Map): The map class from ipyleaflet.
    """    
      
    def __init__(self, center = [20, 0], zoom = 2, **kwargs):
        """
        This is the constructor of the class. It initializes the map with the center and zoom parameters.
    
        Ards:
            center (list, optional): The center of the map. Defaults to [20, 0].
            zoom (int, optional): The zoom of the map. Defaults to 2.
        """

        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        super().__init__(center = center, zoom = zoom, **kwargs)
       
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

    def add_image(self, url, bounds, name = 'image', **kwargs):
        """
        Adds an image overlay to the map.

        Args:
            url (str): The URL of the image.
            bounds (list): The bounds of the image as [[lat1, lon1], [lat2, lon2]].
            name (str, optional): The name of the image overlay. Defaults to 'image'.
        """
        layer = ipyleaflet.ImageOverlay(url = url, bounds = bounds, name = name, **kwargs)
        self.add(layer)

    def add_raster(self, data, name = 'raster', zoom_to_layer = True, **kwargs):
        """
        Adds a raster layer to the map.

        Args:
            data (str): The path to the raster file.
            name (str, optional): The name of the raster layer. Defaults to 'raster'.
        """

        try:
            from localtileserver import TileClient, get_leaflet_tile_layer
        
        except ImportError:
            raise ImportError("Please install the localtileserver package to use this feature.")

        client = TileClient(data)
        layer = get_leaflet_tile_layer(client, name=name, **kwargs)
        self.add(layer) 

        if zoom_to_layer:
            self.center = client.center()
            self.zoom = client.default_zoom
    
    def add_zoom_slider( 
        self, description="Zoom level", min=0, max=24, value=10, position="topright"
    ):
        """Adds a zoom slider to the map.

        Args:
            position (str, optional): The position of the zoom slider. Defaults to "topright".
        """
        zoom_slider = widgets.IntSlider(
            description=description, min=min, max=max, value=value
        )

        control = ipyleaflet.WidgetControl(widget=zoom_slider, position=position)
        self.add(control)
        widgets.jslink((zoom_slider, "value"), (self, "zoom"))

    def add_widget(self, widget, position="topright"):
        """Adds a widget to the map.

        Args:
            widget (object): The widget to be added.
            position (str, optional): The position of the widget. Defaults to "topright".
        """
        control = ipyleaflet.WidgetControl(widget=widget, position=position)
        self.add(control)

    def add_opacity_slider(
        self, layer_index=-1, description="Opacity", position="topright"
    ):
        """Adds an opacity slider to the map.

        Args:
            layer (object): The layer to which the opacity slider is added.
            description (str, optional): The description of the opacity slider. Defaults to "Opacity".
            position (str, optional): The position of the opacity slider. Defaults to "topright".
        """
        layer = self.layers[layer_index]
        opacity_slider = widgets.FloatSlider(
            description=description,
            min=0,
            max=1,
            value=layer.opacity,
            style={"description_width": "initial"},
        )

        def update_opacity(change):
            layer.opacity = change["new"]

        opacity_slider.observe(update_opacity, "value")

        control = ipyleaflet.WidgetControl(widget=opacity_slider, position=position)
        self.add(control)

    def add_basemap_gui(self, basemaps=None, position="topright"):
        """Adds a basemap GUI to the map.

        Args:
            position (str, optional): The position of the basemap GUI. Defaults to "topright".
        """

        basemap_selector = widgets.Dropdown(
            options=[
                "OpenStreetMap",
                "OpenTopoMap",
                "Esri.WorldImagery",
                "Esri.NatGeoWorldMap",
                "CartoDB.Positron",
                "CartoDB.DarkMatter",
            ],
            description="Basemap",
        )

        def update_basemap(change):
            self.add_basemap(change["new"])

        basemap_selector.observe(update_basemap, "value")

        control = ipyleaflet.WidgetControl(widget=basemap_selector, position=position)
        self.add(control)
