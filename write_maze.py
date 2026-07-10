import os


class MazeWriter:
    def __init__(self, generator, solver, output_filename: str) -> None:
        self.generator = generator
        self.solver = solver
        self.output_filename = output_filename

    def _convert_path_to_letters(self) -> str:
        path = self.solver.solution_path
        if not path or len(path) < 2:
            return ""

        path_letters = []
        for i in range(len(path) - 1):
            cx, cy = path[i]
            nx, ny = path[i + 1]

            if ny < cy:
                path_letters.append("N")
            elif nx > cx:
                path_letters.append("E")
            elif ny > cy:
                path_letters.append("S")
            elif nx < cx:
                path_letters.append("W")

        return "".join(path_letters)

    def write_to_file(self) -> bool:
        try:
            with open(self.output_filename, "w") as file:
                for y in range(self.generator.height):
                    row_hex = []
                    for x in range(self.generator.width):
                        if (x, y) in self.generator.blocked_cells:
                            row_hex.append("f")
                        else:
                            cell_val = self.generator.grid[y][x].walls
                            row_hex.append(f"{cell_val:x}")
                    file.write("".join(row_hex) + "\n")
                file.write("\n")

                en_x, en_y = self.generator.entry_coord
                ex_x, ex_y = self.generator.exit_coord
                file.write(f"{en_x},{en_y}\n")
                file.write(f"{ex_x},{ex_y}\n")

                directional_path = self._convert_path_to_letters()
                file.write(f"{directional_path}\n")

            print(f"Successfully saved compliant maze blueprints layouto: {self.output_filename}")
            return True

        except Exception as exc:
            print(f"Error: Failed to write out to target file output context. {exc}")
            return False
