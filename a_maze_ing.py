"""
main engine of the project, imports all the modules as a whole.
"""

import sys
import os
import random
import gen_maze
import solve_maze
import mlx_view
from typing import Any


class AMazeIng:
    """main class managing the whole execution"""
    def __init__(self) -> None:
        """initialising state params to default fallbacks"""
        self.width = 0
        self.height = 0
        self.seed = 42
        self.perfect = True
        self.entry_coord = (0, 0)
        self.exit_coord = (0, 0)
        self.output_file = "maze.txt"
        self.view: Any = None

    def parse_config_file(self) -> bool:
        """validating and getting config settings from a file"""
        if len(sys.argv) != 2:
            print("Usage: python3 a_maze_ing.py <config_file.txt>")
            return False
        config_path = sys.argv[1]
        if not os.path.exists(config_path):
            print(f"Error: Configuration file {config_path} not found.")
            return False
        config_data = {}
        try:
            with open(config_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        print(f"Error: Invalid config on line: '{line}'")
                        return False
                    key, value = line.split("=", 1)
                    config_data[key.strip().upper()] = value.strip()
        except Exception as exc:
            print(f"Error reading config file: {exc}")
            return False

        mandatory_keys = [
                "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
        for key in mandatory_keys:
            if key not in config_data:
                print(f"Error: Missing mandatory configuration key '{key}'.")
                return False
        try:
            self.width = int(config_data["WIDTH"])
            self.height = int(config_data["HEIGHT"])
            self.output_file = config_data["OUTPUT_FILE"]
            en_x, en_y = map(int, config_data["ENTRY"].split(","))
            ex_x, ex_y = map(int, config_data["EXIT"].split(","))
            self.entry_coord = (en_x, en_y)
            self.exit_coord = (ex_x, ex_y)
            perfect_str = config_data["PERFECT"].lower()
            if perfect_str in ("true", "1"):
                self.perfect = True
            elif perfect_str in ("false", "0"):
                self.perfect = False
            else:
                print("Error: PERFECT flag must be 'True' or 'False'.")
                return False
            if "SEED" in config_data:
                self.seed = int(config_data["SEED"])
                if not (0 <= self.seed <= 2147483647):
                    print("Error: Seed must be a postiive int")
                    return False
        except ValueError:
            print("Error: Invalid configuration.")
            return False
        if not (4 <= self.width <= 80) or not (4 <= self.height <= 80):
            print("Error: Dimensions should be between 4x4 and 80x80")
            return False
        if not (0 <= en_x < self.width and 0 <= en_y < self.height):
            print("Error: ENTRY coordinates are outside the maze bounds.")
            return False
        if self.entry_coord == self.exit_coord:
            print("Error: Entry and Exit cannot be identical")
            return False
        if not (0 <= ex_x < self.width and 0 <= ex_y < self.height):
            print("Error: EXIT coordinates are outside the maze bounds.")
            return False
        if self.width < 9 or self.height < 7:
            print("Notice: Maze too small to fit the '42' pattern.")
        return True

    def regenerate_maze_callback(self) -> tuple[Any, Any]:
        """getting a new random seed and regenerating the maze accordingly"""
        self.seed = random.randint(1, 100000)
        print(f"Regenerating maze with random seed:{self.seed}")
        generator = gen_maze.MazeGenerator(
            self.width, self.height, self.entry_coord,
            self.exit_coord, self.seed, self.perfect
        )
        solver = solve_maze.MazeSolver(generator)
        return generator, solver

    def execute(self) -> None:
        """core execution and config validation"""
        if not self.parse_config_file():
            sys.exit(1)
        generator = gen_maze.MazeGenerator(
            self.width, self.height, self.entry_coord,
            self.exit_coord, self.seed, self.perfect
        )
        if not generator.config_valid:
            sys.exit(1)
        solver = solve_maze.MazeSolver(generator)
        # generating txt file with maze struct and solution
        import write_maze
        writer = write_maze.MazeWriter(generator, solver, self.output_file)
        writer.write_to_file()
        # passing everything to the graphic lib
        self.view = mlx_view.MlxView(
            generator, solver, regenerate_fn=self.regenerate_maze_callback)
        self.view.run()


def main() -> None:
    app = AMazeIng()
    app.execute()


if __name__ == "__main__":
    main()
