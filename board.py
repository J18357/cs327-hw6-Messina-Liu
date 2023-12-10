from tile import Tile
# from player import Player

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

    def inc_tile_level(self, row, col):
        self.tiles[row][col].level += 1

    def update(self, prev_pos, worker):
        self.tiles[prev_pos[0]][prev_pos[1]].worker = None
        curr_pos = worker.get_position()
        self.tiles[curr_pos[0]][curr_pos[1]].worker = worker
