"""
Main program file that takes the config file as single argument to create the
maze and handle any config errors with clear output
config parser and game wrapper

importying sys and modules genmaze, solver

define a pydantic config class:
    widht: greater or qual to 5, less or queal to 100
    height: same
    entry_x:
    entry_y
    exit_x
    exit_y
    output_file:str
    perfect: bool = True default
    algo: str dfs or bfs

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
        if key matches entry or exit positions
            split value segment by, to parse indifiviual x and y 
        pass param dict to Config pidtantic schema
    return evaluated clean config schema object

def write_output_file(path:, hex_rows: list, entry: tuple, exit: tuple, path_strings: str) -> None
    open path using with open
    for each row_string inside hex_rows:
    write row_string out followed by /n
    write explcit blank separators
    write formatted line {entry[[0]. {entry[1]} # entry(x,y)
    write line {path_string}


define MLXGraphicEgine controlller class:
    on init matrox, soltion path:
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
        
        if self.show_soution_path is Truw:
            loop each stepcoord element in the soution path array list
                calc path canvas position path_x = step_coord.col * tile size, path_y = stp_coord.row * tile_size
                draw special coloured route path sqate indicator sprite at path_x, path_y
        flush update frame buffer laout to window screen disply engine


define main:
    validate sysargv lengh is 2 params
    if len incorrect print error and instructions
    try exec pipeline:
        rawparams= call parse_config(sys.argv[1])
        clean_config = pass rawparas to pydantic config
        generateor = instantiate MazeGenerator(configdata.widh. condigdata.height, configdata.perfect)
        grid= generator.generate()
        hexrows = genereator.serialize_to_hex_rows()
        start point = (cleanconfig.entry_x, Cleanconfig.entry_y)
        end point = (cleanconfig.exit_x, Cleanconfig.exit_y)
        coorroute= call pathfinder_solver.solve_maze(grid, startcoord, endcordm cleanconfig.algorithm)
        letterpathstring = pathfinder_solver.convert_coordinate_to_letter(coordinatesroute)
        call write_output_file(cleanconfig.output-file, hexrows, startcoord, endcoord, letterpathstring)
        gamewindow = instantiiat mlxgraphicalengin(inalmatrix, finalpath)
        gamewindow.laumuchgame_loop()

    catch file, parsing or validation as error;
        print error descipt text stream to consolee
        exit(1)


if __name__ == "__main__"

"""

