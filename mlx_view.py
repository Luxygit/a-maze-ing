import sys
import os
import mlx
from typing import Any


class MlxView:
	WALL_COLORS = [0xFFFFFFFF, 0xFF39FF14, 0xFFFFA500, 0xFF00CFFF, 0xFFFF3CBE]

	def __init__(self, generator, solver, regenerate_fn=None) -> None:
		self.generator = generator
		self.solver = solver
		self.regenerate_fn = regenerate_fn

		self.show_path = True
		self.color_idx = 0

		self.cell_size = 24
		self.win_width = self.generator.width * self.cell_size
		self.win_height = self.generator.height * self.cell_size

		self.mlx = mlx.Mlx()
		self.mlx_ptr = self.mlx.mlx_init()
		if not self.mlx_ptr:
			print("MiniLibX initialization failed.")
			sys.exit(1)

		self.win_ptr = self.mlx.mlx_new_window(
			self.mlx_ptr, self.win_width, self.win_height,
            "A-Maze-ing Graphical Viewport"
        )
		if not self.win_ptr:
			print("Failed to build targeting window context.")
			sys.exit(1)
		self.mlx.mlx_key_hook(self.win_ptr, self._on_key, self)
		self.mlx.mlx_hook(self.win_ptr, 33, 1 << 16, self._on_close, self)
		#self.mlx.mlx_hook(self.win_ptr, 17, 1 << 17, self._on_close, self)

	def _put_pixel_to_buffer(self, mv, size_line, bpp, x: int,
                             y: int, color_hex: int) -> None:
		if 0 <= x < self.win_width and 0 <= y < self.win_height:
			offset = y * size_line + x * bpp
			b = color_hex & 0xFF
			g = (color_hex >> 8) & 0xFF
			r = (color_hex >> 16) & 0xFF
			a = (color_hex >> 24) & 0xFF
			try:
				mv[offset] = b
				mv[offset + 1] = g
				mv[offset + 2] = r
				mv[offset + 3] = a
			except (IndexError, TypeError):
				pass

	def _draw_block(self, mv, size_line, bpp, cx: int, cy: int,
                    color_hex: int) -> None:
		start_x = cx * self.cell_size
		start_y = cy * self.cell_size
		for y_offset in range(self.cell_size):
			for x_offset in range(self.cell_size):
				self._put_pixel_to_buffer(
					mv, size_line, bpp, start_x + x_offset,
					start_y + y_offset, color_hex
                )

	def _draw_cell_walls(self, mv, size_line, bpp, cx: int, cy: int) -> None:
		cell = self.generator.grid[cy][cx]
		start_x = cx * self.cell_size
		start_y = cy * self.cell_size
		max_idx = self.cell_size - 1
		wall_color = self.WALL_COLORS[self.color_idx]

		if cell.walls & self.generator.NORTH:
			for x in range(self.cell_size):
				self._put_pixel_to_buffer(mv, size_line,
                                          bpp, start_x + x, start_y, wall_color)

		if cell.walls & self.generator.SOUTH:
			for x in range(self.cell_size):
				self._put_pixel_to_buffer(mv,
                                          size_line,
                                          bpp, start_x + x,
                                          start_y + max_idx,
                                          wall_color)
		if cell.walls & self.generator.WEST:
			for y in range(self.cell_size):
				self._put_pixel_to_buffer(mv, size_line, bpp, start_x, start_y + y, wall_color)

		if cell.walls & self.generator.EAST:
			for y in range(self.cell_size):
				self._put_pixel_to_buffer(mv, size_line, bpp, start_x + max_idx, start_y + y, wall_color)

	def _render(self) -> None:
		img_ptr = self.mlx.mlx_new_image(self.mlx_ptr, self.win_width, self.win_height)
		mv, bpp_bits, size_line, _fmt = self.mlx.mlx_get_data_addr(img_ptr)
		bpp = max(bpp_bits // 8, 1)

		for y in range(self.generator.height):
			for x in range(self.generator.width):
				if (x, y) in self.generator.blocked_cells:
					self._draw_block(mv, size_line, bpp, x, y, 0xFF00FF00)
				elif (x, y) == self.generator.entry_coord:
					self._draw_block(mv, size_line, bpp, x, y, 0xFFFF0000)
				elif (x, y) == self.generator.exit_coord:
					self._draw_block(mv, size_line, bpp, x, y, 0xFF0000FF)
				elif self.show_path and (x, y) in self.solver.solution_path:
					self._draw_block(mv, size_line, bpp, x, y, 0xFFFFFF00)
				else:
					self._draw_block(mv, size_line, bpp, x, y, 0xFF1C1C1C)
				if (x, y) not in self.generator.blocked_cells:
					self._draw_cell_walls(mv, size_line, bpp, x, y)
		self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
		self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, img_ptr, 0, 0)
		self.mlx.mlx_destroy_image(self.mlx_ptr, img_ptr)
		self.mlx.mlx_do_sync(self.mlx_ptr)

	def force_emergency_exit(self) -> None:
		try:
			if self.win_ptr:
				self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
		except Exception:
			pass
		os._exit(0)

	def run(self) -> None:
		self._render()
		self.mlx.mlx_loop(self.mlx_ptr)
		self.force_emergency_exit()

	def _regenerate(self) -> None:
		if self.regenerate_fn is None:
			return
		self.generator, self.solver = self.regenerate_fn()
		self._render()

	def _toggle_path(self) -> None:
		self.show_path = not self.show_path
		self._render()

	def _rotate_colors(self) -> None:
		self.color_idx = (self.color_idx + 1) % len(self.WALL_COLORS)
		self._render()

	def _on_key(self, keycode: int, param: Any) -> int:
		if param is None:
			return 0
		if keycode in (53, 65307, ord("4")):
			param.mlx.mlx_loop_exit(param.mlx_ptr)
			param.force_emergency_exit()
		elif keycode == ord("1"):
			param._regenerate()
		elif keycode == ord("2"):
			param._toggle_path()
		elif keycode == ord("3"):
			param._rotate_colors()
		return 0

	def _on_close(self, param: Any = None) -> int:
		target = param if param is not None else self
		target.mlx.mlx_loop_exit(target.mlx_ptr)
		target.force_emergency_exit()
		return 0
