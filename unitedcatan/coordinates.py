from enum import Enum
from enum import auto

# assuming flat-topped hexagons
# https://www.redblobgames.com/grids/hexagons/#coordinates
# http://www-cs-students.stanford.edu/~amitp/game-programming/grids/

#TODO: refactor into different files/modules/whatever

# error for invalid direction, with input for what the allowed directions are
class DirectionError(ValueError):
    def __init__(self, allowed_directions):
        ValueError.__init__(self, "direction invalid, must be " + " or ".join([d.name for d in allowed_directions]))

class Direction(Enum):
    W = auto()
    NW = auto()
    N = auto()
    NE = auto()
    E = auto()
    SE = auto()
    S = auto()
    SW = auto()
    
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

class Vertex(object):
    __allowed_directions = [Direction.W, Direction.E]
    
    # Initialize a Vertex object with a location and direction
    def __init__(self, direction, q, r, s = None):
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
        if direction not in Vertex.__allowed_directions:
            raise DirectionError(Vertex.__allowed_directions)
        # store variables
        self.__d = direction
        self.__q = q
        self.__r = r
    
    # accessors
    def d(self):
        return self.__d
    def q(self):
        return self.__q
    def r(self):
        return self.__r
    def s(self):
        return -self.__q - self.__r
    # for creating tuples etc
    def __iter__(self):
        yield self.d()
        yield self.q()
        yield self.r()
        yield self.s()
        
    # get hexes that this vertex is a corner of
    def touches(self):
        if self.d() == Direction.W:
            return [Hex(self.q(), self.r()),
                    Hex(self.q()-1, self.r()+1),
                    Hex(self.q()-1, self.r())]
        if self.d() == Direction.E:
            return [Hex(self.q(), self.r()),
                    Hex(self.q()+1, self.r()-1),
                    Hex(self.q()+1, self.r())]
        raise DirectionError(Vertex.__allowed_directions)
    
    # get edges that this vertex is an endpoint of
    def protrudes(self):
        if self.d() == Direction.W:
            return [Edge(Direction.SW, self.q(), self.r()),
                    Edge(Direction.S, self.q()-1, self.r()),
                    Edge(Direction.NW, self.q(), self.r())]
        if self.d() == Direction.E:
            return [Edge(Direction.NE, self.q(), self.r()),
                    Edge(Direction.N, self.q()+1, self.r()),
                    Edge(Direction.SE, self.q(), self.r())]
        raise DirectionError(Vertex.__allowed_directions)
            
    # get vertexes that are one edge away from this vertex
    def adjacents(self):
        if self.d() == Direction.W:
            return [Vertex(Direction.SW, self.q(), self.r()),
                    Vertex(Direction.SW, self.q()-1, self.r()),
                    Vertex(Direction.NW, self.q(), self.r())]
        if self.d() == Direction.E:
            return [Vertex(Direction.NE, self.q(), self.r()),
                    Vertex(Direction.NE, self.q()+1, self.r()),
                    Vertex(Direction.SE, self.q(), self.r())]
        raise DirectionError(Vertex.__allowed_directions)
    
    ##### Overloaded operators #####
    
    # Hex objects are equal if their coordinates are equal
    def __equ__(self, other):
        if not isinstance(other, Vertex):
            return False
        else:
            return tuple(self) == tuple(other)
    # hash a tuple of coordinates
    def __hash__(self):
        return hash(tuple(self))
    

