from worker import Worker


class Player:
    def __init__(self):
        self.workers = [Worker()]


    def _initialize_workers(self):
        self.tiles[1][1].worker = Worker("Y", 1, 1)
        self.tiles[1][3].worker = Worker("B", 1, 3)
        self.tiles[3][1].worker = Worker("A", 3, 1)
        self.tiles[3][3].worker = Worker("Z", 3, 1)
        

