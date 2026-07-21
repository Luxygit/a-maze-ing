"""
Maze generation through DFS algorithm Last-in First-out, and bitwise
operations, while respecting both perfect and non perfect subject
requirements.
"""

import random


class Cell:
    """blueprint for each single square in the maze grid"""
    def __init__(self, x: int, y: int, visited: bool = False,
                 walls: int = 15) -> None:
        self.x = x
        self.y = y
        self.visited = visited
        self.walls = walls


class MazeGenerator:
    """
    Through bitmasking, this class, creates a grid of cells,
    destroys walls between them and displays the 42 pattern when possible
    """
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
        self.entry_coord = tuple(entry_coord)
        self.exit_coord = tuple(exit_coord)
        self.perfect = perfect
        # randomizing a seed number
        random.seed(seed)
        # init a unique set of blocked cell positions for the 42 pattern
        self.blocked_cells: set[tuple[int, int]] = set()
        self.grid: list[list[Cell]] = []
        # looping through rows and columns to populate the grid
        for y in range(self.height):
            row: list[Cell] = []
            for x in range(self.width):
                row.append(Cell(x, y))
            self.grid.append(row)
        self.config_valid = self._carve_42_pattern()
        # calling conditional methods to modify the grid
        if self.config_valid:
            self._generate_perfect_maze()
            if not self.perfect:
                self._apply_pacman_rules()
            self._enforce_external_borders()

    def _carve_42_pattern(self) -> bool:
        """conditionally drawing a 42 patter in the center of the maze"""
        if self.width < 13 or self.height < 9:
            return True
        start_x = (self.width - 9) // 2
        start_y = (self.height - 5) // 2
        blocked_offsets = {
                (0, 0), (2, 0),
                (0, 1), (2, 1),
                (0, 2), (1, 2), (2, 2),
                        (2, 3),
                        (2, 4),
                (6, 0), (7, 0), (8, 0),
                                (8, 1),
                (6, 2), (7, 2), (8, 2),
                (6, 3),
                (6, 4), (7, 4), (8, 4)
                }
        for dx, dy in blocked_offsets:
            abs_cell = (start_x + dx, start_y + dy)
            if self.entry_coord == abs_cell or self.exit_coord == abs_cell:
                print("Error: Entry or Exit cannot be inside 42 pattern")
                return False
            self.blocked_cells.add(abs_cell)
        return True

    def _get_valid_neighbors(
            self,
            x: int,
            y: int,
            check_visited: bool = True
    ) -> list[tuple[tuple[int, int], int, int]]:
        """
        checks if the 4 adjacent cells around coord x,y can be broken
        taking into account dx,dy that are the direction steps,
        wall_curr the bitmask for the starting border wall value
        and wall_next for the neighbour wall
        check_visited is passed to indicate if the algorithm should
        care or not if cells were already visited and revisit them.
        """
        neighbors = []
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
                    if not check_visited or not self.grid[ny][nx].visited:
                        neighbors.append(((nx, ny), wall_curr, wall_next))
        return neighbors

    def _generate_perfect_maze(self) -> None:
        """
        looping thru neighbors to open walls and link them to the maze
        comparing wall values via bitwise operations.
        saves this neighbour in the stack memory to keep checking its
        own neighbours and once its a dead end, it deletes it from the stack
        to continue with the previous saved neighbour in the stack
        """
        start_x, start_y = self.entry_coord
        self.grid[start_y][start_x].visited = True
        stack = [(start_x, start_y)]
        while stack:
            cx, cy = stack[-1]
            neighbors = self._get_valid_neighbors(cx, cy, check_visited=True)
            if neighbors:
                (nx, ny), w_curr, w_next = random.choice(neighbors)
                self.grid[cy][cx].walls &= ~w_curr
                self.grid[ny][nx].walls &= ~w_next
                self.grid[ny][nx].visited = True
                stack.append((nx, ny))
            else:
                stack.pop()

    def _apply_pacman_rules(self) -> None:
        """
        previos method only opened one random neighbours wall, but for
        the non-perfect maze we open dead ends as well,
        checking if their wall int in binary is 1 three times then it is a
        dead end and chooses a random neighbor and opens their walls.
        """
        max_sweeps = self.width * self.height
        sweep_count = 0
        while sweep_count < max_sweeps:
            dead_ends_found = False
            for y in range(self.height):
                for x in range(self.width):
                    if (x, y) in self.blocked_cells:
                        continue
                    cell = self.grid[y][x]
                    if bin(cell.walls).count("1") == 3:
                        neighbors = self._get_valid_neighbors(
                                x, y,
                                check_visited=False)
                        if neighbors:
                            (nx, ny), w_curr, w_next = random.choice(neighbors)
                            self.grid[y][x].walls &= ~w_curr
                            self.grid[ny][nx].walls &= ~w_next
                            dead_ends_found = True
            sweep_count += 1
            if not dead_ends_found:
                break
        if self.width > 1 and self.height > 1:
            # opening up the 4 corners of the maze.
            self.grid[0][0].walls &= ~(self.EAST | self.SOUTH)
            self.grid[0][1].walls &= ~self.WEST
            self.grid[1][0].walls &= ~self.NORTH
            # top right corner
            tr_x = self.width - 1
            self.grid[0][tr_x].walls &= ~(self.WEST | self.SOUTH)
            self.grid[0][tr_x - 1].walls &= ~self.EAST
            self.grid[1][tr_x].walls &= ~self.NORTH
            # bottom left corner
            bl_y = self.height - 1
            self.grid[bl_y][0].walls &= ~(self.EAST | self.NORTH)
            self.grid[bl_y][1].walls &= ~self.WEST
            self.grid[bl_y - 1][0].walls &= ~self.SOUTH
            # bottom right corner
            br_x, br_y = self.width - 1, self.height - 1
            self.grid[br_y][br_x].walls &= ~(self.WEST | self.NORTH)
            self.grid[br_y][br_x - 1].walls &= ~self.EAST
            self.grid[br_y - 1][br_x].walls &= ~self.SOUTH
        # opening up center corridor
        mid_x, mid_y = self.width // 2, self.height // 2
        if (mid_x, mid_y) not in self.blocked_cells:
            self.grid[mid_y][mid_x].walls &= ~(
                    self.NORTH |
                    self.EAST |
                    self.SOUTH |
                    self.WEST
                    )
            if mid_y > 0 and (mid_x, mid_y - 1) not in self.blocked_cells:
                self.grid[mid_y - 1][mid_x].walls &= ~self.SOUTH
            else:
                self.grid[mid_y][mid_x].walls |= self.NORTH
            if mid_x < self.width - 1 and (
                    mid_x + 1, mid_y) not in self.blocked_cells:
                self.grid[mid_y][mid_x + 1].walls &= ~self.WEST
            else:
                self.grid[mid_y][mid_x].walls |= self.EAST
            if mid_y < self.height - 1 and (
                    mid_x, mid_y + 1) not in self.blocked_cells:
                self.grid[mid_y + 1][mid_x].walls &= ~self.NORTH
            else:
                self.grid[mid_y][mid_x].walls |= self.SOUTH
            if mid_x > 0 and (mid_x - 1, mid_y) not in self.blocked_cells:
                self.grid[mid_y][mid_x - 1].walls &= ~self.EAST
            else:
                self.grid[mid_y][mid_x].walls |= self.WEST

    def _enforce_external_borders(self) -> None:
        """
        using the bitwise OR assignment and looping thru every cell
        of the borders it modifies that outer border specific bit to 1
        """
        for y in range(self.height):
            for x in range(self.width):
                if x == 0:
                    self.grid[y][x].walls |= self.WEST
                if x == self.width - 1:
                    self.grid[y][x].walls |= self.EAST
                if y == 0:
                    self.grid[y][x].walls |= self.NORTH
                if y == self.height - 1:
                    self.grid[y][x].walls |= self.SOUTH
