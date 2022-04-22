# agent.py
import random


class AgentStoppedError(Exception):
    pass


class Agent:
    def __init__(self, maze, pos, step_num):
        x_dim, y_dim = maze.get_grid_shape()
        if not (0 <= pos[0] < x_dim and 0 <= pos[1] < y_dim):
            raise ValueError
        self._pos = pos
        self._step_num = step_num
        self._reward = 0

    def sense_reward(self, maze):
        """
        Return
        ------
        set
            the set of positions with rewards. The set can be 0.
        """
        ans = set()
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = self._pos[0] + dx, self._pos[1] + dy
            if 0 <= new_x < maze.get_grid_shape()[0] and 0 <= new_y < maze.get_grid_shape()[1]:
                if maze.get_reward((new_x, new_y)) > 0:
                    ans.add((new_x, new_y))
        return ans

    def collect_reward(self, maze):
        self._reward += maze.get_reward(self._pos)

    def move(self, maze):
        if self._step_num <= 0:
            raise AgentStoppedError

        reward_positions = self.sense_reward(maze)

        # update agent position
        if len(reward_positions) == 0:
            new_positions = maze.get_edges(self._pos)
            self._pos = random.choice([i for i in new_positions])
        else:
            self._pos = random.choice([i for i in reward_positions])

        self._step_num -= 1
        self.collect_reward(maze)

    def get_reward(self):
        return self._reward
