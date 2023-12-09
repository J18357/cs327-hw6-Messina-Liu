from tile import Tile
from player import Player

class Board:
    def __init__(self):

        # initializing the tiles
        self.tiles = []
        for i in range(5):
            row = []
            for j in range(5):
                row.append(Tile())
            self.tiles.append(row)
        # initialize the players within the board
        # self.players = [Player(1), Player(2)]
    
    def board_display(self):
        pass