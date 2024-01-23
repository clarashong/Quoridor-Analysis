from Player import Player
import random

def print_lst(lst): 
    for i in lst: 
        print(i)
    print()

class Board: 
    """
    The Board class is a place for players and walls to be located. 
    
    Attributes
    ----------
    grid: str[][] 
        grid with the game setup, player location, wall locations 
    wall_cols: int[]
        list of indexes where walls can be placed 
    wall_cols: int[] 
        list of indexes where walls can be placed
    p1: Player
        player 1 (bottom player)
    p2: Player 
        player 2 (top player)
    curr_player: Player
        the current player for the current turn
    finished: bool
        whether the game is finished
    turn: int
        current turn number
    """
    
    def __init__(self):
        self.side = 17
        self.grid = [[None for i in range(17)] for j in range(17)]

        self.wall_cols = [i*2 for i in range(7)]
        self.wall_rows = [i*2 for i in range(7)]

        self.p1 = Player(1)
        self.p2 = Player(2) 

        self.curr_player = self.p1
        self.finished = False
        self.turn = 1


        
    def playGame(self):
        while (not self.finished):
            self.takeTurn()
            input()
            print_lst(self.grid)


    def takeTurn(self): 
        print("turn number " + str(self.turn))
        self.curr_player = self.p1 if (self.turn % 2 == 1) else self.p2
        
        if (self.turn <= 2): 
            self.update_start(self.curr_player)
            self.turn += 1
            return
        
        player = self.curr_player
        print("player " + str(player.get_type()) + " turn")
        print("generating move")

        move = player.pick_move() 
        print(move)

        if (move == "pawn"): 
            location = self.move_pawn()
            self.update_board_pawn(player, player.get_location(), location)
        elif (move == "h_wall"): 
            self.put_h_wall() 
        else: 
            self.put_v_wall()
        self.turn += 1


    def move_pawn(self): 
        """
        Produces the next spot for a pawn to move
        """
        curr = self.curr_player.get_location() 
        p_type = self.curr_player.get_type() 
        new = self.check_spaces(curr, p_type) 
        if (len(new) == 0): 
            return False
        else: 
            return random.choice(new)


    def check_spaces(self, loc):
        """
        returns a list of adjacent spaces the the player can move to

        Parameters
        ----------
        loc: tuple
            player's location

        Returns
        -------
        list of tuples: list of neighbour locations that the pawn can move to
        """
        row = self.get_x(loc)
        col = self.get_y(loc)
        
        neighbours = []

        if (row > 1 and self.grid[row-1][col] == None): 
            neighbours.append((row-2, col)) # above
        if (row < 16 and self.grid[row+1][col] == None): 
            neighbours.append((row+2, col)) # below
        if (col > 0 and self.grid[row][col-1] == None): 
            neighbours.append((row, col-2)) # left
        if (col < 16 and self.grid[row][col+1] == None): 
            neighbours.append((row, col+2))

        return neighbours


    def put_h_wall(self): 
        """
        Returns coordinates of where a horizontal wall would go
        """
        validWall = False
        valid_rows = [(i * 2) + 1 for i in range (int((self.side - 2) / 2))]
        while(not validWall): 
            print("h wall loop")
            row = random.choice(valid_rows)   
            left_side = random.choice(self.wall_cols)
            if (self.grid[row][left_side] is None 
                and self.grid[row][left_side+1] is None
                and self.grid[row][left_side+2] is None): 
                validWall = True
                wall_coords = [(row, left_side), (row, left_side+1), (row, left_side+2)]
                if (self.can_place_wall(wall_coords)):
                    print("valid wall!") 
                    return wall_coords
                else: 
                    validWall = False


    def put_v_wall(self): 
        validWall = False
        valid_cols = [(i * 2) + 1 for i in range (int((self.side - 2) / 2))]
        while(not validWall): 
            print("v wall loop")
            col = random.choice(valid_cols)   
            upper = random.choice(self.wall_rows)  
            if (self.grid[upper][col] is None 
                and self.grid[upper+1][col] is None
                and self.grid[upper+2][col] is None): 
                validWall = True
                wall_coords = [(upper, col),(upper+1, col), (upper+2, col)]
                if (self.can_place_wall(wall_coords)): 
                    print("valid wall!")
                    return wall_coords
                else: 
                    validWall = False


    def can_place_wall(self, coords):         
        print("can place wall?")
        self.update_board_wall(coords)
        player = self.p1 if (self.turn % 2 == 0) else self.p2
        if (self.search_paths(player.get_location(), player.get_type())):
            self.curr_player.use_wall()
            return True
        else:
            for c in coords: 
                self.grid[c[0]][c[1]] = None # reverse changes
            return False
        

    def update_board_pawn(self, player, old_pos, new_pos): 
        print("updating board pawn")
        name = "P1" if (player.get_type() == 1) else "P2"

        self.grid[old_pos[0]][old_pos[1]] = None # clear the previous space
        self.grid[new_pos[0]][new_pos[1]] = name  
        self.curr_player.set_location(new_pos)  

        print(name + " from " + str(old_pos) + " to " + str(new_pos))

        # win condition
        if (player.get_type() == 1 and new_pos[0] == 0): 
            self.finished = True
            print("game finished! player 1 won")
        elif (player.get_type() == 2 and new_pos[0] == 16): 
            self.finished = True
            print("game finished! player 2 won")
    

    def update_board_wall(self, wall_pos): 
        name = "W" + str(self.curr_player.get_type())
        for wall in wall_pos: 
            self.grid[wall[0]][wall[1]] = name
        print(name + " at " + str(wall_pos))


    def search_paths(self, start, p_type): 
        print("pathfinding for player " + str(p_type))
        final_row = 0 if p_type == 1 else 16
        
        visited = set({}) 
        queue = [start]

        while (not (len(queue) == 0)):
            current_loc = queue.pop(0)

            if (current_loc[0] == final_row) :
                print("There is a valid path to " + str(current_loc))
                return True

            lst_neighbours = self.check_spaces(current_loc, p_type)
            for n in lst_neighbours: 
                if (n not in visited):
                    queue.append(n)
                    visited.add(n)

        print("there is no path")
        return False


    def update_start(self, player): 
        """
        Updates the board with players starting positions. 
        """
        row = 16 if player.get_type() == 1 else 0
        starting_loc = random.choice(self.get_col_coords(row))

        print("generated coordinate " + str(starting_loc))
        old = starting_loc.copy()
        player.set_location(starting_loc)

        self.update_board_pawn(player, old, starting_loc)




    def get_col_coords(self, row): 
        arr = []
        for i in range(self.side): 
            if (i % 2 == 0): 
                arr.append([row, i])
        return arr

    def get_x(self, coord): 
        return coord[0]
    
    def get_y(self, coord): 
        return coord[1]

    def get_bottom_row(self): 
        return self.bottom_row
    
    def get_top_row(self): 
        return self.top_row
    
    def get_finished(self):
        return self.finished
    
    def get_grid(self): 
        return self.grid


def main():
    board = Board() 
    board.playGame()

if (__name__ == "__main__"): 
    main()