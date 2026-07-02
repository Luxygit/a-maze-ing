"""
maze gen/trnaformations and hexadecimal bitmasking
"""

"""
defining Cell class:
    properties: x, y, visited, walls

defining a GenMaze class:
    init (width, height, perfect)
        store args
        initiaise 2d array matrix with Cell objects
        defining bitmask North=1 east=2 South =4 West=8
        define dict for opposite sides N-S E-W

    get_unvisited_neighbours(cell: Cell) -> list(cell):

