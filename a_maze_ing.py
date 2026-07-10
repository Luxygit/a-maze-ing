"""

"""

import sys
import gen_maze
import solve_maze
import mlx_view


def parse_arguments() -> tuple[int, int, int, bool] | None:
    if len(sys.argv) != 5:
        print("Usage: python3 a_maze_ing.py <width> <height> <seed> <perfect_flag>")
        print("Example: python3 a_maze_ing.py 15 15 42 True")
        return None

    try:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        seed = int(sys.argv[3])
        perfect_str = sys.argv[4].strip().lower()
        if perfect_str in ("true", "1"):
            perfect = True
        elif perfect_str in ("false", "0"):
            perfect = False
        else:
            print("Error: perfect_flag must be 'True', 'False', '1', or '0'.")
            return None

    except ValueError:
        print("Error: width, height, and seed must be valid whole integers.")
        return None
    if width <= 0 or height <= 0:
        print("Error: Dimensions must be greater than 0.")
        return None
    if width < 9 or height < 7:
        print("Error: Dimensions too small to center the '42' pattern safely.")
        print("Minimum requirements: Width >= 9, Height >= 7.")
        return None
    return width, height, seed, perfect

def main() -> None:
    args = parse_arguments()
    if not args:
        sys.exit(1)
    width, height, seed, perfect = args
    entry_coord = (0, 0)
    exit_coord = (width - 1, height - 1)
    print(f"Building a {width}x{height} maze (Seed: {seed}, Perfect: {perfect})...")
    maze = gen_maze.MazeGenerator(width, height, entry_coord, exit_coord, seed, perfect)
    solver = solve_maze.MazeSolver(maze)
    print("Opening MLX graphical viewport screen window... Press ESC or close window to exit.")
    view = mlx_view.MlxView(maze, solver)
    view.run()


if __name__ == "__main__":
    main()
