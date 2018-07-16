from enum import Enum
from enum import auto

# assuming flat-topped hexagons
# https://www.redblobgames.com/grids/hexagons/#coordinates
# http://www-cs-students.stanford.edu/~amitp/game-programming/grids/

# TODO: refactor into different files/modules/whatever


# error for invalid direction, with input for what the allowed directions are
class DirectionError(ValueError):

    def __init__(self, allowed_directions):
        direction_names = [d.name for d in allowed_directions]
        ValueError.__init__(self, "direction invalid, must be "
                                  + " or ".join(direction_names))


class Direction(Enum):
    W = 1
    NW = 2
    N = 3
    NE = 4
    E = 5
    SE = 6
    S = 7
    SW = 8

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __lt__(self, other):
        return self.value < other.value


# function for verifying that coords are integers that sum to 0
def verify_coords(q, r, s):

    if not isinstance(q, int):
        raise TypeError("q must be integer type")
    if not isinstance(r, int):
        raise TypeError("r must be integer type")
    # generate third dimension if none provided
    if s is None:
        s = -q - r
    elif not isinstance(s, int):
        raise TypeError("s must be integer type")
    # now verify valid cube coordinate
    if not (q + r + s == 0):
        raise ValueError("q + r + s must equal 0")


# Base class for objects which are completely representable by a tuple.
# Includes overrides for __eq__, __hash__, __str__, and __repr__.
class Tupleable(object):

    # raise error if the object cannot be iterated, i.e. converted to a tuple
    def __iter__(self):
        raise InterfaceError(self)

    # objects are equal if their tuples are equal
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return tuple(self) == tuple(other)

    # hash a tuple of the object
    def __hash__(self):
        return hash(tuple(self))

    # get the string representation of this object
    def __str__(self):
        return self.__class__.__name__ + str(tuple(self))

    # get the string representation of this object
    def __repr__(self):
        return self.__class__.__name__ + str(tuple(self))

    def __lt__(self, other):
        return tuple(self) < tuple(other)


class Vertex(Tupleable):

    _allowed_directions = [Direction.W, Direction.E]

    # Initialize a Vertex object with a location and direction
    def __init__(self, direction, q, r, s=None):
        verify_coords(q, r, s)
        # adjust so that internally we only have W or E vertexes
        if direction == Direction.NW:
            direction = Direction.E
            q = q-1
            r = r
        elif direction == Direction.NE:
            direction = Direction.W
            q = q+1
            r = r-1
        elif direction == Direction.SW:
            direction = Direction.E
            q = q-1
            r = r+1
        elif direction == Direction.SE:
            direction = Direction.W
            q = q+1
            r = r
        # confirm that direction is valid
        if direction not in Vertex._allowed_directions:
            raise DirectionError(Vertex._allowed_directions)
        # store variables
        self._d = direction
        self._q = q
        self._r = r

    # direction
    def d(self):
        return self._d

    # q-coordinate
    def q(self):
        return self._q

    # r-coordinate
    def r(self):
        return self._r

    # s-coordinate
    def s(self):
        return -self._q - self._r

    # for creating tuples etc
    def __iter__(self):
        yield self.d()
        yield self.q()
        yield self.r()
        yield self.s()

    # get hexes that this vertex is a corner of
    def touches(self):
        assert(self.d() in Vertex._allowed_directions)
        if self.d() == Direction.W:
            return [Hex(self.q(), self.r()),
                    Hex(self.q()-1, self.r()+1),
                    Hex(self.q()-1, self.r())]
        if self.d() == Direction.E:
            return [Hex(self.q(), self.r()),
                    Hex(self.q()+1, self.r()-1),
                    Hex(self.q()+1, self.r())]


    def is_touching(self, hex_):
        return hex_ in self.touches()

    # get edges that this vertex is an endpoint of
    def protrudes(self):
        assert(self.d() in Vertex._allowed_directions)
        if self.d() == Direction.W:
            return [Edge(Direction.SW, self.q(), self.r()),
                    Edge(Direction.S, self.q()-1, self.r()),
                    Edge(Direction.NW, self.q(), self.r())]
        if self.d() == Direction.E:
            return [Edge(Direction.NE, self.q(), self.r()),
                    Edge(Direction.N, self.q()+1, self.r()),
                    Edge(Direction.SE, self.q(), self.r())]


    def is_protruding(self, edge):
        return edge in self.protrudes()

    # get vertexes that are one edge away from this vertex
    def adjacents(self):
        assert(self.d() in Vertex._allowed_directions)
        if self.d() == Direction.W:
            return [Vertex(Direction.SW, self.q(), self.r()),
                    Vertex(Direction.SW, self.q()-1, self.r()),
                    Vertex(Direction.NW, self.q(), self.r())]
        if self.d() == Direction.E:
            return [Vertex(Direction.NE, self.q(), self.r()),
                    Vertex(Direction.NE, self.q()+1, self.r()),
                    Vertex(Direction.SE, self.q(), self.r())]


    def is_adjacent(self, vertex):
        return vertex in self.adjacents()


