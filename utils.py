# utils.py

import numpy as np
import matplotlib.pyplot as plt
import copy
import queue


def num_of_reachable_cells(connectivity, x, y, n):
    """
    This function returns the number of reachable cells in n steps, starting from the given position.
    
    Parameters
    ----------
    connectivity: {(int, int): set((int,int))}
        describes the reachable positions from each cell.
    
    pos: (int, int)
        the position in grid for which to calculate the number of reachable cells
    
    Returns
    -------
    int
        the number of reachable cells from the given position
    """
    # perform depth-first search, but only for n levels deep.
    connectivity = copy.deepcopy(connectivity)
    q = queue.SimpleQueue()
    visited = set()
    count = 0
    
    q.put(((x,y), 0)) # a tuple of (position, step) where position is also a tuple of (x,y)
    while not q.empty():
        pos, step = q.get()
        if step > n: # stop expanding if reached n-step horizon
            break
#         print(f'{pos} is' + ('' if pos in visited else ' not') + ' in visited')

        if pos not in visited:
            visited.add(pos)
            count += 1
            for next_pos in connectivity[pos]:
                if next_pos not in visited:
                    q.put((next_pos, step+1))
    
    assert count == len(visited)
    return count


# edges store the number of edges at each grid position
def inspect_edge_num(connectivity, grid_shape):
    edge_count = {pos: len(connectivity[pos]) for pos in connectivity}
    edges = np.zeros(grid_shape)
    for pos in edge_count:
        x, y = pos
        edges[y, x] = edge_count[pos]
    return edges


def plot_walls(walls: {((int,int), (int,int))}, fmt: str):
    for pos1, pos2 in walls:
        x1, y1 = pos1
        x2, y2 = pos2
        assert (x1 == x2) ^ (y1 == y2) # use XOR because only one of the pairs should be equal
        if x1 == x2:
            plt.plot([x1-0.5, x1+0.5], [(y1+y2)/2, (y1+y2)/2], fmt)
        elif y1 == y2:
            plt.plot([(x1+x2)/2, (x1+x2)/2], [y1-0.5, y1+0.5], fmt)
            
