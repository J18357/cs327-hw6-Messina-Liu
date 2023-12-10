from board import Board
from exceptions import InvalidDirectionError

class Game:
    def __init__(self):
        # initialize the players within the board
        # self.players = [Player(1), Player(2)]
        self._board = Board()
        self.test_dict = {'tuple': (23, 32)}
        self.direction_dict = {"n":(-1,0), 
                               "ne":(-1,1),
                               "e":(0,1),
                               "se":(1,1),
                               "s":(1,0),
                               "sw":(1,-1),
                               "w":(0,-1),
                               "nw":(-1,-1)}
    
    def check_move_dir(self, selectedWorker, dir_type, dir):
        input_dir = self.direction_dict[dir] # a tuple
        workerPosition = selectedWorker.get_position()
        move_row = workerPosition[0] + input_dir[0]
        move_col = workerPosition[1] + input_dir[1]
        # check still in board
        if move_row < 0 or move_row > 4 or move_col < 0 or move_col > 4:
            return False
        else:
            neighbor_tile = self._board.tiles[move_row][move_col]

            # check space does not have a worker or dome (level 4)
            # TODO: check encapsulation of Tile from Game
            if neighbor_tile.has_worker() or neighbor_tile.get_level() == 4:
                # print("neighbor tile has a worker or dome")
                return False
            if (dir_type == "move") and (neighbor_tile.get_level() > self.get_tile_level(workerPosition) + 1):
                # print("can't move onto +2 level")
                return False
        return True
    
    def get_tile_level(self, workerPosition):
        worker_tile = self._board.tiles[workerPosition[0]][workerPosition[1]]
        return worker_tile.get_level()
    
    def enumerate_moves(self, selectedWorker, dir_type):
        '''Returns list of valid step OR build (dir_type) moves for the selected worker'''
        valid_moves_lst = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0 and j == 0):
                    pass
                else:
                    proposed_dir = self._get_dir_from_coords((i, j))
                    # print(f"Proposed dir: {proposed_dir}")
                    if self.check_move_dir(selectedWorker, dir_type, proposed_dir):
                        valid_moves_lst.append(proposed_dir)
        return valid_moves_lst
    
    # Helper function to return key for any value
    def _get_dir_from_coords(self, val):
        for key, value in self.direction_dict.items():
            if val == value:
                return key
        return None
        
    # def is_valid_worker(self, player, worker):
    #     if player == 1:
    #         if self.players[0].is_players_worker(worker):
    #             return True
    #         if self.players[1].is_players_worker(worker):
    #             print("That is not your worker")
    #             return False
    #     else:
    #         if self.players[1].is_players_worker(worker):
    #             return True
    #         if self.players[0].is_players_worker(worker):
    #             print("That is not your worker")
    #             return False
    #     print("Not a valid worker")
    #     return False

    def update_board_step(self, worker_oldPos, worker_newPos, selectedWorker):
        self._board.update_tile(worker_oldPos)
        self._board.update_tile(worker_newPos, selectedWorker) # passes selectedWorker reference to new tile

    def update_board_build(self, build_pos):
        self._board.update_tile_build(build_pos)

    
    def display_board(self, all_workers):
        for i in range(5):
            print("+--+--+--+--+--+")
            for j in range(5):
                print(f"|{self._board.tiles[i][j].level}",end='')

                # if there is a worker on the tile or not
                is_worker = False
                for worker in all_workers:
                    if [i,j] == worker.get_position():
                        print(f"{worker.get_letter()}",end='')
                        is_worker = True
                if is_worker == False:
                    print(" ", end='')
            print("|")
        print("+--+--+--+--+--+")
