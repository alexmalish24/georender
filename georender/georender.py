"""Main module."""

import ipyleaflet


class Map(ipyleaflet.Map):
    def __copy__(self):
        # Add your implementation here
        pass

    def __deepcopy__(self, memo):
        # Add your implementation here
        pass

    def __init__(self, center = [20, 0], zoom = 2, **kwargs):
        super().__init__(**kwargs)
        self.add_control(ipyleaflet.LayersControl(position='topright'))