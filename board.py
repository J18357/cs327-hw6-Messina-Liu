from tile import Tile
from player import Player

class Board:
    def __init__(self):

        # initializing the tiles
        self.tiles = []
        for i in range(5):
            row = []
            for j in range(5):
                row.append(Tile())
            self.tiles.append(row)
        # initialize the players within the board
        # self.players = [Player(1), Player(2)]

    def get_all_workers(self):
        """returns all workers [p1_worker1, p1_worker2, p2_worker1, p2_worker2]"""
        all_workers = []
        for worker in self.players[0].get_workers():
            all_workers.append(worker)
        for worker in self.players[1].get_workers():
            all_workers.append(worker)
        return all_workers
    def display_player(self, player):
        # displays player 1 or 2
        if player == 1:
            return f"white ({self.players[0].get_workers()[0].get_letter()}{self.players[0].get_workers()[1].get_letter()})"
        else:
            return f"blue ({self.players[1].get_workers()[0].get_letter()}{self.players[1].get_workers()[1].get_letter()})"

    # TODO: in cli.py under display menu
    def display_score(self):
        print()

    def is_valid_worker(self, player, worker):
        if player == 1:
            if self.players[0].is_players_worker(worker):
                return True
            if self.players[1].is_players_worker(worker):
                print("That is not your worker")
                return False
        else:
            if self.players[1].is_players_worker(worker):
                return True
            if self.players[0].is_players_worker(worker):
                print("That is not your worker")
                return False
        print("Not a valid worker")
        return False
    
    def check_neighbors(self, x_pos, y_pos, worker_level, dir_type, dir):
        pass

                    
                        
                
        

    