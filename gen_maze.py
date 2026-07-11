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
		self._enforce_external_borders()

	def _carve_42_pattern(self) -> None:
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
				if (x, y) in self.blocked_cells:
					continue
				cell = self.grid[y][x] 
				if bin(cell.walls).count("1") == 3:
					neighbors = self._get_valid_neighbors(x, y, check_visited=False) 
					if neighbors:
						(nx, ny), w_curr, w_next = random.choice(neighbors)
						self.grid[y][x].walls &= ~w_curr
						self.grid[ny][nx].walls &= ~w_next
		if self.width > 1 and self.height > 1:
			self.grid[0][0].walls &= ~(self.EAST | self.SOUTH)
			self.grid[0][1].walls &= ~self.WEST
			self.grid[1][0].walls &= ~self.NORTH
			tr_x = self.width - 1
			self.grid[0][tr_x].walls &= ~(self.WEST | self.SOUTH)
			self.grid[0][tr_x - 1].walls &= ~self.EAST
			self.grid[1][tr_x].walls &= ~self.NORTH
			bl_y = self.height - 1
			self.grid[bl_y][0].walls &= ~(self.EAST | self.NORTH)
			self.grid[bl_y][1].walls &= ~self.WEST
			self.grid[bl_y - 1][0].walls &= ~self.SOUTH
			br_x, br_y = self.width - 1, self.height - 1
			self.grid[br_y][br_x].walls &= ~(self.WEST | self.NORTH)
			self.grid[br_y][br_x - 1].walls &= ~self.EAST
			self.grid[br_y - 1][br_x].walls &= ~self.SOUTH
		mid_x, mid_y = self.width // 2, self.height // 2
		if (mid_x, mid_y) not in self.blocked_cells:
			self.grid[mid_y][mid_x].walls &= ~(self.NORTH | self.EAST | self.SOUTH | self.WEST)
			if mid_y > 0:
				self.grid[mid_y - 1][mid_x].walls &= ~self.SOUTH
			if mid_x < self.width - 1:
				self.grid[mid_y][mid_x + 1].walls &= ~self.WEST
			if mid_y < self.height - 1:
				self.grid[mid_y + 1][mid_x].walls &= ~self.NORTH
			if mid_x > 0:
				self.grid[mid_y][mid_x - 1].walls &= ~self.EAST

	def _enforce_external_borders(self) -> None:
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
