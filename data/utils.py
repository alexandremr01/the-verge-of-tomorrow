"""
Functions that are generic and therefore useful
in many classes
"""

def is_in_rect(rect, pos):
    """
    Determines if tuple pos is inside pygame rect
    """
    if rect.left < pos[0] < rect.left + rect.width:
        if rect.top < pos[1] < rect.top + rect.height:
            return True
    return False
