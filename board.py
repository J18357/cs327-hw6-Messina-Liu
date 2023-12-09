from tile import Tile
from player import Player

class Board:
    def __init__(self, players=None):

        # initializing the tiles
        self.tiles = []
        for i in range(5):
            row = []
            for j in range(5):
                is_worker = False
                # add the workers to each tile
                for player in players:
                    for worker in player.workers:
                        if [i,j] == worker.get_position():
                            row.append(Tile(worker))
                            is_worker = True
                if is_worker == False:
                    row.append(Tile())
            self.tiles.append(row)

    
    def check_neighbors(self, x_pos, y_pos, worker_level, dir_type, dir):
        return_val = False
        # matrix
        for i in range(x_pos-1, x_pos+1):
            for j in range(y_pos-1, y_pos+1):
                if (j >= 0) and (j <= 5) and (i >= 0) and (i <= 5) and (i != x_pos) and (j != y_pos):
                    neighbor_tile = self.tiles[i][j]
                    # check space does not have a worker or dome (level 4)
                    check_1 = not neighbor_tile.has_workerDome()
                    # check valid level move
                    check_2 = neighbor_tile._get_level()

    def board_display(self):
        for i in range(5):
            print("+--+--+--+--+--+")
            for j in range(5):
                print(f"|{self.tiles[i][j].level}",end='')

                # if there is a worker on the tile or not
                if self.tiles[i][j].get_worker():
                    print(f"{self.tiles[i][j].get_worker().get_letter()}", end="")
                else:
                    print(' ', end="")
            print("|")
        print("+--+--+--+--+--+")


                        
                
        

    