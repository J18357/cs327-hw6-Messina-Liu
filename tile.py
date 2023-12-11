from worker import Worker

class Tile:
    def __init__(self, worker=None):
        self.worker = worker
        self.level = 0
    
    def has_worker(self):
        """returns false if tile.worker is None, otherwise True"""
        return not self.worker is None
    
    def get_worker(self):
        """returns the worker on the tile"""
        return self.worker
    
    def get_level(self):
        """returns the level of the tile"""
        return self.level
    
    def set_worker(self, worker=None):
        """sets the worker on the tile"""
        self.worker = worker

    def incr_level(self):
        """increases the level of the tile by 1"""
        self.level = self.level + 1
        