from tile import Tile

class Board:
    def __init__(self):

        # initializing the tiles
        self.tiles = []
        for i in range(5):
            row = []
            for j in range(5):
                row.append(Tile())
            self.tiles.append(row)
    
    def update_tile(self, tilePos, worker=None):
        tile_to_update = self.tiles[tilePos[0]][tilePos[1]]
        tile_to_update.set_worker(worker)
    
    def update_tile_build(self, tilePos):
        tile_to_build = self.tiles[tilePos[0]][tilePos[1]]
        tile_to_build.incr_level()

    def get_otherPlayer_positions(self, worker1_pos, worker2_pos):
        otherPlayer_pos_lst = []
        for i in range(5):
            for j in range(5):
                if self.tiles[i][j].has_worker() and [i,j] != worker1_pos and [i,j] != worker2_pos:
                    otherPlayer_pos_lst.append([i,j])                
        return otherPlayer_pos_lst
        