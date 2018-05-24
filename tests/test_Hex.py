# Test Hex class in coordinates module
import pytest
import context
from unitedcatan.coordinates import *

# Test that Hex initialization succeeds with valid input
def test_Hex_init_succeeds():
    # Arrange
    inputs = [(0, 0, 0),
              (1, 0, -1),
              (-17, 14, 3),
              (0, 0),
              (2, 3)]
    
    # Act
    outputs = [Hex(*input_tuple) for input_tuple in inputs]
    
# Test that Hex initialization fails with invalid input
def test_Hex_init_fails():
    # Arrange
    inputs_0 = [(0, (0,0), 0),
                (0, "hi", 0),
                ("yo", 0, 0),
                (0, 0, "suh")]
    inputs_1 = [(0, 0, 1),
                (1, 2, 3),
                (-1, -3, 5)]
    
    # Act
    for invalid_input in inputs_0:
        with pytest.raises(TypeError) as e:
            output = Hex(*invalid_input)
    
    for invalid_input in inputs_1:
        with pytest.raises(ValueError) as e:
            output = Hex(*invalid_input)

def test_Hex_eq_hash():
    # Arrange
    inputs_0 = [Hex(0, 0, 0), Hex(0, 0, None)]
    inputs_1 = [Hex(-1, 2, -1), Hex(-1, 2)]
    inputs_2 = [Hex(0, 0), Hex(1, 0)]
    inputs_3 = [Hex(1, -2, 1), Hex(-1, 2, -1)]
    
    # Act
    outputs_eq_0 = inputs_0[0] == inputs_0[1]
    outputs_hash_0 = hash(inputs_0[0]) == hash(inputs_0[1])
    outputs_eq_1 = inputs_1[0] == inputs_1[1]
    outputs_hash_1 = hash(inputs_1[0]) == hash(inputs_1[1])
    
    outputs_eq_2 = inputs_2[0] != inputs_2[1]
    outputs_eq_3 = inputs_3[0] != inputs_3[1]
    
    # Assert
    assert( outputs_eq_0 )
    assert( outputs_hash_0 )
    assert( outputs_eq_1 )
    assert( outputs_hash_1 )
    assert( outputs_eq_2 )
    assert( outputs_eq_3 )
    
def test_Hex_arithmetic():
    pass

### NEIGHBOURS ###

def test_Hex_neighbours():
    pass

def test_Hex_neighbour():
    pass

def test_Hex_is_neighbour():
    pass
    
### BORDERS ###

def test_Hex_borders():
    pass
    
def test_Hex_border():
    pass

def test_Hex_is_border():
    pass

### CORNERS ###

def test_Hex_corners():
    pass

def test_Hex_corner():
    pass

def test_Hex_is_corner():
    pass
