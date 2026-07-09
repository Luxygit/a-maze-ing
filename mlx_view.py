import sys
import os
import signal
import mlx
from typing import Any

"""
define MLXGraphicEgine class:
    on init matrix, soltion path:
        store matrix and solution path arrays
        set tile_sze = 32 px per block
        calc window bounds : x idth * tile_size, Y = heigh * Tilesize
        init MLX framework env
        register keyboard trackking hooks.
        map ESC to termination script
        remember ctrl c or d must not crash it
        register display loop hook, bind hook to exec render_frame method
    method: render_frame()-> none:
        clear graphic window background canvas buffer
        loop through every row and col cord in the matrix
            calc screen postion: ixel_x=col *Tilesize, pixel_y=row * tile_size
            draw background ground floor tile asset sprite at (pixel_x, pixel_y)

            read cell.walls 4-bit mask byte flads from matrixblock:
                if norh bit is set render solid hrizontal line boundary along top block edge
                if east bit is set: remder solid vertical line bound along right block edge
                same for south and west

        if self.show_soution_path is True:
            loop each stepcoord element in the soution path array list
                calc path canvas position path_x = step_coord.col * tile size, path_y = stp_coord.row * tile_size
                draw special coloured route path sqate indicator sprite at path_x, path_y
        flush update frame buffer laout to window screen disply engine
"""

# Window Manager close request event codes
_X11_CLIENT_MESSAGE = 33
_X11_DESTROY_NOTIFY = 17

class MLXGraphic:
    def __init__(self, width: int = 640, height: int = 480) -> None:
        self.width = width
        self.height = height
        self.mlx = mlx.Mlx()

        # 1. Initialize core system graphics pointer connections
        self.mlx_ptr = self.mlx.mlx_init()
        if not self.mlx_ptr:
            print("MiniLibX initialization failed.")
            sys.exit(1)

        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, self.width, self.height, "Green Rectangle Test"
        )
        if not self.win_ptr:
            print("Failed to build targeting window context.")
            sys.exit(1)

        # 2. Register standard input hooks
        self.mlx.mlx_key_hook(self.win_ptr, self._on_key, None)
        self.mlx.mlx_hook(self.win_ptr, _X11_CLIENT_MESSAGE, 1 << 16, self._on_close, None)
        self.mlx.mlx_hook(self.win_ptr, _X11_DESTROY_NOTIFY, 0, self._on_close, None)

        # 3. ✅ REGISTER SUSPENSION SIGNAL INTERCEPTOR (Ctrl+Z)
        signal.signal(signal.SIGTSTP, self._on_terminal_suspend)

    def _draw(self) -> None:
        """Standard canvas memory buffer generation loop."""
        img_ptr = self.mlx.mlx_new_image(self.mlx_ptr, self.width, self.height)
        mv, bpp, size_line, _fmt = self.mlx.mlx_get_data_addr(img_ptr)
        bytes_per_pixel = max(bpp // 8, 1)

        rect_w = int(self.width * 0.8)
        rect_h = int(self.height * 0.8)
        start_x = (self.width - rect_w) // 2
        start_y = (self.height - rect_h) // 2

        for y in range(start_y, start_y + rect_h):
            for x in range(start_x, start_x + rect_w):
                offset = y * size_line + x * bytes_per_pixel
                opaque_green = 0xFF00FF00
                data = opaque_green.to_bytes(4, "little")[:bytes_per_pixel]
                mv[offset:offset + bytes_per_pixel] = data

        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, img_ptr, 0, 0)
        self.mlx.mlx_destroy_image(self.mlx_ptr, img_ptr)

    def force_emergency_exit(self) -> None:
        """Hardware-level backup termination to avoid underlying C thread loops freezing."""
        print("\nClose event intercepted. Terminating graphics pipelines safely...")
        try:
            if self.win_ptr:
                self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        except Exception:
            pass
        os._exit(0)

    def run(self) -> None:
        self._draw()
        self.mlx.mlx_loop(self.mlx_ptr)
        self.force_emergency_exit()

    # -- Callback Hook Event Targets ----------------------------------------

    def _on_key(self, keycode: int, _param: object) -> int:
        if keycode in (53, 65307):
            self.mlx.mlx_loop_exit(self.mlx_ptr)
            self.force_emergency_exit()
        return 0

    def _on_close(self, _param: object = None) -> int:
        self.mlx.mlx_loop_exit(self.mlx_ptr)
        self.force_emergency_exit()
        return 0

    # -- ✅ SIGNAL INTERCEPT SIGNAL HANDLER ---------------------------------
    def _on_terminal_suspend(self, signum: int, frame: Any) -> None:
        """Fires instantly when Ctrl+Z is triggered in the terminal."""
        print("\nCtrl+Z detected! Erasing window before suspending process...")
        try:
            if self.win_ptr:
                # 1. Cleanly tear down the active window manager representation
                self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
                self.win_ptr = None
        except Exception:
            pass

        # 2. Reset the handler to default so we don't cause an infinite loop
        signal.signal(signal.SIGTSTP, signal.SIG_DFL)

        # 3. Manually pass the suspend signal back down to stop the background thread cleanly
        os.kill(os.getpid(), signal.SIGTSTP)

