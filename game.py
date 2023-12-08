from board import Board
from player import Player, HumanPlayer
from tile import Tile
from exceptions import InvalidDirectionError

class Game:
    def __init__(self):
         self._board = Board()
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