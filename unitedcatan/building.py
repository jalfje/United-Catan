from catanerrors import InterfaceError
from resource import Resource
from hextype import HexType
import board
import coordinates


# Base interface for purchaseable items
class Item(object):

    def resourceCost(self):
        raise InterfaceError(self)

    def name(self):
        return self.__class__.__name__


# Base interface for development cards
class DevelopmentCard(Item):

    def resourceCost(self):
        return {Resource.SHEEP: 1,
                Resource.WHEAT: 1,
                Resource.ROCK: 1}

    def execute(self):
        return InterfaceError(self)

    def maxPerGame(self):
        return InterfaceError(self)


# Base interface for buildings
class Building(Item):

    def __init__(self, ownerID, maxPerPlayer, buildLocation):
        self._ownerID = ownerID
        self._maxPerPlayer = maxPerPlayer
        self._buildLocation = buildLocation

    def owner(self):
        return self._ownerID

    def maxPerPlayer(self):
        return self._maxPerPlayer

    # TODO: change buildLocation to Enum instead of string
    # Each subclass of Building overwrites the necessary function
    def canPlaceHex(self, player, theBoard, theHex, isSetup):
        return False

    def canPlaceEdge(self, player, theBoard, theEdge, isSetup):
        return False

    def canPlaceVertex(self, player, theBoard, theVertex, isSetup):
        return False


# Superclass for City and Settlement (and possibly Metropolis in future)
class Colony(Building):

    def __init__(self, ownerID, maxPerPlayer):
        Building.__init__(self, ownerID, maxPerPlayer, "Vertex")

    def resourcesGenerated(self):
        raise InterfaceError(self)


# Superclass for Ship and Road
class Path(Building):

    def __init__(self, ownerID, maxPerPlayer):
        Building.__init__(self, ownerID, maxPerPlayer, "Edge")


class Settlement(Colony):

    def __init__(self, ownerID):
        Colony.__init__(self, ownerID, 5)

    def resourceCost(self):
        return {Resource.WHEAT: 1,
                Resource.SHEEP: 1,
                Resource.BRICK: 1,
                Resource.LOG: 1}

    def resourcesGenerated(self):
        return 1

    # TODO: check for water (land must be on one adjacent hex)
    def canPlaceVertex(self, player, theBoard, theVertex, isSetup):
        nearbyVertices = theVertex.adjacents()
        nearbyEdges = theVertex.protrudes()

        for n in nearbyVertices:
            b = theBoard.getBuilding(n)
            if isinstance(b, Settlement) or isinstance(b, City):
                return False

        if not isSetup:
            for e in nearbyEdges:
                b = theBoard.getBuilding(e)
                if b is not None and b.owner() == player.id:
                    return True

        return True


class City(Colony):

    def __init__(self, ownerID):
        Colony.__init__(self, ownerID, 4)

    def resourceCost(self):
        return {Resource.ROCK: 3,
                Resource.WHEAT: 2}

    def resourcesGenerated(self):
        return 2

    def canPlaceVertex(self, player, theBoard, theVertex, isSetup):
        curBuilding = theBoard.getBuilding(theVertex)

        if isinstance(curBuilding, Settlement) and curBuilding.owner() == player.id:
            return True
        else:
            return False


class Road(Path):

    def __init__(self, ownerID):
        Path.__init__(self, ownerID, 15)

    def resourceCost(self):
        return {Resource.LOG: 1,
                Resource.BRICK: 1}

    def canPlaceEdge(self, player, theBoard, theEdge, isSetup):
        nearbyHexes = theEdge.joins()
        nearbyEdges = theEdge.continues()
        nearbyVertices = theEdge.endpoints()

        existingRoad = theBoard.getBuilding(theEdge)

        if isinstance(existingRoad, Path):
            return False

        bordersLand = False
        for h in nearbyHexes:
            theHex = theBoard.getHexType(h)
            if theHex != HexType.WATER:
                bordersLand = True

        if not bordersLand:
            return False

        # TODO: deal with corner case of putting a road through an opponent's
        # settlement being invalid
        for n in nearbyVertices:
            curBuilding = theBoard.getBuilding(n)
            if isinstance(curBuilding, Colony) and curBuilding.owner() == player.id:
                return True

        for e in nearbyEdges:
            curPath = theBoard.getBuilding(e)
            if isinstance(curPath, Road) and curPath.owner() == player.id:
                return True

        return False


class Ship(Path):

    def __init__(self, ownerID):
        Path.__init__(self, ownerID, 15)

    def resourceCost(self):
        return {Resource.LOG: 1,
                Resource.SHEEP: 1}

    # Precondition: theEdge exists within theBoard (or at least theBoard
    # manages access. TODO: make theBoard manage access to edges properly)
    def canPlaceEdge(self, player, theBoard, theEdge, isSetup):
        nearbyHexes = theEdge.joins()
        nearbyEdges = theEdge.continues()
        nearbyVertices = theEdge.endpoints()

        existingBuilding = theBoard.getBuilding(theEdge)

        if isinstance(existingBuilding, Path):
            return False

        bordersWater = False
        for h in nearbyHexes:
            theHex = theBoard.getHexType(h)
            if theHex == HexType.WATER:
                bordersWater = True

        if not bordersWater:
            return False

        # TODO: deal with corner case of putting a ship through an opponent's
        # settlement being invalid
        for n in nearbyVertices:
            curBuilding = theBoard.getBuilding(n)
            if isinstance(curBuilding, Colony) and curBuilding.owner() == player.id:
                return True

        for e in nearbyEdges:
            curPath = theBoard.getBuilding(e)
            if isinstance(curPath, Ship) and curPath.owner() == player.id:
                return True

        return False

