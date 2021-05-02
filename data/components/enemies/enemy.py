"""
Entity that is an enemy to the player,
programmed to stalk and hurt him
"""

from math import sin, cos, pi
import numpy as np
import pygame
from collections import deque
from ..base.entity import Entity
from ...constants import DEFAULT_ENEMY_VELOCITY, DEFAULT_ENEMY_HEALTH
from ...constants import DEFAULT_ENEMY_DAMAGE, FRAMES_TO_ENEMIES_TURN
from ...constants import FRAMES_PER_SECOND, PREDICTION_STEP, VALID_POS_SEARCH_STEP
from ...constants import TILE_SIZE, ATTRACTION_FACTOR, REPULSION_FACTOR
from ...constants import ENEMY_VISION_RANGE, VORTICE_FACTOR

class Enemy(Entity):
    """
    Abstraction of a stalker enemy
    """
    def __init__(self, position, sprite_graphic):
        super().__init__(position, sprite_graphic)
        self.health = DEFAULT_ENEMY_HEALTH
        self.velocity = DEFAULT_ENEMY_VELOCITY*FRAMES_TO_ENEMIES_TURN
        self.damage = DEFAULT_ENEMY_DAMAGE
        self.flying = False

        self.previous_pos = position
        self.curr_pos = position
        self.looking_angle = 0
        step = -VALID_POS_SEARCH_STEP*pi/180
        self.rot_mat = np.array([[cos(step), -sin(step)], [sin(step), cos(step)]])
        self.counter_rot_mat = np.array([[cos(-step), -sin(-step)], [sin(-step), cos(-step)]])
        self.nothing_detected = 0
        self.obstacles = []
        self.num_of_obstacles_in_line = 0
        self.rotational = -1

    def estimate_velocity(self):
        """
        Obtains an estimate of enemy velocity
        by finite differences
        """
        return (np.array(self.curr_pos) - np.array(self.previous_pos))*FRAMES_PER_SECOND/FRAMES_TO_ENEMIES_TURN

    def search_valid_direction(self, next_angle, valid_pos):
        """
        Searches a direction to move to
        """
        iteration = 0
        max_iterations = 360/VALID_POS_SEARCH_STEP
        while not valid_pos(self.curr_pos + next_angle*(self.sprite.get_width()/2 + PREDICTION_STEP)) and iteration < max_iterations:
            if self.rotational == -1:
                next_angle = self.counter_rot_mat.dot(next_angle)
            else:
                next_angle = self.rot_mat.dot(next_angle)

            iteration += 1

        return next_angle

    def search_obstacle(self, target, obstacle_pos):
        """
        Searches and returns the first obstacle encountered
        in the line between itself and the target
        """
        pos = self.get_position()

        self.num_of_obstacles_in_line = 0
        obstacles_in_line = []
        while np.linalg.norm(target - pos) > TILE_SIZE:
            pos = pos + (target - pos)/np.linalg.norm(target - pos)*TILE_SIZE
            if obstacle_pos(pos):
                obstacles_in_line.append(pos)
                self.num_of_obstacles_in_line += 1

        if self.num_of_obstacles_in_line > 0:
            return obstacles_in_line[0]
        else:
            return None

    def potential_fields_path_planning(self, target):
        """
        Given a target and obstacles between itself and the target,
        computes what its next angle should be based on the potential
        fields path planning
        """
        next_angle = np.zeros(2)

        vector_product_sign = 1
        if len(self.obstacles) > 0:
            center_mass = np.zeros(2)
            for obstacle in self.obstacles:
                center_mass += obstacle
            center_mass /= len(self.obstacles)

            center_to_me = self.get_position() - center_mass
            center_to_target = target - center_mass
            triangle_area = np.abs(np.cross(center_to_me, center_to_target))/2
            obstacle_disruptance = triangle_area/np.linalg.norm(self.get_position() - target)
            if obstacle_disruptance > 2*TILE_SIZE/3:
                if self.num_of_obstacles_in_line < 4:
                    vector_product_sign = np.sign(np.cross(center_to_me, center_to_target))
        self.rotational = vector_product_sign

        diff = target - self.get_position()
        next_angle += diff*ATTRACTION_FACTOR/(diff[0]**2 + diff[1]**2)
        for obstacle in self.obstacles:
            next_angle += self.obstacle_vortex(obstacle, -vector_product_sign)

        return next_angle/np.linalg.norm(next_angle)

    def obstacle_repulsion(self, obstacle):
        """
        Computes the obstacle as a source in the
        potential fields path planning
        """
        diff = self.get_position() - obstacle
        return diff*REPULSION_FACTOR/(diff[0]**2 + diff[1]**2)

    def obstacle_vortex(self, obstacle, sign):
        """
        Computes the obstacle as a vortex in the
        potential fields path planning
        """
        if sign == 0:
            return 0
        diff = self.get_position() - obstacle
        diff[0], diff[1] = sign*diff[1], -sign*diff[0]
        return diff*VORTICE_FACTOR/(diff[0]**2 + diff[1]**2)

    def enemy_bfs(self, root, validate_func):
        """
        Searches breadth first for other obstacles
        that start with root, at maximum 10
        """
        possible_dirs = [np.array([TILE_SIZE, 0]), np.array([0, TILE_SIZE]), np.array([0, -TILE_SIZE]), np.array([-TILE_SIZE, 0])]
        self.obstacles = []

        q = deque()
        q.append((root, None))
        while len(q) > 0 and len(self.obstacles) < ENEMY_VISION_RANGE:
            front = q.popleft()
            self.obstacles.append(front[0])
            for i in range(len(possible_dirs)):
                if not np.all(front[1] == possible_dirs[i]) and validate_func(front[0] + possible_dirs[i]):
                    q.append((front[0] + possible_dirs[i], possible_dirs[len(possible_dirs) - i - 1]))

    def ai_move(self, target, valid_pos, obstacle_pos):
        """
        Default trajectory planning for a enemy
        """
        self.previous_pos = self.curr_pos
        self.curr_pos = self.get_position()

        obst = self.search_obstacle(target, obstacle_pos)
        if obst is not None:
            self.enemy_bfs(obst, obstacle_pos)
        else:
            self.nothing_detected += 1
        if self.nothing_detected == 10:
            self.obstacles.clear()
            self.nothing_detected = 0
        next_angle = self.potential_fields_path_planning(target)
        next_angle = self.search_valid_direction(next_angle, valid_pos)

        self.move(next_angle[0]*self.velocity, next_angle[1]*self.velocity)
        velocity_vector = self.estimate_velocity()
        if np.linalg.norm(velocity_vector):
            self.looking_angle = -np.degrees(np.arctan2(velocity_vector[1], velocity_vector[0]))

    def play_noise(self, time, player_position):
        """
        Plays the enemy's noise sound effect.
        This is an abstract method.
        """
        pass
