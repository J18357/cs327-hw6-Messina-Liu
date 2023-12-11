class Worker:
    """two workers per player, each worker has a letter and its row and col"""
    
    def __init__(self, letter='', row_pos=None, col_pos=None):
        self.letter = letter
        self.row = row_pos
        self.col = col_pos
    
    def __str__(self):
        return f"letter: {self.letter}, position: ({self.row}, {self.col})"
    
    def get_letter(self):
        """returns the letter of the given worker"""
        return self.letter
    
    def get_position(self):
        """returns the position of the worker as [row, col]"""
        return [self.row, self.col]
    
    def step(self, new_row, new_col):
        self.row = new_row
        self.col = new_col