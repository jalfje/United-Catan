# Test Vertex class in coordinates module
import pytest
import context
from unitedcatan.coordinates import *

# Test that Vertex initialization succeeds with valid input
def test_Vertex_init_succeeds():
    # Arrange
    input_0 = (Direction.W, 0, 0, 0)
    input_1 = (Direction.E, 1, 0, -1)
    input_2 = (Direction.W, 1, 0, None)
    input_3 = (Direction.E, 1, 0)
    input_4 = (Direction.NW, 0, 0, 0)
    
    expected_0_q = 0
    expected_0_tuple = input_0
    expected_1_r = 0
    expected_2_s = -1
    expected_3_s = -1
    expected_4_d = Direction.E
    expected_4_q = -1
    
    # Act
    output_0 = Vertex(*input_0)
    output_1 = Vertex(*input_1)
    output_2 = Vertex(*input_2)
    output_3 = Vertex(*input_3)
    output_4 = Vertex(*input_4)
    
    # Assert
    assert( expected_0_q == output_0.q() )
    assert( expected_0_tuple == tuple(output_0) )
    assert( expected_1_r == output_1.r() )
    assert( expected_2_s == output_2.s() )
    assert( expected_3_s == output_3.s() )
    assert( expected_4_d == output_4.d() )
    assert( expected_4_q == output_4.q() )
    
# Test that Vertex initialization fails with invalid input
def test_Vertex_init_fails():
    # Arrange
    input_0 = (Direction.N, 0, 0, 0)
    input_1 = (Direction.S, 0, 0, 0)
    input_2 = (Direction.W, 1, 1, 1)
    input_3 = (Direction.E, -1, 0, 2)
    input_4 = (Direction.W, 1, 2, "hi")
    
    # Act
    with pytest.raises(DirectionError) as e:
        output_0 = Vertex(*input_0)
    with pytest.raises(DirectionError) as e:
        output_1 = Vertex(*input_1)
    with pytest.raises(ValueError) as e:
        output_2 = Vertex(*input_2)
    with pytest.raises(ValueError) as e:
        output_3 = Vertex(*input_3)
    with pytest.raises(TypeError) as e:
        output_4 = Vertex(*input_4)

# Test Vertex objects are equal to eachother exactly when they should be
# Also test that equal Vertex objects have equal hash values
def test_Vertex_eq_hash():
    # Arrange
    input_0a = Vertex(Direction.W, 0, 0)
    input_0b = Vertex(Direction.W, 0, 0)
    input_1a = Vertex(Direction.E, 0, 0)
    input_1b = Vertex(Direction.SW, 1, -1)
    input_1c = Vertex(Direction.NW, 1, 0)
    input_2a = Vertex(Direction.W, 0, 0)
    input_2b = Vertex(Direction.W, 1, 0)
    
    # Act
    output_0_eq = (input_0a == input_0b)
    output_0_hash = (hash(input_0a) == hash(input_0b))
    output_1_eq = (input_1a == input_1b == input_1c)
    output_1_hash = (hash(input_1a) == hash(input_1b) == hash(input_1c))
    output_2_eq = (input_2a != input_2b)
    # no test that hashes are different, because they don't need to be
    
    # Assert
    assert( output_0_eq )
    assert( output_0_hash )
    assert( output_1_eq )
    assert( output_1_hash )
    assert( output_2_eq )

# Test Vertex.touches()
def test_Vertex_touches():
    # Arrange
    input_0 = Vertex(Direction.W, 0, 0)
    input_1 = Vertex(Direction.E, 0, 0)
    
    expected_len = 3
    expected_0_Hex_0 = Hex(0, 0)
    expected_1_Hex_0 = Hex(0, 0)
    
    # Act
    output_0 = input_0.touches()
    output_1 = input_1.touches()
    
    # Assert
    assert( expected_len == len(output_0) )
    assert( expected_0_Hex_0 in output_0 )
    assert( expected_len == len(output_1) )
    assert( expected_1_Hex_0 in output_1 )

# Test Vertex.protrudes()
def test_Vertex_protrudes():
    # Arrange
    input_0 = Vertex(Direction.W, 0, 0)
    input_1 = Vertex(Direction.E, 0, 0)
    
    expected_len = 3
    expected_0_Edges = [Edge(Direction.N, -1, 1),
                        Edge(Direction.NW, 0, 0),
                        Edge(Direction.SW, 0, 0)]
    expected_1_Edges = [Edge(Direction.S, 1, -1),
                        Edge(Direction.NE, 0, 0),
                        Edge(Direction.SE, 0, 0)]
    
    # Act
    output_0 = input_0.protrudes()
    output_1 = input_1.protrudes()
    
    # Assert
    assert( expected_len == len(output_0) )
    assert( all(e in output_0 for e in expected_0_Edges) )
    assert( expected_len == len(output_1) )
    assert( all(e in output_1 for e in expected_1_Edges) )

# Test Vertex.adjacents()
def test_Vertex_adjacents():
    # Arrange
    input_0 = Vertex(Direction.W, 0, 0)
    input_1 = Vertex(Direction.E, 0, 0)
    
    expected_len = 3
    expected_0_Vertexes = [Vertex(Direction.NW, -1, 1),
                           Vertex(Direction.NW, 0, 0),
                           Vertex(Direction.SW, 0, 0)]
    expected_1_Vertexes = [Vertex(Direction.SE, 1, -1),
                           Vertex(Direction.NE, 0, 0),
                           Vertex(Direction.SE, 0, 0)]
    
    # Act
    output_0 = input_0.adjacents()
    output_1 = input_1.adjacents()
    
    # Assert
    assert( expected_len == len(output_0) )
    assert( all(v in output_0 for v in expected_0_Vertexes) )
    
    assert( expected_len == len(output_1) )
    assert( all(v in output_1 for v in expected_1_Vertexes) )
