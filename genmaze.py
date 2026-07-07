"""
maze gen/trnaformations and hexadecimal bitmasking
"""

"""
defining Cell class:
    properties: x, y, visited, walls

defining a GenMaze class:
    init (width, height, perfect)
        store args
        initiaise 2d array matrix with Cell objects
        defining bitmask North=1 east=2 South =4 West=8
        define dict for opposite sides N-S E-W

    get_unvisited_neighbours(cell: Cell) -> list(cell):
        init empty choice array
        check cell bounds in 4 direstcions(y-1, x+1, y+1, x-1)
        if adjacest cordinates exists in bounds and neighbour.visited is false:
            append neighbou cell to choices array
        return choices array
    
    method: remove_shared_wall(cell_a, cell_b) :
        determine relative alignment between cella cellb
        if cellb is north of cella (cellb.y == cella.y - 1):
            substract north from cell a.walls bitmask
            substract south from cellb.walls bitmask
        if cellb is east of cella (cellb.x == cella.x + 1):
            substract east from cella.walls bitmask
            substarct west from cellb.walls bitmask
    
    method: generate() list:
        init history stack as empty list
        pick starting cell, set visited=true, push to historystack
        while historystack is not empty:
            currentcell = top item of history stack
            neighbours = call getunivisitedneighbouts(currentcell)
            if neighbouts list is not empty:
                chosenneighbout = select a random element from neighbours
                removesharedwall(currentcell, chosen neighbour)
                set chosenneighbour.visited = true
                push chosenneighbout to histort stack
            else
                pop top item off hisorty stack (backtrack)
        if flag is false:
            loop every cell
                count how many walls are up bitwise compare
                if cell has 3 walls deadend:
                    pick a random closed wall
                    find neiighbour behind that wall
                    remove shared walls with remove shared wall
        return 2d matrix

    method: export to hex strings () -> list[str]:
        inti empty rows string list
        for each row in matrix:
            inti current ro string = ""
            for each cell in current_row:
                convert cell.walls int to uppercase hex
                append hex to current-row_string
            append cuurent row string to rowsstring list
        return rows string list