class Edge(object):
    __allowed_directions = [Direction.NW, Direction.N, Direction.NE]
    
    def __init__(self, direction, q, r, s = None):
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
        
        if direction not in Edge.__allowed_directions:
            raise DirectionError(Edge.__allowed_directions)
            
        self.__d = direction
        self.__q = q
        self.__r = r
    
    # accessors
    def d(self):
        return self.__d
    def q(self):
        return self.__q
    def r(self):
        return self.__r
    def s(self):
        return -self.__q - self.__r
    # for creating tuples etc
    def __iter__(self):
        yield self.d()
        yield self.q()
        yield self.r()
        yield self.s()
    
    # get hexes that this edge is a border of
    def joins(self):
        if self.d() == Direction.NW:
            return [Hex(self.q(), self.r()),
                    Hex(self.q()-1, self.r())]
        if self.d() == Direction.N:
            return [Hex(self.q(), self.r()),
                    Hex(self.q(), self.r()-1)]
        if self.d() == Direction.NE:
            return [Hex(self.q(), self.r()),
                    Hex(self.q()+1, self.r()-1)]
        raise DirectionError(Edge.__allowed_directions)
    
    # get edges that continue from this edge
    def continues(self):
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
        raise DirectionError(Edge.__allowed_directions)
        
    # get vertexes that are endpoints of this edge
    def endpoints(self):
        if self.d() == Direction.NW:
            return [Vertex(Direction.W, self.q(), self.r()),
                    Vertex(Direction.NW, self.q(), self.r())]
        if self.d() == Direction.N:
            return [Vertex(Direction.NW, self.q(), self.r()),
                    Vertex(Direction.NE, self.q(), self.r())]
        if self.d() == Direction.NE:
            return [Vertex(Direction.NE, self.q(), self.r()),
                    Vertex(Direction.E, self.q(), self.r())]
        raise DirectionError(Edge.__allowed_directions)
    
    ##### Overloaded operators #####
    
    # Hex objects are equal if their coordinates are equal
    def __equ__(self, other):
        if not isinstance(other, Vertex):
            return False
        else:
            return tuple(self) == tuple(other)
    # hash a tuple of coordinates
    def __hash__(self):
        return hash(tuple(self))
            

class Hex(object):
    __corner_directions = [Direction.W, Direction.NW, Direction.NE,
                           Direction.E, Direction.SE, Direction.SW]
    __border_directions = [Direction.NW, Direction.N, Direction.NE,
                           Direction.SW, Direction.S, Direction.SE]
    __neighbour_directions = __border_directions
    
    def __init__(self, q, r, s = None):
        # validate that coordinates sum to 0
        verify_coords(q, r, s)
        self.__q = q
        self.__r = r
    
    # accessors
    def q(self):
        return self.q
    def r(self):
        return self.r
    def s(self):
        return -self.q - self.r
    # for creating tuples etc
    def __iter__(self):
        yield self.q()
        yield self.r()
        yield self.s()
        
    # set of neighbour hexes, in clockwise order: NW, N, NE, SE, S, SW
    def neighbours(self):
        return [self.neighbour(d) for d in Hex.__neighbour_directions]
    def is_neighbour(self, other):
        return other in self.neighbours()
    # get neighbour hex by direction relative to this hex
    def neighbour(self, direction):
        n = self.neighbours()
        if direction == Direction.NW:
            return Hex(self.q() - 1, self.r() + 1)
        if direction == Direction.N:
            return Hex(self.q(),     self.r() - 1)
        if direction == Direction.NE:
            return Hex(self.q() + 1, self.r() - 1)
        if direction == Direction.SE:
            return Hex(self.q() + 1, self.r()    )
        if direction == Direction.S:
            return Hex(self.q(),     self.r() + 1)
        if direction == Direction.SW:
            return Hex(self.q() - 1, self.r()    )
        raise DirectionError(Hex.__neighbour_directions)
        
    # set of border edges, in clockwise order: NW, N, NE, SE, S, SW
    def borders(self):
        return [self.border(d) for d in Hex.__border_directions]
    def is_border(self, edge):
        return edge in self.borders()
    # get border edge by direction relative to this hex
    def border(self, direction):
        if direction in Hex.__border_directions:
            return Edge(direction, self.q(), self.r())
        else:
            raise DirectionError(Hex.__border_directions)
        
    
    # set of corner vertices, in clockwise order: W, NW, NE, E, SE, SW
    def corners(self):
        return [self.corner(d) for d in Hex.__corner_directions]
    def is_corner(self, vertex):
        return vertex in self.corners()
    # get corner vertex by direction relative to this hex
    def corner(self, direction):
        if direction in Hex.__corner_directions:
            return Vertex(direction, self.q(), self.r())
        else:
            raise DirectionError(Hex.__corner_directions)
        
                
    
    ##### Overloaded operators #####
    
    # Hex objects are equal if their coordinates are equal
    def __equ__(self, other):
        if not isinstance(other, Hex):
            return False
        else:
            return tuple(self) == tuple(other)
    # hash a tuple of coordinates
    def __hash__(self):
        return hash(tuple(self))
    
    # get positive/negative copies of this coordinate
    def __pos__(self):
        return Hex(self.q(), self.r())
    def __neg__(self):
        return Hex(-self.q(), -self.r())
    # get two coordinates added together
    def __add__(self, other):
        qtot = self.q() + other.q()
        rtot = self.r() + other.r()
        return Hex(qtot, rtot)
    # get difference of two coordinates
    def __sub__(self, other):
        return self + -other
        
    
