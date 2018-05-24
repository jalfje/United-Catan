# Test Edge class in coordinates module
import pytest
import context
from unitedcatan.coordinates import *

# Test that Edge initialization succeeds with valid input
def test_Edge_init_succeeds():
    # Arrange
    input_0 = (Direction.NW, 0, 0, 0)
    input_1 = (Direction.N, 1, 0, -1)
    input_2 = (Direction.NE, 0, 2, None)
    input_3 = (Direction.SE, -1, 0)
    input_4 = (Direction.S, 0, 0, 0)
    input_5 = (Direction.SW, 0, 0, 0)
    
    expected_0_tuple = input_0
    expected_1_q = 1
    expected_2_s = -2
    expected_3_tuple = (Direction.NW, 0, 0, 0)
    expected_4_tuple = (Direction.N, 0, 1, -1)
    expected_5_tuple = (Direction.NE, -1, 1, 0)
    
    # Act
    output_0 = Edge(*input_0)
    output_1 = Edge(*input_1)
    output_2 = Edge(*input_2)
    output_3 = Edge(*input_3)
    output_4 = Edge(*input_4)
    output_5 = Edge(*input_5)
    
    # Assert
    assert( expected_0_tuple == tuple(output_0) )
    assert( expected_1_q == output_1.q() )
    assert( expected_2_s == output_2.s() )
    assert( expected_3_tuple == tuple(output_3) )
    assert( expected_4_tuple == tuple(output_4) )
    assert( expected_5_tuple == tuple(output_5) )
    
    
# Test that Edge initialization fails with invalid input
def test_Edge_init_fails():
    # Arrange
    input_0 = (Direction.W, 0, 0, 0)
    input_1 = (Direction.E, 0, 0, 0)
    input_2 = (Direction.N, 1, 1, 0)
    input_3 = (Direction.S, 1, 0, 1)
    input_4 = (Direction.N, 1, 2, "hi")
    
    # Act
    with pytest.raises(DirectionError) as e:
        output_0 = Edge(*input_0)
    with pytest.raises(DirectionError) as e:
        output_1 = Edge(*input_1)
    with pytest.raises(ValueError) as e:
        output_2 = Edge(*input_2)
    with pytest.raises(ValueError) as e:
        output_3 = Edge(*input_3)
    with pytest.raises(TypeError) as e:
        output_4 = Edge(*input_4)

    
# Test Edge objects are equal to eachother exactly when they should be
# Also test that equal Edge objects have equal hash values
def test_Vertex_eq_hash():
    # Arrange
    input_0a = Edge(Direction.NW, 0, 0)
    input_0b = Edge(Direction.NW, 0, 0)
    input_1a = Edge(Direction.N, 0, 0)
    input_1b = Edge(Direction.S, 0, -1)
    input_2a = Edge(Direction.N, 0, 0)
    input_2b = Edge(Direction.NW, 0, 0)
    
    # Act
    output_0_eq = (input_0a == input_0b)
    output_0_hash = (hash(input_0a) == hash(input_0b))
    output_1_eq = (input_1a == input_1b)
    output_1_hash = (hash(input_1a) == hash(input_1b))
    output_2_eq = (input_2a != input_2b)
    # no test that hashes are different, because they don't need to be
    
    # Assert
    assert( output_0_eq )
    assert( output_0_hash )
    assert( output_1_eq )
    assert( output_1_hash )
    assert( output_2_eq )
        
# Test Edge.joins()
def test_Edge_joins():
    # Arrange
    input_0 = Edge(Direction.NW, 0, 0)
    
    expected_len = 2
    expected_0_Hexes = [Hex(0, 0),
                        Hex(-1, 0)]
                        
    
    # Act
    output_0 = input_0.joins()
    
    # Assert
    assert( expected_len == len(output_0) )
    assert( all(h in output_0 for h in expected_0_Hexes) )


# Test Edge.continues()
def test_Edge_continues():
    # Arrange
    input_0 = Edge(Direction.N, 0, 0)
    
    expected_len = 4
    expected_0_Edges = [Edge(Direction.NW, 0, 0),
                        Edge(Direction.NE, 0, 0),
                        Edge(Direction.SW, 0, -1),
                        Edge(Direction.SE, 0, -1)]
    
    # Act
    output_0 = input_0.continues()
    
    # Assert
    assert( expected_len == len(output_0) )
    assert( all(e in output_0 for e in expected_0_Edges) )
    
# Test Edge.endpoints()
def test_Edge_endpoints():
    # Arrange
    input_0 = Edge(Direction.N, 0, 0)
    
    expected_len = 2
    expected_0_Vertices = [Vertex(Direction.NW, 0, 0),
                           Vertex(Direction.NE, 0, 0)]
                           
    # Act
    output_0 = input_0.endpoints()
    
    # Assert
    assert( expected_len == len(output_0) )
    assert( all(v in output_0 for v in expected_0_Vertices) )
