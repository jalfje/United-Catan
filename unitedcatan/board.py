from coordinates import Hex, Edge, Vertex
from hextype import HexType
from random import shuffle
from catanerrors import NoHexNumberError


class Board(object):

    def __init__(self):
        self.hexset, self.edgeset, self.vertexset = self._initHexGrid()
        self._buildings = {}  # location->[buildings] map
        defaultHexTypes = {HexType.DESERT: 1,
                            HexType.WATER: 0,
                            HexType.MOUNTAIN: 4,
                            HexType.FIELD: 4,
                            HexType.GRASS: 3,
                            HexType.FOREST: 4,
                            HexType.CLAY: 3}
        defaultNumbers = {2: 1,
                          3: 2,
                          4: 2,
                          5: 2,
                          6: 2,
                          7: 0,
                          8: 2,
                          9: 2,
                          10: 2,
                          11: 2,
                          12: 1}
        self._hextypes, self._hexnumbers = self.randomizeHexTypesAndNumbers(self.hexset,
                                                           defaultHexTypes,
                                                           defaultNumbers)

    # initializes a hexagonal board with a given radius
    # use default radius=2 for vanilla catan board
    # doesn't fill in the board with resources etc
    def _initHexGrid(self, radius=2):
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

    # Doesn't need to be in the class, but it works well enough in here
    def randomizeHexTypesAndNumbers(self, hexset, hextypes, numbers):

        # Create list to get hextypes from
        resList = [k for k, n in hextypes.items() if n > 0 for _ in range(n)]
        # Create list to get numbers from
        numList = [k for k, n in numbers.items() if n > 0 for _ in range(n)]

        # check resource list has at least as many hexes as the board does
        if len(hexset) > len(resList):
            # TODO: raise other error
            raise Exception("Not enough hextypes to fill every hex! Ahhhh!")

        if len(numList) < len([r for r in resList if r.needsNumber()]):
            # TODO: raise other error
            raise Exception("Not enough numbers to fill every resource! Ahhh!")

        shuffle(resList)
        shuffle(numList)

        outHextypes = {}
        outNumbers = {}
        j = 0
        for i, h in enumerate(hexset):
            outHextypes[h] = resList[i]
            if outHextypes[h].needsNumber():
                outNumbers[h] = numList[j]
                j = j + 1

        return outHextypes, outNumbers

    # Gets the building at a location. Default to None if none exists.
    def getBuilding(self, location):
        try:
            b = self._buildings[location]
        except KeyError:
            b = None

        return b

    # Get the hex type at a location. Default to WATER if the hex is off board.
    def getHexType(self, the_hex):
        try:
            t = self._hextypes[the_hex]
        except KeyError:
            t = HexType.WATER

        return t

    # Get the number for a hex
    def getNumber(self, the_hex):
        try:
            n = self._hexnumbers[the_hex]
        except KeyError:
            raise NoHexNumberError()

        return n

    # Given a player trying to place a building in a place, and knowing whether
    # or not we're in the setup phase (where building settlement rules are more
    # lax), determine whether the player can place the building there.
    def canPlace(self, player, building, location, is_setup=False):
        if isinstance(location, Hex):
            if location not in self.hexset:
                return False
            return building.canPlaceHex(player, self, location, is_setup)
        elif isinstance(location, Edge):
            if location not in self.edgeset:
                return False
            return building.canPlaceEdge(player, self, location, is_setup)
        elif isinstance(location, Vertex):
            if location not in self.vertexset:
                return False
            return building.canPlaceVertex(player, self, location, is_setup)
        else:
            raise TypeError("location must be hex, edge, or vertex. This shouldn't have happened.")
