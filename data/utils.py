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
