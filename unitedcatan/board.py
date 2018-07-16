from coordinates import Hex, Edge, Vertex


class Board(object):

    def __init__(self):
        self.hexes, self.edges, self.vertices = self.init_hex_board()
        self.buildings = {}

    # initializes a hexagonal board with a given radius
    def init_hex_board(self, radius=2):
        hexes = set()
        edges = set()
        vertices = set()
        for q in range(-radius, radius+1):
            r1 = max(-radius, -q - radius)
            r2 = min(radius, -q + radius)
            for r in range(r1, r2+1):
                hexes.add(Hex(q, r))
        for h in hexes:
            edges.update([edge for edge in h.borders()])
            vertices.update([vertex for vertex in h.corners()])
        return hexes, edges, vertices

    # TODO: actually implement this
    def can_place(self, player, building, location, is_setup=False):
        if location isinstance Hex:
            return location in self.hexes
        elif location isinstance Edge:
            return location in self.edges
        elif location isinstance Vertex:
            return location in sefl.vertices
        else:
            return False
