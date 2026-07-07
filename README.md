*This project has been created as part of the 42 curriculum by jboan-gu, dievarga*

Description
- A_maze_ing is a project written in Python for which typical knowledge of the language is used, such as validation, file/error handling and bitmasking, with the specific goals of creating a seed-based maze and algorithmically finding the path from the start to the exit with interface user interactivity.

Instructions
- Compilation:
- Installatin: Installing the local pre-built .whl (wheel) file directly injects specialized compilation packages straight into our virtual environment without relying on external network assets. pip install mlx-2.2-py3-none-any.whl
- Execution:

Resources
- MLX documentation
- AI

Config File (struct and format)
- 

Maze Generation Algorithm
- DFS: Spanning Tree: a graph that connects every single node exactly once, creating zero loops and zero isolated islands. Depth-First Search achieves this using a History Stack (Last-In, First-Out) to systematically dig through corridors. The algorithm selects a node, marks it as visited, and picks a random unvisited neighbor. It destroys the shared bitmask wall separating them and jumps to that neighbor. It repeats this, digging deeper and deeper into the grid. Dead Ends: Eventually, the algorithm will dive into a corner where all adjacent neighbors have already been visited. The Backtrack Execution: Instead of stalling, the algorithm looks at the top of its history stack, it pops the current dead-end cell off the array stack, effectively reversing its steps to look at the previous cell. It checks if that cell has any alternative unvisited neighbors. If it doesn't, it pops again, tracing backward until it finds an intersection with unexplored paths, resuming the deep push. Once the history stack pops all the way back to the absolute starting node and finds no remaining unvisited paths anywhere, the stack empties to [] and the loop terminates. Every cell has been connected, and the spanning tree is complete.

Why DFS?
- 

What part of the code is reusable? How?
- Maze generator: instantiating and using the generator, pass custom parameters(size, seed), access the structure and at least a solution. via pip. name mazegen-*.whl 

Team and project management
- Roles:
- Planning:
- What works and improvements:

Display Output
- MlX lib: It functions as a window interface that translates Python arrays into visual pixel points. It launches an infinite loop at the display refresh rate. The Render Hook Callback in the initialization method is the rendering function executed over and over in the background. The image frame buffer system saves partial frames in the RAM and only flushes/syncs at the end of the frame routine. It also handles Keyboard interrupt with event loop hooks.

Licensing
- 






