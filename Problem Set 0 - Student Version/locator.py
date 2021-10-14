from typing import Any, Set, Tuple
from grid import Grid
import utils


def locate(grid: Grid, item: Any) -> Set[Tuple[int, int]]:
    '''
    This function takes a 2D grid and an item
    It should return a list of (x, y) coordinates that specify the locations that contain the given item
    To know how to use the Grid class, see the file "grid.py"  
    '''
    # TODO: ADD YOUR CODE HERE
    itemPlaces = set()
    rows = grid.height
    cols = grid.width
    for row in range(rows):
        for col in range(cols):
            if(item == grid[(col, row)]):
                itemPlaces.add((col, row))
    return itemPlaces
