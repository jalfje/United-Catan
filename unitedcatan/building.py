from interfaceerror import InterfaceError
from resource import Resource


# Base interface for purchaseable items
class Item(object):

    def resource_cost(self):
        raise InterfaceError(self)

    def name(self):
        return self.__class__.__name__


# Base interface for development cards
class DevelopmentCard(Item):

    def resource_cost(self):
        return {Resource.SHEEP: 1,
                Resource.WHEAT: 1,
                Resource.ROCK: 1}

    def execute(self):
        return InterfaceError(self)

    def max_per_game(self):
        return InterfaceError(self)


# Base interface for buildings
class Building(Item):

    def __init__(self, owner_ID):
        self.__owner_ID = owner_ID

    def owner(self):
        return self.__owner_ID

    def max_per_player(self):
        raise InterfaceError(self)


class Settlement(Building):

    def __init__(self, owner_ID):
        Building.__init__(self, owner_ID)

    def resource_cost(self):
        return {Resource.WHEAT: 1,
                Resource.SHEEP: 1,
                Resource.BRICK: 1,
                Resource.LOG: 1}

    def max_per_player(self):
        return 5


class City(Building):

    def __init__(self, owner_ID):
        Building.__init__(self, owner_ID)

    def resource_cost(self):
        return {Resource.ROCK: 3,
                Resource.WHEAT: 2}

    def max_per_player(self):
        return 4


class Road(Building):

    def __init__(self, owner_ID):
        Building.__init__(self, owner_ID)

    def resource_cost(self):
        return {Resource.LOG: 1,
                Resource.BRICK: 1}

    def max_per_player(self):
        return 15
