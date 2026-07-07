"""
DFS backtracking line generators
"""


"""
def solve_maze (matrix, start, end _> list[tuple[]int,int]):
    inti ist acting as stack array 
    inti a visisted set tracking tuple pairs
    init an empty tracking lookup dict: parent_map = {}

    add start coord tuple to  contaner and mark start as visited
    goal_found = False

    while stack list not empy:
        current coord = pop last item from stack LIFO
        if current_ cord matches end cord tuple:
            goal_found = True
            break

        extract current cell object from matrix using current_cords
        define directions movementts lookups matching bit values:
            if NORTH bit is opne (0): add (x, y - 1) to open paths
            same for south and west open boundaries

        for each valid adjacent move coord tuple:
            if move coor sits in grid bounds and is not in visited set:
                mark move coord as visited
                map tracking pointer : parent_map[move] = cuurent_coords
                add move coord to data collection

    if goal_found is False:
        return empty list since no valid path exists

    #backtracking line generation
    init clean solution_path array list
    set trace_position = end coord tuple

    while trace_position not equal start coord tuple:
        append trace_pos to solution_path list
        trace_position = parent_map[trace_position] to step backwards
    append start coord tuple to finalize path loop
    reverse solution_path list so it read from start to end
    return sluton_path list
   
define path_to_letters(coord path) -> str:
    ini output_string = ""
    loop throuh path indexes:
        if dy == -1: append N to output
        same with E, S and N
    return output_string


"""
