# Test coordinates module
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
