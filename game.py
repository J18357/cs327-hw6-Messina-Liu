from board import Board
from player import Player, HumanPlayer
from tile import Tile
from exceptions import InvalidDirectionError

class Game:
    def __init__(self):
        # initialize the players within the board
        self.players = [Player(1), Player(2)]
        self._board = Board(self.players)
        self.direction_dict = {"n":(-1,0), "ne":(-1,1), "e":(0,1), "se":(1,1), "s":(1,0), "sw":(1,-1), "w":(0,-1), "nw":(-1,-1)}
    
    def check_move_dir(self, row_pos, col_pos, worker_level, dir_type, dir):
        input_dir = self.direction_dict[dir] # a tuple
        move_row = row_pos + input_dir[0]
        move_col = col_pos + input_dir[1]
        # check still in board
        if (move_row < 0 or move_row > 5) or (move_col < 0 or move_col > 5):
            # may revise later to re-use in enumerate moves method
            raise InvalidDirectionError(dir, dir_type)
        else:
            neighbor_tile = self.tiles[move_row][move_col]
            if neighbor_tile.has_worker() or neighbor_tile.get_level() == 4:
                raise InvalidDirectionError(dir, dir_type)
            if (dir_type == "move") and (neighbor_tile.get_level() > worker_level + 1):
                raise InvalidDirectionError(dir, dir_type)
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
