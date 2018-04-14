import numpy as np
from random import shuffle


class VecPattern:
    """
    The pattern is composed of sets of Polygons
    """

    def __init__(self, parameters):
        try:
            self.width = np.abs(parameters['width'])
            self.height = np.abs(parameters['height'])
            self.polygon_size = max(1, np.abs(parameters['polygon_size']))
            self.color_bleed = np.abs(parameters['color_bleed'])
            if 'max_depth' in parameters.keys():
                self.max_depth = max(0, np.abs(parameters['max_depth']))
            else:
                self.max_depth = 15
            self.colors = parameters['colors']

            if len(self.colors) == 0:
                self.colors = ['#000000']

            self.list_polygons = []
            self.nbr_polygons = 0

        except KeyError:
            raise KeyError("Please check that your parameter dictionary is correctly written.")

    def add_polygon(self, p):
        self.list_polygons.append(p)

    def shuffle_polygons(self):
        self.nbr_polygons = len(self.list_polygons)
        shuffle(self.list_polygons)
