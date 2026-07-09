"""
Main program file that takes the config file as single argument to create the
maze and handle any config errors with clear output
config parser and game wrapper
"""
import sys
import os
import signal
import mlx
from typing import Any
#import modules genmaze, solver

try:
    import mlx
except ImportError:
    print("mlx library not found")
    sys.exit(1)


"""
define a pydantic config class:
    widht: greater or qual to 5, less or queal to 100
    height: same
    entry_x:
    entry_y
    exit_x
    exit_y
    output_file:str
    perfect: bool = True default

define parse_config_file(path:str) -> ConfigSchema:
    init a raw param storage dict
    open path using with open 
    for each raw line in file stream:
        strip white spaces
        if line is empty or starts with # skip
        partition string line around = token into key and value strings
        clean up spaces around key and value
        convert value into datatypes
        store mapping pair isnide a raw param dict
        unpack andd split values into separate vars entry_x entry_y
        if key matches entry or exit positions
            split value segment by, to parse indifiviual x and y 
        pass param dict to Config pidtantic schema
    return evaluated clean config schema object

def write_output_file(path:, hex_rows: list, entry: tuple, exit: tuple, path_strings: str) -> None
    open path using with open
    for each row_string inside hex_rows:
    write row_string out followed by /n
    write explcit blank separators
    write formatted line {entry[[0], {entry[1]} # entry(x,y)}
    write formatted line {exit[[0], {exit[1]} # exiitx,y)}
    write line {path_string}

 define main:
    try:
        validate sysargv lengh is 2 params
        if len incorrect print error and instructions
        try exec pipeline:
            rawparams= call parse_config(sys.argv[1])
            clean_config = pass rawparas to pydantic config
            generateor = instantiate MazeGenerator(configdata.widh. condigdata.height, configdata.perfect)
            grid= genmaze.generate()
            hexrows = generator.serialize_to_hex_rows()
            start point = (cleanconfig.entry_x, Cleanconfig.entry_y)
            end point = (cleanconfig.exit_x, Cleanconfig.exit_y)
            coordroute= call solver.solve_maze(grid, startcoord, endcordm cleanconfig.algorithm)
            letterpathstring = _solver.convert_coordinate_to_letter(coordinatesroute)
            call write_output_file(cleanconfig.output-file, hexrows, startcoord, endcoord, letterpathstring)
            gamewindow = instantiiat mlxgraphicalengin(inalmatrix, finalpath)
            gamewindow.laumuchgame_loop()

        catch file, parsing or validation as error;
            print error descipt text stream to consolee
            exit(1)
    except KeyboardInterrupt, EOFError:
        print("shutting down")
"""
def main() -> None:
    try:
        app = MLXGraphic()
        app.run()
    except KeyboardInterrupt:
        print("termination keyboard")


if __name__ == "__main__":
    main()


