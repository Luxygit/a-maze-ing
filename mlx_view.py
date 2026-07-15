import sys
import os
import mlx  # type: ignore
from typing import Any


class MlxView:
    """manages memory buffers, interaction and rendering"""
    WALL_COLORS = [
            0xFFFFFFFF, 0xFF39FF14, 0xFFFFA500, 0xFF00CFFF, 0xFFFF3CBE]

    def __init__(
            self, generator: Any, solver: Any, regenerate_fn: Any = None
            ) -> None:
        """initialising grpahic properties, pointer context and listeners"""
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
            print("Mlx initialization failed.")
            sys.exit(1)
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, self.win_width, self.win_height,
            "A-Maze-Ing"
        )
        if not self.win_ptr:
            print("Failed to build window.")
            sys.exit(1)
        self.mlx.mlx_key_hook(self.win_ptr, self._on_key, self)
        self.mlx.mlx_hook(self.win_ptr, 33, 1 << 16, self._on_close, self)

    def _draw_cell_fast(
            self, mv: Any, size_line: int, bpp: int,
            cx: int, cy: int) -> None:
        """Draw cell blocks and walls using memory view slice rows."""
        start_x = cx * self.cell_size
        start_y = cy * self.cell_size
        # Determine base cell color layout
        if (cx, cy) in self.generator.blocked_cells:
            color_hex = 0xFF00FF00  # Green
        elif (cx, cy) == self.generator.entry_coord:
            color_hex = 0xFFFF0000  # Red
        elif (cx, cy) == self.generator.exit_coord:
            color_hex = 0xFF0000FF  # Blue
        elif self.show_path and (cx, cy) in self.solver.solution_path:
            color_hex = 0xFFFFFF00  # Yellow
        else:
            color_hex = 0xFF1C1C1C  # Gray Background
        # Unpack colors into raw byte strings
        b = color_hex & 0xFF
        g = (color_hex >> 8) & 0xFF
        r = (color_hex >> 16) & 0xFF
        a = (color_hex >> 24) & 0xFF
        bg_pixel = bytes([b, g, r, a])
        # Form block row slices
        bg_row = bg_pixel * self.cell_size
        # Unpacking wall color params
        w_color = self.WALL_COLORS[self.color_idx]
        wb, wg, wr, wa = w_color & 0xFF, (
                w_color >> 8) & 0xFF, (w_color >> 16) & 0xFF, (
                        w_color >> 24) & 0xFF
        wall_pixel = bytes([wb, wg, wr, wa])
        cell = self.generator.grid[cy][cx]
        is_blocked = (cx, cy) in self.generator.blocked_cells
        # Process line buffers sequentially
        for y_offset in range(self.cell_size):
            actual_y = start_y + y_offset
            offset = actual_y * size_line + start_x * bpp
            # Copy basic block rows into memory
            mv[offset:offset + len(bg_row)] = bg_row
            if not is_blocked:
                # Carve North wall lines
                if y_offset == 0 and (cell.walls & self.generator.NORTH):
                    mv[offset:offset + len(bg_row)] = wall_pixel * \
                            self.cell_size
                # Carve South wall lines
                elif y_offset == self.cell_size - 1 and (
                        cell.walls & self.generator.SOUTH):
                    mv[offset:offset + len(bg_row)] = wall_pixel * \
                            self.cell_size
                else:
                    # Carve West wall lines
                    if cell.walls & self.generator.WEST:
                        mv[offset:offset + bpp] = wall_pixel
                    # Carve East wall lines
                    if cell.walls & self.generator.EAST:
                        e_offset = offset + (self.cell_size - 1) * bpp
                        mv[e_offset:e_offset + bpp] = wall_pixel

    def _render(self) -> None:
        """Creates new canvas frame"""
        img_ptr = self.mlx.mlx_new_image(
                self.mlx_ptr, self.win_width, self.win_height)
        mv, bpp_bits, size_line, _fmt = self.mlx.mlx_get_data_addr(img_ptr)
        bpp = max(bpp_bits // 8, 1)
        for y in range(self.generator.height):
            for x in range(self.generator.width):
                self._draw_cell_fast(mv, size_line, bpp, x, y)
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self.mlx.mlx_put_image_to_window(
                self.mlx_ptr, self.win_ptr, img_ptr, 0, 0)
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
        if keycode in (65307, ord("4")):
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
