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

class MazeSolver:
    """Handles pathfinding to discover the path from entry to exit."""

    def __init__(self, generator) -> None:
        # Link directly to the completed maze instance metrics
        self.width = generator.width
        self.height = generator.height
        self.entry_coord = generator.entry_coord
        self.exit_coord = generator.exit_coord
        self.grid = generator.grid
        self.blocked_cells = generator.blocked_cells

        # 1. This list will store our final path coordinates in order: [(x1, y1), (x2, y2), ...]
        self.solution_path: list[tuple[int, int]] = []

        # Execute the pathfinder
        self._solve()

    def _get_walkable_neighbors(self, x: int, y: int, visited_set: set[tuple[int, int]]) -> list[tuple[int, int]]:
        """Returns a list of adjacent coordinates that have an open path connection."""
        walkable = []

        # Directions mapping configuration format: (dx, dy, wall_mask_on_current_cell)
        # Note: We must look up the generator constants (1, 2, 4, 8) using our class variables
        directions = [
            (0, -1, 1),  # North
            (1, 0,  2),  # East
            (0, 1,  4),  # South
            (-1, 0, 8)   # West
        ]

        current_cell = self.grid[y][x]

        for dx, dy, wall_flag in directions:
            nx, ny = x + dx, y + dy

            # Boundary & Blocked Check
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (nx, ny) not in self.blocked_cells and (nx, ny) not in visited_set:
                    # ✅ CRITICAL BITWISE CHECK: The path is ONLY walkable if the wall flag bit is 0 (open)
                    # If (current_cell.walls & wall_flag) == 0, there is no wall blocking us!
                    if (current_cell.walls & wall_flag) == 0:
                        walkable.append((nx, ny))
        return walkable

    def _solve(self) -> None:
        """Finds a valid sequence of open coordinates from entry to exit via DFS."""
        start_x, start_y = self.entry_coord
        
        # 1. Initialize our stack with the starting point and create a separate visited set
        stack = [(start_x, start_y)]
        visited = {(start_x, start_y)}

        while stack:
            cx, cy = stack[-1]

            # 2. Check if the current cell is our destination exit
            if (cx, cy) == self.exit_coord:
                # We found the exit! Save the full stack history as our solution path
                self.solution_path = list(stack)
                return

            # 3. Fetch any open, unvisited corridors adjacent to our current location
            neighbors = self._get_walkable_neighbors(cx, cy, visited)

            if neighbors:
                # In pathfinding DFS, we can simply take the first available branch route
                nx, ny = neighbors[0]
                
                # Mark it as visited for the solver and push it onto our exploration path
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                # Stuck? Backtrack out of this corridor branch safely
                stack.pop()
# print teeeeest
    def print_solution_test(self) -> None:
        """Temporary debugger to show coordinates making up the trail."""
        print(f"\nSolution Path Found ({len(self.solution_path)} steps):")
        print(self.solution_path)

if __name__ == "__main__":
    import gen_maze
    
    # 1. Create a 15x15 perfect maze instance framework
    maze = gen_maze.MazeGenerator(15, 15, (0, 0), (14, 14), 42, True)
    
    # 2. Feed that exact maze generator object straight into our path solver
    solver = MazeSolver(maze)
    solver.print_solution_test()