class Edge(Tupleable):

    _allowed_directions = [Direction.NW, Direction.N, Direction.NE]

    def __init__(self, direction, q, r, s=None):
        verify_coords(q, r, s)
        # adjust direction s.t. the edge is a top edge (NW, N, or NE)
        if direction == Direction.SW:
            direction = Direction.NE
            q = q-1
            r = r+1
        elif direction == Direction.S:
            direction = Direction.N
            q = q
            r = r+1
        elif direction == Direction.SE:
            direction = Direction.NW
            q = q+1
            r = r

        if direction not in Edge._allowed_directions:
            raise DirectionError(Edge._allowed_directions)

        self._d = direction
        self._q = q
        self._r = r

    # direction
    def d(self):
        return self._d

    # q-coordinate
    def q(self):
        return self._q

    # r-coordinate
    def r(self):
        return self._r

    # s-coordinate
    def s(self):
        return -self._q - self._r

    # for creating tuples etc
    def __iter__(self):
        yield self.d()
        yield self.q()
        yield self.r()
        yield self.s()

    # get hexes that this edge is a border of
    def joins(self):
        assert(self.d() in Edge._allowed_directions)
        if self.d() == Direction.NW:
            return [Hex(self.q(), self.r()),
                    Hex(self.q()-1, self.r())]
        if self.d() == Direction.N:
            return [Hex(self.q(), self.r()),
                    Hex(self.q(), self.r()-1)]
        if self.d() == Direction.NE:
            return [Hex(self.q(), self.r()),
                    Hex(self.q()+1, self.r()-1)]


    def is_joining(self, hex_):
        return hex_ in self.joins()

    # get edges that continue from this edge
    def continues(self):
        assert(self.d() in Edge._allowed_directions)
        if self.d() == Direction.NW:
            return [Edge(Direction.SW, self.q(), self.r()),
                    Edge(Direction.S, self.q()-1, self.r()),
                    Edge(Direction.NE, self.q()-1, self.r()),
                    Edge(Direction.N, self.q(), self.r())]
        if self.d() == Direction.N:
            return [Edge(Direction.NW, self.q(), self.r()),
                    Edge(Direction.SW, self.q(), self.r()-1),
                    Edge(Direction.SE, self.q(), self.r()-1),
                    Edge(Direction.NE, self.q(), self.r())]
        if self.d() == Direction.NE:
            return [Edge(Direction.N, self.q(), self.r()),
                    Edge(Direction.NW, self.q()+1, self.r()-1),
                    Edge(Direction.S, self.q()+1, self.r()-1),
                    Edge(Direction.SE, self.q(), self.r())]


    def is_continuing(self, edge):
        return edge in self.continues()

    # get vertexes that are endpoints of this edge
    def endpoints(self):
        assert(self.d() in Edge._allowed_directions)
        if self.d() == Direction.NW:
            return [Vertex(Direction.W, self.q(), self.r()),
                    Vertex(Direction.NW, self.q(), self.r())]
        if self.d() == Direction.N:
            return [Vertex(Direction.NW, self.q(), self.r()),
                    Vertex(Direction.NE, self.q(), self.r())]
        if self.d() == Direction.NE:
            return [Vertex(Direction.NE, self.q(), self.r()),
                    Vertex(Direction.E, self.q(), self.r())]


    def is_endpoint(self, vertex):
        return vertex in self.endpoints()


