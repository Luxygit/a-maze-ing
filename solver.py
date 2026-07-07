"""
DFS BFS traversal algos and backtracking line generators
"""


"""
def pathfinder function:
    solve(matrix: list[list[CELL]]), start: tuple[int, int], end: tuple, algo: str
    ) -> str
    init tracking data collection (list as a stack for dfs
    init tracking data collection (collections.deque for bfs)
    init a set tracking visited coordinate tuples
    init an empty tracking lookup dict: parent_map = {}

    add start coord tuple to data collection and mark start as visited
    goal_found = False

    while datacollection contains items:
        if algo == dfs:
            current coord = pop last element from data collection LIFO
        else:
            current coord = pop first eleetn from data collection FIFO
        if current_ cord matches end cord tuple:
            goal_found = True
            break

        extract current cell object from matrix using current_coords
        define directions to look up based on active wallls bitmask flags:
            if cell.walls not contain NORTH wall add neighbour (x, y-1) to valid moves
            if cell.walls not contain EAST add neighbour (x+1, y) to valid moves
            same for south and west open boundaries
        for each valid adjacent move coord tuple:
            if move coor sits in grid bounds and is not in visited set:
                mark move coord as visited
                map tracking pointer : parent_map[move] = cuurent_coords
                add move coord to data collection

    if goal_found is False:
        return empty list since no valid path exists

    #backtracking line geneation
    init clean solution_path array list
    set trace_position = end coord tuple

    while trace_position not equal start coord tuple:
        append trace_pos to solution_path list
        trace_position = parent_map[trace_position] 


"""
