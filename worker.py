from tile import Tile


class Worker:
    def __init__(self, letter='', tile=None, row_pos=None, col_pos=None):
        self.letter = letter
        self._tile = tile
        self.row = row_pos
        self.col = col_pos
    
    def get_level(self):
        return self._tile.get_level()
    
        