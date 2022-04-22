# maze.py
import random

import numpy as np
import copy
import queue


class Maze:
    """
    A 2D maze board implemented using graph.
    """

    def __init__(self, x_dim, y_dim, walls: set = None, reward_chance=0):
        if walls is None:
            walls = set()
        self._grid_shape = (x_dim, y_dim)
        self._walls = walls
        self._connectivity = self._generate_full_connectivity()
        self.add_walls(self._walls)
        self._reward_grid = None
        self._reward_chance = reward_chance
        self._generate_reward()

    def _generate_full_connectivity(self):
        """
        Returns
        -------
        dict
            a dictionary whose keys are position (x, y) as tuples of 2 integers
            and values are the set of positions not separated by walls.
        """
        x_dim, y_dim = self._grid_shape
        connectivity = dict()
        for x in range(x_dim):
            for y in range(y_dim):
                s = set()
                for delta in [-1, 1]:
                    if 0 <= x + delta < x_dim:
                        s.add((x + delta, y))
                    if 0 <= y + delta < y_dim:
                        s.add((x, y + delta))
                connectivity[(x, y)] = s
        return connectivity

    def get_connectivity(self):
        return self._connectivity

    def get_edges(self, pos):
        if not self._is_valid_pos(pos):
            raise IndexError
        return self._connectivity[pos]

    def _generate_reward(self):
        x_dim, y_dim = self._grid_shape
        self._reward_grid = np.zeros((y_dim, x_dim))
        x_dim, y_dim = self._grid_shape
        for x in range(x_dim):
            for y in range(y_dim):
                self._reward_grid[y, x] = 1 if random.random() <= self._reward_chance else 0

    def get_reward(self, pos) -> int:
        if not self._is_valid_pos(pos):
            raise IndexError
        return self._reward_grid[pos]

    def _is_valid_pos(self, pos):
        if 0 <= pos[0] < self._grid_shape[0] and 0 <= pos[1] < self._grid_shape[1]:
            return True
        else:
            return False

    def num_of_reachable_cells(self, x, y, n) -> int:
        # x and y need to be separate parameters due to later numpy vectorization
        """
        This function returns the number of reachable cells in n steps, starting from the given position.

        Parameters
        ----------
        x: int
            x index of the interested cell

        y: int
            y index of the interested cell

        n: int
            the number of steps considered, excluding the given initial position (x,y)
        Returns
        -------
        int
            the number of reachable cells from the given position
        """
        # perform depth-first search, but only for n levels deep.
        connectivity = copy.deepcopy(self._connectivity)  # is deepcopy necessary?
        q = queue.SimpleQueue()
        visited = set()
        count = 0

        q.put(((x, y), 0))  # a tuple of (position, step) where position is also a tuple of (x,y)
        while not q.empty():
            pos, step = q.get()
            if step > n:  # stop expanding if reached n-step horizon
                break
            # print(f'{pos} is' + ('' if pos in visited else ' not') + ' in visited')

            if pos not in visited:
                visited.add(pos)
                count += 1
                for next_pos in connectivity[pos]:
                    if next_pos not in visited:
                        q.put((next_pos, step + 1))

        assert count == len(visited)
        return count

    # define the vectorized function, where x and y are expected as 1D vectors.
    def num_of_reachables(self, n: int):
        """
        numpy vectorized version of the method 'num_of_reachable_cells'

        Parameters
        ----------
        n: int
            the number of steps considered, excluding the given initial position (x,y)
        Returns
        -------
        np.ndarray
            A 2D np.array, where each cell contains the number of reachable cells from itself in n steps.
        """
        x_dim, y_dim = self._grid_shape
        Y, X = np.mgrid[0:y_dim, 0:x_dim]
        Y = Y.flatten()
        X = X.flatten()
        num_grid = np.vectorize(self.num_of_reachable_cells, excluded={'n'})(X, Y, n).reshape((y_dim, x_dim))
        return num_grid

    # edges store the number of edges at each grid position
    def inspect_edge_num(self):
        """
        Returns
        -------
        np.ndarray
            A 2D np.array, where each cell contains the number of reachable cells from itself in 1 step.
        """
        edge_count = {pos: len(self._connectivity[pos]) for pos in self._connectivity}
        edges = np.zeros(self._grid_shape)
        for pos in edge_count:
            x, y = pos
            edges[y, x] = edge_count[pos]
        return edges

    def add_wall(self, wall):
        """
        the method adds a wall into the maze, which also removes an edge from the connectivity graph
        Parameters
        ----------
        wall: ((int, int), (int, int))
            the inter-cell connection prohibited by the wall
        """
        if len(wall) != 2 or len(wall[0]) != 2 or len(wall[0]) != 2:
            raise ValueError

        self._walls.add(wall)
        self._remove_edge(wall)

    def add_walls(self, walls):
        """
        the method adds walls into the maze, which removes edges from the connectivity graph
        Parameters
        ----------
        walls:
            an iterable whose elements are ((int, int), (int, int)) as described in 'add_wall' method
        """
        for w in walls:
            self.add_wall(w)

    def _remove_edge(self, wall):
        """removes bidirectional edges between two cells that are separated by a wall"""
        cell1, cell2 = wall
        self._connectivity[cell1].remove(cell2)
        self._connectivity[cell2].remove(cell1)

    def get_empowerment_grid(self, n):
        num_grid = self.num_of_reachables(n)  # HxW: y_dim x x_dim
        empowerment_grid = np.log2(num_grid)  # convert to bits of information

        return empowerment_grid

    def get_grid_shape(self):
        return self._grid_shape
