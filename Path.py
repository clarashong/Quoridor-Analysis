# test file for trying out the pathfinding algorithm

grid = [[None for i in range(17)] for j in range(17)]
start = (0,0)
end_row = 16
for i in range (17): 
    grid[14][i] = "W"

def check_spaces(loc, p_type):
        """
        returns a list of adjacent spaces the the player can move to
        """
        row = loc[0]
        col = loc[1]
        
        neighbours = []

        if (row > 1 and grid[row-1][col] == None): 
            neighbours.append((row-2, col)) # above
        if (row < 15 and grid[row+1][col] == None): 
            neighbours.append((row+2, col)) # below
        if (col > 1 and grid[row][col-1] == None): 
            neighbours.append((row, col-2)) # left
        if (col < 15 and grid[row][col+1] == None): 
            neighbours.append((row, col+2)) # right
        
        print("neighbours are " + str(neighbours))
        return neighbours


def search_paths(start, p_type): 
    print("pathfinding for player " + str(p_type))
    final_row = 0 if p_type == 1 else 16
    
    visited = set({}) 
    queue = [start]

    while (not (len(queue) == 0)):
        current_loc = queue[0]

        if (current_loc == final_row) :
            print("There is a valid path to " + str(current_loc))
            return True

        lst_neighbours = check_spaces(current_loc, p_type)
        for n in lst_neighbours: 
            if (n not in visited):
                queue.append(n)
                visited.add(n)
        queue.pop(0)
    return False

search_paths((0,0), 2)

