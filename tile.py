from worker import Worker

class Tile:
    def __init__(self, worker=None):
        self._worker = worker
        # self.x = x
        # self.y = y
        self._level = 0
    
    def has_worker(self):
        return not self._worker is None
    
    def get_level(self):
        return self._level
        