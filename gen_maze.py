"""
Handling cell flags, 2d arrays and board gen.
Must be packagable into a distrib package.
"""

import random


class Cell:
    def __init__(self, x: int, y: int, visited: bool = False, walls: int = 15) -> None:
        self.x = x
        self.y = y
        self.visited = visited
        self.walls = walls
"""
    method: remove_shared_wall(cell_current, cell_neihbour, direction:str) :
        if dir is NORTH:
            substract north from cell_current.walls bitmask
            substract south from cell_neighb.walls bitmask
        apply the same for east south and west

    method: generate() -> list[list[Cell]]:
        init history stack as empty list 
        pick starting cell, set visited=true, push to historystack
        while historystack is not empty:
            current  = top item of history stack
            valid_options = call get_univisitedneighbouts(current)
            if valod options is not empty:
                pick random choice direction neighor cell from list
                set chosem_cell_visited = true
                push chosen_cell t to histort stack
            else
                pop top item off hisorty stack (backtrack)

    method: apply_pacman() -> None:
        #rule1 corners are open
        define corner_tples = [(0,0), (width-1,0), (0, height-1), (width-1,height-1)]
        foor each (cx, cy) in corner_tuples:
            force open at least one inner wall by sustracting it from the bitmask

        #rule2 ensure center area loop space is clear
        calc center_x= width//2, center_y= height//2
        for x from center_x -1 to center_x + 1:
         for y from center_y - 1 to center_1 + 1:
            destroy inner walls between center cells 

        #rule3 destroy dead-ends
        for each cell in matrix:
            count activate ramining walls by checking bitwise boundaries
            if cell has 3 walls active
                pick a random closed dir that doesnt blow past map borders
                fetch cell sittin behind that wall side
                call remove_wall(current_cell, neighbout_cell, chosen_dir)
    
    method execute_gen() -> list[lis[Cell]]:
        call generate()
        if perfect flag isTrue:
            call force_forty_two()
        else:
            cal apply_pacman()
        return self.matrix

    method: export to hex strings () -> list[str]:
        inti empty rows string list
        for each row in matrix:
            inti current ro string = ""
            for each cell in current_row:
                convert cell.walls int to uppercase hex
                append hex to current-row_string
            append cuurent row string to rowsstring list
        return rows string list
"""
class MazeGenerator:
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __init__(
            self,
            width: int,
            height: int,
            entry_coord: tuple[int, int],
            exit_coord: tuple[int, int],
            seed: int,
            perfect: bool
            ) -> None:
        self.width = width
        self.height = height
        self.entry_coord = entry_coord
        self.exit_coord = exit_coord
        self.perfect = perfect

        random.seed(seed)
        self.blocked_cells: set[tuple[int, int]] = set()
        self.grid: list[list[int]] = []
        for y in range(self.height):
            row: list[Cell] = []
            for x in range(self.width):
                row.append(Cell(x, y))
            self.grid.append(row)
        self._carve_42_pattern()
        self.print_grid()

    
    def _carve_42_pattern(self) -> set:
        if self.width < 9 or self.height < 7:
            return
        start_x = (self.width - 7) // 2
        start_y = (self.height - 5) // 2
        blocked_offsets = {
                (0, 0), (2, 0),
                (0, 1), (2, 1),
                (0, 2), (1, 2), (2, 2),
                        (2, 3),
                        (2, 4),
                (4, 0), (5, 0), (6, 0),
                                (6, 1),
                (4, 2), (5, 2), (6, 2),
                (4, 3),
                (4, 4), (5, 4), (6, 4) 
                }
        for dx, dy in blocked_offsets:
            self.blocked_cells.add((start_x + dx, start_y + dy))

    def _get_valid_neighbors(self, x: int, y:int
            )-> list[tuple[tuple[int, int], int, int]]:
        neighbors= []
        directions = [
                (0, -1, self.NORTH, self.SOUTH),
                (1, 0, self.EAST, self.WEST),
                (0, 1, self.SOUTH, self.NORTH),
                (-1, 0, self.WEST, self.EAST)
                ]
        for dx, dy, wall_curr, wall_next in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (nx, ny) not in self.blocked_cells:
                    if not self.grid[ny][nx].visited:
                        neighbors.append((nx, ny), wall_curr, wall_next)
        return neighbors

    def _generate_perfect_maze(self) -> None:
        start_x, start_y = self.entry_coord
        sef.grid[start_y][start_x].visited = True
        stack [(start_x, start_y)]
        while stack:
            cx, cy = stack[-1]
            neighbors = self._get_valid_neighbors(cx, cy)
            if neighbors:
                for n in neighbors:
                    
                    stack.append(n)
                    n.visited = True

            else:
                stack.pop

#TESTING PRINT GRID       
    def print_grid(self) -> None:
        for y in range(self.height):
            row_chars = []
            for x in range(self.width):
                if (x, y) in self.blocked_cells:
                    row_chars.append("  ")
                else:
                    row_chars.append(f"{self.grid[y][x].walls}")
            print(" ".join(row_chars))

if __name__ == "__main__":
    MazeGenerator(15, 15, [0, 0], [5, 5], 7, True)
