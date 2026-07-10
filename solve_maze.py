"""
"""


class MazeSolver:
    def __init__(self, generator) -> None:
        self.width = generator.width
        self.height = generator.height
        self.entry_coord = generator.entry_coord
        self.exit_coord = generator.exit_coord
        self.grid = generator.grid
        self.blocked_cells = generator.blocked_cells
        self.solution_path: list[tuple[int, int]] = []
        self._solve()

    def _get_walkable_neighbors(self, x: int, y: int,
                                visited_set: set[tuple[int, int]]
                                ) -> list[tuple[int, int]]:
        walkable = []
        directions = [
            (0, -1, 1),  # North
            (1, 0,  2),  # East
            (0, 1,  4),  # South
            (-1, 0, 8)   # West
        ]
        current_cell = self.grid[y][x]
        for dx, dy, wall_flag in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (nx, ny) not in self.blocked_cells and (nx, ny) not in visited_set:
                    if (current_cell.walls & wall_flag) == 0:
                        walkable.append((nx, ny))
        return walkable

    def _solve(self) -> None:
        start_x, start_y = self.entry_coord
        stack = [(start_x, start_y)]
        visited = {(start_x, start_y)}
        while stack:
            cx, cy = stack[-1]
            if (cx, cy) == self.exit_coord:
                self.solution_path = list(stack)
                return
            neighbors = self._get_walkable_neighbors(cx, cy, visited)
            if neighbors:
                nx, ny = neighbors[0]
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()
