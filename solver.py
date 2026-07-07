"""
DFS BFS traversal algos and backtracking line generators
"""


"""
def pathfinder function:
    solve(matrix: list[list[CELL]]), start: tuple[int, int], end: tuple, algo: str
    ) -> str

    if mode == dfs
        init collection container as a list LIFO stack
    else:
        init collection container as collections.deque() FIFO queue

    inti a visisted set tracking tuple pairs
    init an empty tracking lookup dict: parent_map = {}

    add start coord tuple to collection contaner and mark start as visited
    target_found = False

    while collection not empy:
        if amode == dfs:
            current_x, cuurent_y  = pop last element from data collection LIFO
        else:
            current coord = pop first eleetn from collection
        if current_ cord matches end cord tuple:
            goal_found = True
            break

        extract current cell object from matrix using current_x, curren_y
        define directions movementts lookups matching bit values:
            if current_cell.walls not contain NORTH wall add neighbour (x, y-1) to valid moves
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
        trace_position = parent_map[trace_position] to step backwards
    append start coord tuple to finalize path loop
    reverse solution_path list so it read from start to end
    return sluton_path list
   
define string vector directon conversion utility:
    convert_coord_to_lettes(coordinate_path: list[tuple[int,int]])
    if coordpat leng is less than 2:
        return ""
    init letter_output_buffer = ""
    for index from 0 to len of coord_path - 2:
        current_step = coord_path[i]
        next_step = coord_path[index+1]
        calc offsets: dx = next_step[0] - current_step[0], dy= next_step[1] - current_step[1]
    if dy == -1: append N to letters_out_buffer
    same with E, S and N
    return letters_output_buffer


"""
