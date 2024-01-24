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
    game_id: int
        the game number
    game_log: str dict []
        log of all turns in the game
    win_entry: str dict []
        winner data entry
    """
    
    def __init__(self, game_id):
        self.side = 17
        self.grid = [[None for i in range(17)] for j in range(17)]

        self.wall_cols = [i*2 for i in range(7)]
        self.wall_rows = [i*2 for i in range(7)]

        self.p1 = Player(1)
        self.p2 = Player(2) 

        self.curr_player = self.p1
        self.finished = False
        self.turn = 1 

        self.game_id = game_id
        self.game_log = []
        self.win_entry = []
        
    def playGame(self):
        """
        Take turns until game is finished
        """
        while (not self.finished):
            self.takeTurn()
        # print_lst(self.grid)
        print("done game " + str(self.game_id))

    def takeTurn(self): 
        """
        Executes an in-game turn where the player moves or puts down a wall
        """

        self.curr_player = self.p1 if (self.turn % 2 == 1) else self.p2
        
        if (self.turn <= 2): 
            # first two moves are putting the players on the board
            self.update_start(self.curr_player)
            self.turn += 1
            return
        
        player = self.curr_player
        move = player.pick_move() # choose what move to do

        if (move == "pawn"): 
            location = self.move_pawn()
            self.update_board_pawn(player, player.get_location(), location)
            self.game_log.append(self.make_move_entry(player.get_type(), location))
        elif (move == "h_wall"): 
            self.put_h_wall() 
        else: 
            self.put_v_wall()
        self.turn += 1 # next turn

    def move_pawn(self): 
        """
        Produces the next spot for a pawn to move
        """
        curr = self.curr_player.get_location() 
        p_type = self.curr_player.get_type() 
        new = self.check_spaces(curr) 
        if (len(new) == 0): 
            return False
        else: 
            return random.choice(new)

    def check_spaces(self, loc):
        """
        Returns a list of adjacent spaces the the player can move to

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
            row = random.choice(valid_rows)   
            left_side = random.choice(self.wall_cols)

            if (self.grid[row][left_side] is None 
                and self.grid[row][left_side+1] is None
                and self.grid[row][left_side+2] is None): 
                validWall = True
                wall_coords = [(row, left_side), (row, left_side+1), (row, left_side+2)]

                if (self.can_place_wall(wall_coords)):
                    self.game_log.append(self.make_wall_entry("h wall", wall_coords, self.curr_player.get_type()))
                    return wall_coords
                else: 
                    validWall = False

    def put_v_wall(self): 
        """
        Returns coordinates of where a horizontal wall would go
        """

        validWall = False
        # valid columns that the wall can go
        valid_cols = [(i * 2) + 1 for i in range (int((self.side - 2) / 2))]
        while(not validWall): 
            # randomly choose column
            col = random.choice(valid_cols)   
            # the upper unit of the wall's placement
            upper = random.choice(self.wall_rows)  

            if (self.grid[upper][col] is None   
                and self.grid[upper+1][col] is None
                and self.grid[upper+2][col] is None): 
                # there is space for the wall
                validWall = True
                wall_coords = [(upper, col),(upper+1, col), (upper+2, col)]

                if (self.can_place_wall(wall_coords)): 
                    # add an entry to the log
                    self.game_log.append(self.make_wall_entry("v wall", wall_coords, self.curr_player.get_type()))
                    return wall_coords
                else: 
                    validWall = False

    def can_place_wall(self, coords):   
        """
        Returns true if the wall can be placed, 
        false otherwise (player is blocked from winning)
        """  

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
        """
        Updates a pawn's position on the board

        Parameters
        ----------
        player: Player
            the player that needs to be moved
        old_pos: int tuple
            the player's position before moving 
        new_pos: int tuple
            the desired new location for the player
        """

        name = "P1" if (player.get_type() == 1) else "P2"

        self.grid[old_pos[0]][old_pos[1]] = None # clear the previous space
        self.grid[new_pos[0]][new_pos[1]] = name
        self.curr_player.set_location(new_pos)  

        # win condition
        if (player.get_type() == 1 and new_pos[0] == 0): 
            self.finished = True
            self.set_win_entry(1, new_pos)
        elif (player.get_type() == 2 and new_pos[0] == 16): 
            self.finished = True
            self.set_win_entry(2, new_pos)
    
    def update_board_wall(self, wall_pos):
        """
        Updates the grid with wall placements
        """
        name = "W" + str(self.curr_player.get_type())
        for wall in wall_pos: 
            self.grid[wall[0]][wall[1]] = name

    def search_paths(self, start, p_type): 
        """
        Returns true if there is a valid path to the winning row of the board
        """

        final_row = 0 if p_type == 1 else 16
        visited = set({}) 
        queue = [start]
        while (not (len(queue) == 0)):
            current_loc = queue.pop(0)

            if (current_loc[0] == final_row) :
                return True

            lst_neighbours = self.check_spaces(current_loc)
            for n in lst_neighbours: 
                if (n not in visited):
                    queue.append(n)
                    visited.add(n)
        return False

    def update_start(self, player): 
        """
        Updates the board with players starting positions. 
        """
        row = 16 if player.get_type() == 1 else 0
        starting_loc = random.choice(self.get_col_coords(row))
        old = starting_loc.copy()
        player.set_location(starting_loc)

        self.update_board_pawn(player, old, starting_loc)
        self.game_log.append(self.make_move_entry(player.get_type(), starting_loc))

    def make_move_entry(self, p_type, location):
        """
        Makes an data entry of the player's move
        """
        dict = {"game id": self.game_id, 
                "turn number": self.turn,
                "player": p_type, 
                "move type": "pawn", 
                "row": location[0],
                "column": location[1]}
        return dict

    def make_wall_entry(self, wall_type, location, p_type): 
        """
        Makes data entry of a wall placement
        """

        dict = {"game id": self.game_id, 
                "turn number": self.turn,
                "player": p_type, 
                "move type": wall_type, 
                "row": location[0][0],
                "column": location[0][1]}
        return dict
        
    def set_win_entry(self, p_type, location): 
        dict = {"game id": self.game_id, 
                "turn number": self.turn,
                "player": p_type,
                "row": location[0], 
                "column": location[1]}
        self.win_entry = [dict]


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

    def get_finished(self):
        return self.finished
    
    def get_grid(self): 
        return self.grid

    def get_game_log(self): 
        return self.game_log
    
    def get_win_entry(self): 
        return self.win_entry

def main():
    board = Board(1)
    board.playGame()

if (__name__ == "__main__"): 
    main()