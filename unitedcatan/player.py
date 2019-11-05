from collections import defaultdict
import random


class Player(object):

    def __init__(self, id_, name, colour):
        self.id = id_
        self.name = name
        self.colour = colour
        self._resources = defaultdict(int)
        self._development_cards = []
        self.victoryPoints = 0

    def getResources(self):
        return self._resources

    def giveResources(self, resources):
        for resource, quantity in resources.items():
            self._resources[resource] += quantity

    def takeResources(self, resources):
        if not self.hasResources(resources):
            raise Exception("Cannot take resources")  # TODO: better exception
        for resource, quantity in resources.items():
            self._resources[resource] -= quantity

    def hasResources(self, resources):
        for resource, quantity in resources.items():
            if self._resources[resource] < quantity:
                return False
        return True

    def randomResource(self):
        if self.numResources() == 0:
            return {}
        num = random.randrange(0, self.numResources())
        cur = 0
        for resource, quantity in self._resources.items():
            if quantity == 0:
                continue
            cur += quantity
            if num < cur:
                return {resource: 1}

    def takeRandomResource(self):
        res = self.randomResource()
        self.takeResources(res)
        return res

    def numResources(self):
        return sum(self._resources.values())

