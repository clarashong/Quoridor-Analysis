import random
class Player: 
    """
    Attributes
    ----------
    type: (Anyof 1, 2)
        Whether the player is player 1 (bottom) or player 2 (top)
    move: str
        The type of turn the player will take
    wall_storage: int
        The number of walls left to use
    location: int[]
        player's coordinates
    
    Methods
    -------
    gen_start(): 
        generates and returns starting position of player
    pick_move():
        randomly chooses and returns move for player
    """

    def __init__(self, type):
        self.type = type
        self.wall_storage = 10
        self.move = self.pick_move()
        self.location = []
        
    def gen_start(self): 
        """"
        generates and returns starting position of player
        """
        if (self.type == 1): 
            start_pos = random.choice(self.board.get_bottom_row())
        else: 
            start_pos = random.choice(self.board.get_top_row())
        return start_pos

    def pick_move(self): 
        """
        randomly chooses and returns move for player
        """
        if (self.wall_storage <= 0): 
            self.move = "pawn"
        else: 
            self.move = random.choice(["pawn", "h_wall", "v_wall"])
        return self.move
    
    def set_location(self, new_loc): 
        self.location = new_loc

    def get_type(self): 
        return self.type

    def get_location(self): 
        return self.location

    def get_move(self): 
        self.pick_move
        return self.move
    
    def use_wall(self): 
        self.wall_storage -= 1



