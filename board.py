from tile import Tile
from exceptions import InvalidDirectionError
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
        # self._initialize_workers()
        self.direction_dict = {"n":(-1,0), "ne":(-1,1), "e":(0,1), "se":(1,1), "s":(1,0), "sw":(1,-1), "w":(0,-1), "nw":(-1,-1)}

    def check_move_dir(self, row_pos, col_pos, worker_level, dir_type, dir):
        input_dir = self.direction_dict[dir] # a tuple
        move_row = row_pos + input_dir[0]
        move_col = col_pos + input_dir[1]
        # check still in board
        if (move_row < 0 or move_row > 5) or (move_col < 0 or move_col > 5):
            # may revise later to re-use in enumerate moves method
            raise InvalidDirectionError(dir, dir_type)
        else:
            neighbor_tile = self.tiles[move_row][move_col]
            if neighbor_tile.has_worker() or neighbor_tile.get_level() == 4:
                raise InvalidDirectionError(dir, dir_type)
            if (dir_type == "move") and (neighbor_tile.get_level() > worker_level + 1):
                raise InvalidDirectionError(dir, dir_type)
        return True

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

                    
                        
                
        

    