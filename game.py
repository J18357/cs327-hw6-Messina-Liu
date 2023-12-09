from board import Board
from tile import Tile
from exceptions import InvalidDirectionError

class Game:
    def __init__(self):
        # initialize the players within the board
        # self.players = [Player(1), Player(2)]
        self._board = Board(self.players)
        self.direction_dict = {"n":(-1,0), "ne":(-1,1), "e":(0,1), "se":(1,1), "s":(1,0), "sw":(1,-1), "w":(0,-1), "nw":(-1,-1)}
    
    # TODO: revise to pass in worker
    def check_move_dir(self, selectedWorker, dir_type, dir):
        input_dir = self.direction_dict[dir] # a tuple
        workerPosition = selectedWorker.get_position()
        move_row = workerPosition[0] + input_dir[0]
        move_col = workerPosition[1] + input_dir[1]

        # check still in board
        if (move_row < 0 or move_row > 5) or (move_col < 0 or move_col > 5):
            return False
        else:
            neighbor_tile = self._board.tiles[move_row][move_col]

            # check space does not have a worker or dome (level 4)
            # TODO: check encapsulation of Tile from Game
            if neighbor_tile.has_worker() or neighbor_tile.get_level() == 4:
                return False
            if (dir_type == "move") and (neighbor_tile.get_level() > self.get_tile_level(workerPosition) + 1):
                return False
        return True
    
    # def get_all_workers(self):
    #     """returns all workers [p1_worker1, p1_worker2, p2_worker1, p2_worker2]"""
    #     all_workers = []
    #     for worker in self.players[0].get_workers():
    #         all_workers.append(worker)
    #     for worker in self.players[1].get_workers():
    #         all_workers.append(worker)
    #     return all_workers
    

    def display_player(self, player):
        # displays player 1 or 2
        if player == 1:
            return f"white ({self.players[0].get_workers()[0].get_letter()}{self.players[0].get_workers()[1].get_letter()})"
        else:
            return f"blue ({self.players[1].get_workers()[0].get_letter()}{self.players[1].get_workers()[1].get_letter()})"
        
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
        
    # TODO: in cli.py under display menu
    def display_score(self):
        print()

    def display_board(self):

        self._board.board_display()
