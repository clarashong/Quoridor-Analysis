from Player import Player
import random

class Board: 
    """
    The Board class is a place for players and walls to be located. 
    
    Attributes
    ----------
    grid: str[][] 
        grid with the game setup, player location, wall locations 
    bottom_row: int[][]
        coordinates for the bottom row of the board
    top_row: int[][]
        coordinates for the top row of the board
    p1_loc: int[] 
        coordinates of player 1
    p2_loc: int[]
        coordinates of player 2

    """
    
    def __init__(self):
        self.side = 18
        self.grid = [[None]*self.side]*self.side
        self.bottom_row = self.get_col_coords(17).copy()
        self.top_row = self.get_col_coords(1).copy()

        self.p1 = Player(1)
        self.p2 = Player(2) 
        self.p1_loc = [None, None]
        self.p2_loc = [None, None] 
        
    def takeTurn(self, turn): 
        if (turn <= 2): 
            self.update_start(turn)


    def update_board(self, turn, old_pos, new_pos): 
        self.grid[old_pos[0]][old_pos[1]] = None # clear the previous space
        if (turn % 2 == 1): 
            # player 1's turn
            self.grid[new_pos[0]][new_pos[1]] = "P1"
        else: 
            # player 2's turn
            self.grid[new_pos[0]][new_pos[1]] = "P2"

    def update_start(self, turn): 
        if (turn == 1): 
            old = p1_loc.copy()
            p1_loc = random.choice(self.bottom_row)
            self.update_board(self, turn, old, p1_loc)
        else: 
            old = p2_loc.copy()
            p2_loc = random.choice(self.top_row)
        self.update_board(self, turn, old, p2_loc)

    def get_col_coords(self, row): 
        arr = []
        for i in range(self.side): 
            if (i % 2 == 1): 
                arr.append([row, i])
        return arr

    def get_bottom_row(self): 
        return self.bottom_row
    
    def get_top_row(self): 
        return self.top_row


