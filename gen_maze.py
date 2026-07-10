"""
"""

import random


class Cell:
    def __init__(self, x: int, y: int, visited: bool = False, walls: int = 15) -> None:
        self.x = x
        self.y = y
        self.visited = visited
        self.walls = walls


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
        self.entry_coord = tuple(entry_coord)
        self.exit_coord = tuple(exit_coord)
        self.perfect = perfect

        random.seed(seed)
        self.blocked_cells: set[tuple[int, int]] = set()
        self.grid: list[list[Cell]] = []
        for y in range(self.height):
            row: list[Cell] = []
            for x in range(self.width):
                row.append(Cell(x, y))
            self.grid.append(row)
        self._carve_42_pattern()
        self._generate_perfect_maze()
        if not self.perfect:
            self._apply_pacman_rules()
        en_x, en_y = self.entry_coord
        ex_x, ex_y = self.exit_coord
        if 0 <= en_x < self.width and 0 <= en_y < self.height:
            self.grid[en_y][en_x].walls &= ~self.WEST
        if 0 <= ex_x < self.width and 0 <= ex_y < self.height:
            self.grid[ex_y][ex_x].walls &= ~self.EAST
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

    def _get_valid_neighbors(self, x: int, y:int,
                             check_visited: bool = True
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
                    if not check_visited or not self.grid[ny][nx].visited:
                        neighbors.append(((nx, ny), wall_curr, wall_next))
        return neighbors

    def _generate_perfect_maze(self) -> None:
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
        for y in range(self.height):
            for x in range(self.width):
                # 1. Skip cells that are part of our blocked '42' pattern
                if (x, y) in self.blocked_cells:
                    continue
                cell = self.grid[y][x] 
                # 2. Check if the cell is a dead-end (exactly 3 walls standing)
                if cell.walls.bit_count() == 3:
                    # Look for any available neighbors to break into
                    neighbors = self._get_valid_neighbors(x, y, check_visited=False) 
                    if neighbors:
                        # Pick a random neighbor and break the wall between them
                        (nx, ny), w_curr, w_next = random.choice(neighbors)
                        self.grid[y][x].walls &= ~w_curr
                        self.grid[ny][nx].walls &= ~w_next

#TESTING PRINT GRID       
    def print_grid(self) -> None:
        print("+" + "---+" * self.width)
        for y in range(self.height):
            row_str = "|" if (0, y) in self.blocked_cells or (self.grid[y][0].walls & self.WEST) else " "

            for x in range(self.width):
                if (x, y) in self.blocked_cells:
                    cell_body = "██"
                    east_wall = "█"
                else:
                    if (x, y) == self.entry_coord:
                        cell_body = "S "
                    elif (x, y) == self.exit_coord:
                        cell_body = "E "
                    else:
                        cell_body = "  "
                    east_wall = "|" if (self.grid[y][x].walls & self.EAST) else " "
                row_str += cell_body + east_wall
            print(row_str)
            bottom_str = "+"
            for x in range(self.width):
                if (x, y) in self.blocked_cells:
                    bottom_str += "███+"
                elif self.grid[y][x].walls & self.SOUTH:
                    bottom_str += "---+"
                else:
                    bottom_str += "   +"
            print(bottom_str)

if __name__ == "__main__":
    MazeGenerator(15, 15, [0, 0], [14, 14], 7, True)
