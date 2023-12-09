# from tile import Tile

class Worker:
    def __init__(self, letter='', row_pos=None, col_pos=None):
        self.letter = letter
        self.row = row_pos
        self.col = col_pos

    # WILL change
    # def get_level(self):
    #     return self._tile.get_level()
    
    def __str__(self):
        return f"letter: {self.letter}, position: ({self.row}, {self.col})"
    
    def get_letter(self):
        """returns the letter of the given worker"""
        return self.letter
    
    def get_position(self):
        """returns the position of the worker as [row, col]"""
        return [self.row, self.col]
        