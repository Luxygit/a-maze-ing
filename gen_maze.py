"""
Handling cell flags, 2d arrays and board gen.
Must be packagable into a distrib package.


defining Cell class:
    properties:
        x, y, visited default to false, walls int 4-bit bitmask init to 15
        binary 1111 means all walls are closed

defining a MazeGenerator class:
    init (width, height, perfect seed=None)
        store args
        init random seed state if provided
        initiaise 2d array matrix with Cell objects
        defining bitmask North=1 east=2 South =4 West=8

    method:  get_unvisited_neighbours(cell: Cell) -> list(tuple[str: Cell):
        init empty enighbours llist array
        check alll 4 adjacent directions
        if neighbour coor exists in bounds and candiidate.visited is false:
            append tracking pair cell to choices array
        return neighbours  array
    
    method: remove_shared_wall(cell_current, cell_neihbour, direction:str) :
        if dir is NORTH:
            substract north from cell_current.walls bitmask
            substract south from cell_neighb.walls bitmask
        apply the same for east south and west

    method: generate() -> list[list[Cell]]:
        init history stack as empty list 
        pick starting cell, set visited=true, push to historystack
        while historystack is not empty:
            current  = top item of history stack
            valid_options = call get_univisitedneighbouts(current)
            if valod options is not empty:
                pick random choice direction neighor cell from list
                set chosem_cell_visited = true
                push chosen_cell t to histort stack
            else
                pop top item off hisorty stack (backtrack)

    method: apply_pacman() -> None:
        #rule1 corners are open
        define corner_tples = [(0,0), (width-1,0), (0, height-1), (width-1,height-1)]
        foor each (cx, cy) in corner_tuples:
            force open at least one inner wall by sustracting it from the bitmask

        #rule2 ensure center area loop space is clear
        calc center_x= width//2, center_y= height//2
        for x from center_x -1 to center_x + 1:
         for y from center_y - 1 to center_1 + 1:
            destroy inner walls between center cells 

        #rule3 destroy dead-ends
        for each cell in matrix:
            count activate ramining walls by checking bitwise boundaries
            if cell has 3 walls active
                pick a random closed dir that doesnt blow past map borders
                fetch cell sittin behind that wall side
                call remove_wall(current_cell, neighbout_cell, chosen_dir)
    
    methd: fforce_forty_two -> None::
        if width < 15 or height < 15:
            print warning
            return
        calc center offset coords
        for specific coord array set mapping out a 4 and 2 block shape:
            force cell.walls to fully closed
    
    method execute_gen() -> list[lis[Cell]]:
        call generate()
        if perfect flag isTrue:
            call force_forty_two()
        else:
            cal apply_pacman()
        return self.matrix

    method: export to hex strings () -> list[str]:
        inti empty rows string list
        for each row in matrix:
            inti current ro string = ""
            for each cell in current_row:
                convert cell.walls int to uppercase hex
                append hex to current-row_string
            append cuurent row string to rowsstring list
        return rows string list

