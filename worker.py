


class Worker:
    def __init__(self, letter=' ', x_pos=None, y_pos=None):
        self.letter = letter
        self.x = x_pos
        self.y = y_pos

    def __str__(self):
        return f"letter: {self.letter}, position: ({self.x}, {self.y})"
    
    def get_letter(self):
        """returns the letter of the given worker"""
        return self.letter
    
    def get_position(self):
        """returns the position of the worker as [x,y]"""
        return [self.x, self.y]
        