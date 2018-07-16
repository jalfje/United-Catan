from coordinates import Direction, Hex, Edge, Vertex
from player import Player
from resource import Resource
import building
from board import Board

class Game(object):

    # these are useless at present, but once we have a GUI they could be
    _colours = ["RED", "BLUE", "WHITE", "ORANGE", "YELLOW", "PINK"]

    def __init__(self, num_players=2):
        self.board = Board()
        # initialize player objects
        self.players = []
        for p in range(0, num_players):
            name = "Player " + str(p+1)
            colour = Game._colours[p % len(Game._colours)]
            player = Player(p, name, colour)
            self.players.append(player)
        # victory points required for victory
        self.victory_points = 10
        self.turn_index = 0

    # TODO: change name, refactor. this is VERY preliminary
    # TODO: Board.can_place(Player, Building, Location, is_setup) for all building varieties
    def place_start_buildings(self):
        # place first set of settlement/road pairs, in order of play
        for player in self.players:
            # get player to place a settlement
            valid_settlement = False
            while not valid_settlement:
                ask_str = player.name + ", where will you place your first settlement?"
                vertex = self.get_input_vertex(ask_str)
                valid_settlement = self.board.can_place(player, building.Settlement, vertex, is_setup=True)
                if not valid_settlement:
                    print("You can't place your settlement there.")
            # get player to place a road
            valid_road = False
            while not valid_road:
                ask_str = player.name + ", where will you place your first road?"
                edge = self.get_input_edge(ask_str)
                valid_loc = self.board.can_place(player, building.Road, edge, is_setup=True)
                valid_road = valid_loc and vertex.is_protruding(edge)
                if not valid_road:
                    print("You can't place your road there.")

        # place second set of settlement/road pairs, in reverse order of play
        for player in reversed(self.players):
            # get player to place a settlement
            valid_settlement = False
            while not valid_settlement:
                ask_str = player.name + ", where will you place your second settlement?"
                vertex = self.get_input_vertex(ask_str)
                valid_settlement = self.board.can_place(player, building.Settlement, vertex, is_setup=True)
                if not valid_settlement:
                    print("You can't place your settlement there.")
            # get player to place a road
            valid_road = False
            while not valid_road:
                ask_str = player.name + ", where will you place your second road?"
                edge = self.get_input_edge(ask_str)
                valid_loc = self.board.can_place(player, building.Road, edge, is_setup=True)
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
            except:
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

if __name__ == "__main__":
    g = Game()
    g.place_start_buildings()
