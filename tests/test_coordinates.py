import pytest
import context
from unitedcatan.coordinates import *

# Arrange, Act, Assert
# in this case, asserts are almost entirely implicit - if an exception is
# thrown, the test has failed. else the test has passed.

# Test that verify_coords succeeds with valid input
def test_verify_coords_succeeds():
    # Arrange
    q0, r0, s0 = 0, 0, 0
    q1, r1, s1 = 3, -6, 3
    q2, r2, s2 = 12313, 13255, None
    
    # Act
    verify_coords(q0, r0, s0)
    verify_coords(q1, r1, s1)
    verify_coords(q2, r2, s2)

# Test that verify_coords fails with invalid input
def test_verify_coords_fails():
    # Arrange
    q0, r0, s0 = "hello", 0, 0
    q1, r1, s1 = 0, None, 0
    q2, r2, s2 = 0, 0, 3.14
    q3, r3, s3 = 0, 0, 1
    
    # Act
    with pytest.raises(TypeError) as e:
        verify_coords(q0, r0, s0)
    with pytest.raises(TypeError) as e:
        verify_coords(q1, r1, s1)
    with pytest.raises(TypeError) as e:
        verify_coords(q2, r2, s2)
    with pytest.raises(ValueError) as e:
        verify_coords(q3, r3, s3)

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
    
    # Act
    with pytest.raises(DirectionError) as e:
        output_0 = Vertex(*input_0)
    with pytest.raises(DirectionError) as e:
        output_1 = Vertex(*input_1)
    with pytest.raises(ValueError) as e:
        output_2 = Vertex(*input_2)
    with pytest.raises(ValueError) as e:
        output_3 = Vertex(*input_3)
