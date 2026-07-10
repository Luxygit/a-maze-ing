"""

"""

import sys
import os
import random
import gen_maze
import solve_maze
import mlx_view
from typing import Any

class AMazeIng:
	def __init__(self) -> None:
		self.width = 0
		self.height = 0
		self.seed = 42
		self.perfect = True
		self.entry_coord = (0, 0)
		self.exit_coord = (0, 0)
		self.output_file = "maze.txt"
		self.view = None

	def parse_config_file(self) -> (bool):
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
						print(f"Error: Invalid configuration syntax on line: '{line}'")
						return False
					key, value = line.split("=", 1)
					config_data[key.strip().upper()] = value.strip()         
		except Exception as exc:
			print(f"Error reading configuration file: {exc}")
			return False

		mandatory_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
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
				print("Error: PERFECT flag must be 'True', 'False', '1', or '0'.")
				return False
			if "SEED" in config_data:
				self.seed = int(config_data["SEED"])
		except ValueError:
			print("Error: Invalid numerical values or syntax inside configuration.")
			return False
		if self.width <= 0 or self.height <= 0:
			print("Error: Dimensions must be greater than 0.")
			return False
		if not (0 <= en_x < self.width and 0 <= en_y < self.height):
			print("Error: ENTRY coordinates are outside the maze bounds.")
			return False
		if not (0 <= ex_x < self.width and 0 <= ex_y < self.height):
			print("Error: EXIT coordinates are outside the maze bounds.")
			return False
		if self.width < 9 or self.height < 7:
			print("Notice: Dimensions too small to fit the hidden '42' pattern.")

		return True
	def regenerate_maze_callback(self) -> tuple[Any, Any]:
		self.seed = random.randint(1, 100000)
		print(f"Regenerating maze structure with fresh random seed context:{self.seed}")
		generator = gen_maze.MazeGenerator(
			self.width, self.height, self.entry_coord,
            self.exit_coord, self.seed, self.perfect
        )
		solver = solve_maze.MazeSolver(generator)
		return generator, solver

	def execute(self) -> None:
		#os.system("pkill -9 -f a_maze_ing.py > /dev/null 2>&1")
		if not self.parse_config_file():
			sys.exit(1)
		generator = gen_maze.MazeGenerator(
            self.width, self.height, self.entry_coord,
            self.exit_coord, self.seed, self.perfect
        )
		solver = solve_maze.MazeSolver(generator)
		import write_maze
		writer = write_maze.MazeWriter(generator, solver, self.output_file)
		writer.write_to_file()
		self.view = mlx_view.MlxView(
                generator, solver, regenerate_fn=self.regenerate_maze_callback)
		self.view.run()

def main() -> None:
    app = AMazeIng()
    app.execute()

if __name__ == "__main__":
    main()
