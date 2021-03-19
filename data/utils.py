"""
Functions that are generic and therefore useful
in many classes
"""
import numpy as np

def is_in_rect(rect, pos):
    """
    Determines if tuple pos is inside pygame rect
    """
    if rect.left < pos[0] < rect.left + rect.width:
        if rect.top < pos[1] < rect.top + rect.height:
            return True
    return False


def distance(first_pos, second_pos):
    return np.sqrt(np.sum(np.power(np.array(second_pos) - np.array(first_pos), 2)))


def get_grid_positions(center_position, initial_vector, step=0):
    vectors = [np.array([1, 0]), np.array([1, 1]), np.array([0, 1]), np.array([-1, 1]),
               np.array([-1, 0]), np.array([-1, -1]), np.array([0, -1]), np.array([1, -1])]
    initial = 0
    for i in range(8):
        if np.all(vectors[i] == initial_vector):
            initial = i
            break
    selected = []
    if initial - step < 0:
        selected = vectors[initial - step:] + vectors[0: initial + step + 1]
    else:
        selected = vectors[initial - step: initial + step + 1]
    return [tuple(center_position + vector) for vector in selected]

