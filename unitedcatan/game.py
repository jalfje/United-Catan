from coordinates import Direction, Hex, Edge, Vertex
from player import Player
from resource import Resource
from hextype import HexType
import building
from board import Board

class Game(object):

    # these are useless at present, but once we have a GUI they could be useful
    _colours = ["RED", "BLUE", "WHITE", "ORANGE", "GREEN", "BROWN"]

    def __init__(self, num_players=2):
        self.board = Board()
        # initialize player objects
        # TODO: make players a dict referencable by player ID, and separately
        # have a list of players in turn order.
        self.players = []
        for p in range(0, num_players):
            name = "Player " + str(p+1)
            colour = Game._colours[p % len(Game._colours)]
            player = Player(p, name, colour)
            self.players.append(player)
        # victory points required for victory
        self.victoryPoints = 10

    def placeStartBuildings(self):
        # place first set of settlement/road pairs, in order of play
        for player in self.players:
            self.placeInitialSettlement(player)

        # place second set of settlement/road pairs, in reverse order of play
        for player in reversed(self.players):
            self.placeInitialSettlement(player)

    def placeInitialSettlement(self, player):
        # get player to place a settlement
        valid_settlement = False
        while not valid_settlement:
            ask_str = player.name + ", where will you place your first settlement?"
            vertex = self.get_input_vertex(ask_str)
            valid_settlement = self.board.canPlace(player,
                                                   building.Settlement,
                                                   vertex,
                                                   is_setup=True)
            if not valid_settlement:
                print("You can't place your settlement there.")
        # get player to place a road
        valid_road = False
        while not valid_road:
            ask_str = player.name + ", where will you place your first road?"
            edge = self.get_input_edge(ask_str)
            valid_loc = self.board.canPlace(player, building.Road,
                                             edge, is_setup=True)
            valid_road = valid_loc and vertex.is_protruding(edge)
            if not valid_road:
                print("You can't place your road there.")


    # Returns a Vertex object input by the user
    # TODO: convert this to something that could be GUI or text-based
    def get_input_vertex(self, disp_str=""):
        valid_input = False
        while not valid_input:
            try:
                d, q, r, s = self._get_loc_input(disp_str)
                vertex = Vertex(d, q, r, s)
                valid_input = True
            except:
                print("Invalid location input.")
        return vertex


    # Returns an Edge object input by the user
    # TODO: convert this to something that could be GUI or text-based
    def get_input_edge(self, disp_str=""):
        valid_input = False
        while not valid_input:
            try:
                d, q, r, s = self._get_loc_input(disp_str)
                edge = Edge(d, q, r, s)
                valid_input = True
            except Exception:  # TODO: better exception handling
                print("Invalid location input.")
        return edge

    # Returns d, q, r, s, which can be used to create a Vertex or Edge object.
    def _get_loc_input(self, disp_str):
        # ask for input
        raw_in = input(disp_str + " ").split()
        # verify direction/q/r or direction/q/r was entered
        assert(len(raw_in) in [3, 4])
        # convert to correct types
        d = Direction[raw_in[0]]
        q = int(raw_in[1])
        r = int(raw_in[2])
        # ignore s if none was given
        if len(raw_in) == 4:
            s = int(raw_in[3])
        else:
            s = None
        # return values in standard sequence
        return d, q, r, s

    def _isGameOver(self):
        for player in self.players:
            if player.victoryPoints >= self.victoryPoints:
                return True

        return False

    # TODO: move this somewhere else
    # TODO: deal with gold
    _resFromHex = {HexType.MOUNTAIN: Resource.ROCK,
                   HexType.FIELD: Resource.WHEAT,
                   HexType.GRASS: Resource.SHEEP,
                   HexType.FOREST: Resource.LOG,
                   HexType.CLAY: Resource.BRICK}
    def getResourceFromHexType(self, htype):
        return self._resFromHex[htype]

    def _generateResources(self, redDice, yellowDice):
        # redDice, yellowDice can be used for cities & knights  if we want
        number = redDice + yellowDice

        for h in self.board.hexset:
            if self.board.getNumber(h) == number:
                htype = self.board.getHexType()
                res = self.getResourceFromHexType(htype)
                for v in h.corners():
                    b = self.board.getBuilding(v)
                    if isinstance(b, building.Colony):
                        resources = {res: b.resourcesGenerated()}
                        b.owner().giveResources(resources)


    def _nextTurn(self, player):
        turnOver = False
        # TODO: request to play knight/fish to remove the robber before rolling
        red, yellow = self._rollDice()
        self._generateResources(red, yellow)
        while not turnOver:
            # TODO: allow current player to build
            # TODO: allow current player to trade with others
            # TODO: allow current player to play development cards
            # TODO: allow current player to end turn
            turnOver = True  # this is basically "pass"


    def playGame(self):
        self.placeStartBuildings()
        curPlayer = 0
        while not self._isGameOver():
            self._nextTurn(self.players[curPlayer])
            curPlayer = (curPlayer + 1) % len(self.players)

        print("Game over!")


if __name__ == "__main__":
    g = Game()
    g.playGame()
