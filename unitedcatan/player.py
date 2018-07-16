from collections import defaultdict
import random


class Player(object):

    def __init__(self, id_, name, colour):
        self.id = id_
        self.name = name
        self.colour = colour
        self._resources = defaultdict(int)
        self._development_cards = []
        self.victory_points = 0

    def get_resources(self):
        return self._resources

    def give_resources(self, resources):
        for resource, quantity in resources.items():
            self._resources[resource] += quantity

    def take_resources(self, resources):
        if not self.has_resources(resources):
            raise Exception("Cannot take resources")  # TODO: better exception
        for resource, quantity in resources.items():
            self._resources[resource] -= quantity

    def has_resources(self, resources):
        for resource, quantity in resources.items():
            if self._resources[resource] < quantity:
                return False
        return True

    def random_resource(self):
        if self.num_resources() == 0:
            return {}
        num = random.randrange(0, self.num_resources())
        cur = 0
        for resource, quantity in self._resources.items():
            if quantity == 0:
                continue
            cur += quantity
            if num < cur:
                return {resource: 1}

    def take_random_resource(self):
        res = self.random_resource()
        self.take_resources(res)
        return res

    def num_resources(self):
        return sum(self._resources.values())

