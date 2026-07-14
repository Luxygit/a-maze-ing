*This project has been created as part of the 42 curriculum by jboan-gu, dievarga*

# A-Maze-ing

## Description

A-Maze-ing is a Python project that generates a seed-based maze on a rectangular
grid, embeds a hidden "42" pattern of permanently closed cells somewhere in the
middle of it, and computes a valid path from an entry cell to an exit cell. The
maze can be generated in two modes:

- **PERFECT=True**: a perfect maze, with exactly one path between entry and exit
  (no loops).
- **PERFECT=False** (default): a Pac-Man style playable board, fully connected,
  with loops so a chased player always has an alternative route, and dead ends
  kept rare.

The generated maze is written to a text file (hexadecimal wall encoding) and
displayed in a graphical window using the MiniLibX (MLX) library.

## Instructions

### Installation

```
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install mlx-2_2-py3-none-any.whl
```

`make` (or `make install`) does this automatically.

### Execution

python3 a_maze_ing.py config.txt

or

make run


`config.txt` is the only argument, and can be replaced by any other config file
path. Errors (missing file, bad syntax, invalid dimensions, entry/exit outside
the grid or on the same cell, etc.) are reported with a clear message and the
program exits without crashing.

Once the window is open:

1   | Re-generate a new maze        
2   | Show / hide the shortest path 
3   | Change the wall colours       
4/ESC | Quit                          

Closing the window also quits cleanly.

### Makefile targets

- make install : create the virtual environment and install dependencies
- make run     : run the project (`ARGS="config.txt"` to override the config file)
- make debug   : run the project under `pdb`
- make lint    : run `flake8` and `mypy`
- make clean   : remove caches and stop any hanging window process
- make fclean  : remove the virtual environment too
- make re      : `fclean` + `install`

## Config File Format

One `KEY=VALUE` pair per line. Lines starting with `#` are ignored.

| Key         | Description                        | Example            |
|-------------|-------------------------------------|---------------------|
| WIDTH       | Maze width in cells                 | WIDTH=20            |
| HEIGHT      | Maze height in cells                | HEIGHT=15           |
| ENTRY       | Entry coordinates (x,y)             | ENTRY=0,0           |
| EXIT        | Exit coordinates (x,y)              | EXIT=19,14          |
| OUTPUT_FILE | Output filename                     | OUTPUT_FILE=maze.txt|
| PERFECT     | Perfect maze or Pac-Man board       | PERFECT=True        |
| SEED        | Optional, integer, reproducibility  | SEED=42             |

Minimum size is WIDTH >= 9 and HEIGHT >= 7, so the "42" pattern always fits.

## Maze Generation Algorithm

**Depth-First Search (recursive backtracker)**: starting from the entry cell,
the algorithm marks the current cell as visited, picks a random unvisited
neighbour, knocks down the wall between them, and moves into it, pushing every
step onto a history stack. When a cell has no unvisited neighbour left, the
algorithm backtracks by popping the stack until it finds a cell with an
unexplored side. The traversal ends once the stack is empty, which produces a
spanning tree that touches every reachable cell exactly once: a perfect maze.

For `PERFECT=False`, extra walls are then knocked down between remaining
dead-end cells and one of their neighbours, which introduces loops (so the
board is no longer a tree) while checking that no 3x3 block of cells ends up
fully open, to respect the maximum corridor width rule.

### Why DFS?

DFS with a stack is simple to implement and to reason about, it naturally
guarantees full connectivity (every cell is reachable) with zero loops, it
produces long, winding corridors well suited to a maze, and it is easy to seed
for reproducibility since the only randomness is `random.choice()` picking the
next neighbour.

## Code Reusability

The maze generation and solving logic lives in a single standalone module,
`mazegen.py`, with no dependency on MLX or on any other project file. It
exposes one class, `MazeGenerator`.

This module is packaged as `mazegen-1.0.0-py3-none-any.whl` at the root of the
repository, built from `mazegen.py` and `pyproject.toml`. To rebuild it:

python3 -m venv build_env
build_env/bin/pip install --upgrade pip build
build_env/bin/python -m build --wheel

The main project (`a_maze_ing.py`, `gen_maze.py`, `solve_maze.py`,
`mlx_view.py`) is a separate, thin layer on top of it: config parsing, output
file writing, and the MLX display.

## Resources

- MLX documentation (bundled `.3` man pages inside the provided wheel)
- Wikipedia: [Maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- Python `ctypes` documentation, used by the MLX Python wrapper
- Python packaging user guide, for building the `mazegen` wheel

### AI usage

AI (Claude & Gemini) were used to:
- Debug the code
- Understand algorithm logic and implementation
- Understand Mlx graphic library documentation

## Team and Project Management

- **Roles**: <describe who worked on generation, on the solver/display, on
  packaging/docs>
- **Planning**: <describe how the work was split and how the plan evolved>
- **What worked well / what could be improved**: <fill in>
- **Tools used**: Python 3, MiniLibX (MLX), flake8, mypy, git

## Licensing

This project is distributed under the MIT license, see `LICENSE.md`.
