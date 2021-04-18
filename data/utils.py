"""
Functions that are generic and therefore useful
in many classes
"""
import numpy as np
import random
import math

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


def get_grid_positions(center_position, initial_vector=np.array([1, 0]), step=-1):
    vectors = [np.array([1, 0]), np.array([1, 1]), np.array([0, 1]), np.array([-1, 1]),
               np.array([-1, 0]), np.array([-1, -1]), np.array([0, -1]), np.array([1, -1])]
    if step == -1:
        return [center_position] + [center_position + vector for vector in vectors]
    initial = 0
    for i in range(8):
        if np.all(vectors[i] == initial_vector):
            initial = i
            break
    selected = []
    if initial - step < 0:
        selected = vectors[initial - step:] + vectors[0: initial + step + 1]
    elif initial + step >= len(vectors):
        selected = vectors[initial - step:] + vectors[: (initial + step) % len(vectors) + 1]
    else:
        selected = vectors[initial - step: initial + step + 1]
    return [tuple(center_position + vector) for vector in selected]


def compare(noise_value, starting_value, interval_percentage, slices, percentages):
    carry = starting_value
    for s in enumerate(slices):
        if 0 <= noise_value - carry < percentages[s[0]] * interval_percentage:
            return s[1]
        carry += percentages[s[0]] * interval_percentage

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    angle = np.radians(angle)

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

class RandomEventGenerator:
    """
    Receive a dictionary in the form {"event1": prob1, "event2": prob2, ...} and returns one event based on a
    random generator. Null event is the one triggered if no other is. Raise exception if sum(prob_i) > 1
    """

    def __init__(self, event_prob_dict, null_event):
        self._validate(event_prob_dict)
        self.event_prob_dict = event_prob_dict
        self.null_event = null_event

    def generate(self, seed=None):
        np.random.seed(seed)
        r = np.random.uniform()
        accum = 0
        for event, prob in self.event_prob_dict.items():
            accum += prob
            if r < accum:
                return event
        return self.null_event

    def _validate(self, event_prob_dict):
        total_prob = 0
        for event, prob in event_prob_dict.items():
            total_prob += prob
        if total_prob > 1.0:
            raise Exception("RandomEventGenerator invalid probabilities: sum(p_i)>1")

