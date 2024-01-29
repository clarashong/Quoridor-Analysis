from Player import Player
from GameSystem import Board, print_lst
import random
import csv

log_name = "quoridor_log_rowcol.csv"
log_fields = ["game id", "turn number", "player", "move type", "row", "column"]

win_name = "winner_log_rowcol.csv"
winner_fields = ["game id", "turn number", "player", "row", "column"]

# write the headers for both files

with open(log_name, "w") as file: 
    writer = csv.DictWriter(file, fieldnames=log_fields)
    writer.writeheader()

with open(win_name, "w") as file: 
    writer = csv.DictWriter(file, fieldnames=winner_fields)
    writer.writeheader()

# write the game data into the files
with open(log_name, "a") as file:
    writer = csv.DictWriter(file, fieldnames=log_fields)
    
    for i in range(200):
        # play the game
        board = Board(i)
        board.playGame() 

        # get information from the board
        log_dict = board.get_game_log()
        win_dict = board.get_win_entry()

        writer.writerows(log_dict)

        with open(win_name, "a") as file_w:
            writer_w = csv.DictWriter(file_w, fieldnames=winner_fields)
            writer_w.writerows(win_dict)

