# experiment.py

from maze import Maze
from agent import Agent, AgentStoppedError
import numpy as np


class Experiment:
    def __init__(self, trial_num, maze, step_num):
        """
        Parameters
        ----------
        trial_num: int
            the number of agent simulation at each maze position
        maze: Maze
        step_num: int
            the number of steps that an agent can take to explore the maze
        """
        self._trial_num = trial_num
        self._maze = maze
        self._avg_reward_grid = np.zeros(maze.get_grid_shape())
        self._step_num = step_num

    def run(self):
        x_dim, y_dim = self._maze.get_grid_shape()
        for x in range(x_dim):
            for y in range(y_dim):
                total_reward = 0
                for _ in range(self._trial_num):
                    a = Agent(self._maze, (x, y), self._step_num)
                    while True:
                        try:
                            a.move(self._maze)
                        except AgentStoppedError:
                            break
                    total_reward += a.get_reward()

                self._avg_reward_grid[y, x] = total_reward / self._trial_num

    def get_reward_grid(self):
        return self._avg_reward_grid
