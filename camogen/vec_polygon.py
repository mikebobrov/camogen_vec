class VecPolygon:
    def __init__(self, polygon_geom):
        """
        Constructor with the color index
        :param color_index: Index of the color
        """
        self.geom = polygon_geom
        self.list_neighbours = []

    def add_neighbour(self, polygon):
        self.list_neighbours.append(polygon)

