import random
class Player: 
    """
    Attributes
    ----------
    type: (Anyof 1, 2)
        Whether the player is player 1 (bottom) or player 2 (top)
    move: str
        The type of turn the player will take
    """

    def __init__(self, type):
        self.type = type
        self.move = self.pick_move()

    def gen_start(self): 
        if (self.type == 1): 
            start_pos = random.choice(self.board.get_bottom_row())
        else: 
            start_pos = random.choice(self.board.get_top_row())
        return start_pos

    def pick_move(self): 
        self.move = random.choice(["pawn", "h_wall", "v_wall"])
    
    def getMove(self): 
        return self.move


