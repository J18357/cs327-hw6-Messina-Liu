from worker import Worker

class Tile:
    def __init__(self, worker=None):
        self.worker = worker
        self.level = 0
    
    def has_worker(self):
        return not self.worker is None
    
    def get_worker(self):
        return self.worker
    
    def get_level(self):
        return self.level
        