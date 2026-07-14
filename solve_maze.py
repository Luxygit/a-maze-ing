"""Shortest path solution through BFS algorithm"""

from typing import Any


class MazeSolver:
    """finding the shortest path to exit"""
    def __init__(self, generator: Any) -> None:
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
        """finding adjacent cells with open paths"""
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
                if (nx, ny) not in self.blocked_cells and \
                        (nx, ny) not in visited_set:
                    if (current_cell.walls & wall_flag) == 0:
                        walkable.append((nx, ny))
        return walkable

    def _solve(self) -> None:
        """
        using a queue FIFO first in first out to scan the maze layer
        by layer, parent will store the cell we are in and its next neighbor
        then the path is reconstructed from exit to start
        """
        start_x, start_y = self.entry_coord
        if (start_x, start_y) == self.exit_coord:
            self.solution_path = [(start_x, start_y)]
            return

        queue = [(start_x, start_y)]
        visited = {(start_x, start_y)}
        parent = {}
        while queue:
            cx, cy = queue.pop(0)
            if (cx, cy) == self.exit_coord:
                break
            neighbors = self._get_walkable_neighbors(cx, cy, visited)
            for nx, ny in neighbors:
                visited.add((nx, ny))
                parent[(nx, ny)] = (cx, cy)
                queue.append((nx, ny))
        if self.exit_coord in parent or self.entry_coord == self.exit_coord:
            path = []
            curr = self.exit_coord
            while curr != self.entry_coord:
                path.append(curr)
                curr = parent[curr]
            path.append(self.entry_coord)
            path.reverse()
            self.solution_path = path
