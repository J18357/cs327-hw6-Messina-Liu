from memento import Board, Caretaker
from exceptions import InvalidDirectionError

class Game:
    def __init__(self):
        # initialize the players within the board
        # self.players = [Player(1), Player(2)]
        self._board = Board()
        self.caretaker = Caretaker(self._board)
        self.test_dict = {'tuple': (23, 32)}
        self.direction_dict = {"n":(-1,0), 
                               "ne":(-1,1),
                               "e":(0,1),
                               "se":(1,1),
                               "s":(1,0),
                               "sw":(1,-1),
                               "w":(0,-1),
                               "nw":(-1,-1)}
    
    def check_move_dir(self, selectedWorker, dir_type, dir, proposal=None):
        input_dir = self.direction_dict[dir] # a tuple
        workerPosition = selectedWorker.get_position()
        if not proposal is None:
            workerPosition = proposal
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
        '''Returns list of valid step OR build (dir_type) moves in tuple form (ex: (1,1)) for the selected worker'''
        valid_moves_lst = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0 and j == 0):
                    pass
                else:
                    proposed_dir = self.get_dir_from_coords((i, j))
                    # print(f"Proposed dir: {proposed_dir}")
                    if self.check_move_dir(selectedWorker, dir_type, proposed_dir):
                        valid_moves_lst.append(proposed_dir)
        return valid_moves_lst
    
    def enumerate_full_moves(self, selectedWorker):
        '''Returns list of valid moves for the selected worker in the form:
        [position after move (tuple),  step direction (letter), build direction (letter)]
        '''
        valid_steps = self.enumerate_moves(selectedWorker, "move")
        for valid_step in valid_steps:
            # worker's position after proposed step
            proposed_currPos_row = selectedWorker.get_position()[0] + valid_step[0]
            proposed_currPos_col = selectedWorker.get_position()[1] + valid_step[1]

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i == 0 and j == 0):
                        pass
                else:
                    proposed_build_dir = self.get_dir_from_coords((i, j))
                    # Get valid build directions using worker's (fake) position after proposed step
                    if self.check_move_dir(selectedWorker, "build", proposed_build_dir, proposal=(proposed_currPos_row, proposed_currPos_col)):
                        # Both step direction and build direction are valid
                        valid_step_letter = self.get_dir_from_coords(valid_step) # convert direction to letter for debug/visualize
                        valid_build_letter = self.get_dir_from_coords(proposed_build_dir)
                        proposed_pos = (proposed_currPos_row, proposed_currPos_col)

                        valid_moves_lst.append([proposed_pos, valid_step_letter, valid_build_letter])
        return valid_moves_lst
    
    def get_height_score(self, worker1_pos, worker2_pos):
       return self.get_tile_level(worker1_pos) + self.get_tile_level(worker2_pos)

    def get_center_score(self, worker1_pos, worker2_pos):
        return self.get_center_score_helper(worker1_pos) + self.get_center_score_helper(worker2_pos)

    def get_center_score_helper(self, selectedWorkerPos):
        wRow = selectedWorkerPos[0]
        wCol = selectedWorkerPos[1]
        if wRow == 2 and wCol == 2:
            return 2
        elif wRow in [0,4] or wCol in [0,4]:
            return 0
        else:
            return 1
 
    def get_distance_score(self, movedWorkerPos, nonMovedWorkerPos):
        # Ex: for blue, dscore = min(distance from Z to A, distance from Y to A) + min(distance from Z to B, distance from Y to B)
        otherPlayer_pos = self._board.get_otherPlayer_positions(movedWorkerPos, nonMovedWorkerPos)
        otherPlayer_w1_pos = otherPlayer_pos[0]
        otherPlayer_w2_pos = otherPlayer_pos[1]

        distance_from_movedW_to_w1 = abs(movedWorkerPos[0] - otherPlayer_w1_pos[0]) + abs(movedWorkerPos[1] - otherPlayer_w1_pos[1])
        distance_from_nonMW_to_w1 = abs(nonMovedWorkerPos[0] - otherPlayer_w1_pos[0]) + abs(nonMovedWorkerPos[1] - otherPlayer_w1_pos[1])
        
        distance_from_movedW_to_w2 = abs(movedWorkerPos[0] - otherPlayer_w2_pos[0]) + abs(movedWorkerPos[1] - otherPlayer_w2_pos[1])
        distance_from_nonMW_to_w2 = abs(nonMovedWorkerPos[0] - otherPlayer_w2_pos[0]) + abs(nonMovedWorkerPos[1] - otherPlayer_w2_pos[1])

        distance_score = min(distance_from_movedW_to_w1, distance_from_nonMW_to_w1) + min(distance_from_movedW_to_w2, distance_from_nonMW_to_w2)
        return 8 - distance_score

    def get_curr_score(self, workers_lst):
        worker1_pos = workers_lst[0].get_position()
        worker2_pos = workers_lst[1].get_position()

        height_score = self.get_height_score(worker1_pos, worker2_pos)
        center_score = self.get_center_score(worker1_pos, worker2_pos)
        distance_score = self.get_distance_score(worker1_pos, worker2_pos)

        return f"({height_score},{center_score},{distance_score})"

    # Helper function to return key for any value
    def get_dir_from_coords(self, val):
        for key, value in self.direction_dict.items():
            if val == value:
                return key
        return None
    
    # Helper function to return value for any key
    def get_coords_from_key(self, key):
        return self.direction_dict[key]

    def update_board_step(self, worker_oldPos, worker_newPos, selectedWorker):
        self._board.update_tile(worker_oldPos)
        self._board.update_tile(worker_newPos, selectedWorker) # passes selectedWorker reference to new tile

    def update_board_build(self, build_pos):
        self._board.update_tile_build(build_pos)

    
    def display_board(self):
        # for i in range(5):
        #     print("+--+--+--+--+--+")
        #     for j in range(5):
        #         print(f"|{self._board.tiles[i][j].level}",end='')
        #         if (self._board.tiles[i][j].has_worker() == False):
        #             print(" ", end='')
        #         else:
        #             print(f"{self._board.tiles[i][j].worker.get_letter()}",end='')

        #     print("|")
        # print("+--+--+--+--+--+")
        self.caretaker.show_board()

    def save_board(self):
        self.caretaker.save()

    def undo_board(self):
        return self.caretaker.undo()

    def redo_board(self):
        return self.caretaker.redo()