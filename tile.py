from worker import Worker

class Tile:
    def __init__(self, worker=None):
        self.worker = worker
        self.level = 0

        