class Hex(Tupleable):

    _corner_directions = [Direction.W, Direction.NW, Direction.NE,
                           Direction.E, Direction.SE, Direction.SW]
    _border_directions = [Direction.NW, Direction.N, Direction.NE,
                           Direction.SW, Direction.S, Direction.SE]
    _neighbour_directions = _border_directions

    def __init__(self, q, r, s=None):
        # validate that coordinates sum to 0
        verify_coords(q, r, s)
        self._q = q
        self._r = r

    # accessors
    def q(self):
        return self._q

    def r(self):
        return self._r

    def s(self):
        return -self._q - self._r

    # for creating tuples etc
    def __iter__(self):
        yield self.q()
        yield self.r()
        yield self.s()

    # set of neighbour hexes, in clockwise order: NW, N, NE, SE, S, SW
    def neighbours(self):
        return [self.neighbour(d) for d in Hex._neighbour_directions]

    # check if a hex is a neighbour hex of this hex
    def is_neighbour(self, hex_):
        return hex_ in self.neighbours()

    # get neighbour hex by direction relative to this hex
    def neighbour(self, direction):
        if direction == Direction.NW:
            return Hex(self.q() - 1, self.r() + 1)
        if direction == Direction.N:
            return Hex(self.q(),     self.r() - 1)
        if direction == Direction.NE:
            return Hex(self.q() + 1, self.r() - 1)
        if direction == Direction.SE:
            return Hex(self.q() + 1, self.r())
        if direction == Direction.S:
            return Hex(self.q(),     self.r() + 1)
        if direction == Direction.SW:
            return Hex(self.q() - 1, self.r())
        raise DirectionError(Hex._neighbour_directions)

    # set of border edges, in clockwise order: NW, N, NE, SE, S, SW
    def borders(self):
        return [self.border(d) for d in Hex._border_directions]

    # check if an edge is a border edge of this hex
    def is_border(self, edge):
        return edge in self.borders()

    # get border edge by direction relative to this hex
    def border(self, direction):
        if direction in Hex._border_directions:
            return Edge(direction, self.q(), self.r())
        raise DirectionError(Hex._border_directions)

    # set of corner vertices, in clockwise order: W, NW, NE, E, SE, SW
    def corners(self):
        return [self.corner(d) for d in Hex._corner_directions]

    # check if a vertex is a corner vertex of this hex
    def is_corner(self, vertex):
        return vertex in self.corners()

    # get corner vertex by direction relative to this hex
    def corner(self, direction):
        if direction in Hex._corner_directions:
            return Vertex(direction, self.q(), self.r())
        raise DirectionError(Hex._corner_directions)

    # get distance between this and another hex coordinate
    def dist(self, other):
        # largest absolute value in the difference is the distance.
        return max([abs(c) for c in tuple(self - other)])

    # Overloaded operators #

    # get positive copy of this hex coordinate
    def __pos__(self):
        return Hex(self.q(), self.r())

    # get negative copy of this hex coordinate
    def __neg__(self):
        return Hex(-self.q(), -self.r())

    # get two hex coordinates added together
    def __add__(self, other):
        qtot = self.q() + other.q()
        rtot = self.r() + other.r()
        return Hex(qtot, rtot)

    # get difference of two hex coordinates
    def __sub__(self, other):
        return self + -other
