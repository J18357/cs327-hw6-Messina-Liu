from board import Board, Caretaker

class Game:
    def __init__(self):
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
    
    def check_move_dir(self, workerPos, dir_type, dir):
        '''Checks whether the given direction is valid for the given worker position (workerPos) and direction type (dir_type, "move" or "build").'''
        input_dir = self.direction_dict[dir] # a tuple
        workerPosition = workerPos
        move_row = workerPosition[0] + input_dir[0]
        move_col = workerPosition[1] + input_dir[1]
        # check still in board
        if move_row < 0 or move_row > 4 or move_col < 0 or move_col > 4:
            return False
        else:
            
            # check space does not have a worker or dome (level 4)
            if self._board.get_tile_has_worker(move_row, move_col) or self._board.get_tile_level(move_row, move_col) == 4:
                return False
            if (dir_type == "move") and (self._board.get_tile_level(move_row, move_col) > self._board.get_tile_level(workerPosition[0], workerPosition[1]) + 1):          
                return False
        return True
    
    def get_tile_level(self, workerPos):
        return self._board.get_tile_level(workerPos[0], workerPos[1])
    
    def check_moves_adaptor(self, selectedWorker, dir_type, dir, proposal=None):
        '''Semi-adaptor design pattern to simplify check_move_dir()'''
        workerPos = selectedWorker.get_position()
        if not proposal is None:
            workerPos = proposal
        return self.check_move_dir(workerPos, dir_type, dir)
    
    def enumerate_moves(self, selectedWorker, dir_type):
        '''Returns list of valid step OR build (dir_type) moves in tuple form (ex: (1,1)) for the selected worker'''
        valid_moves_lst = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0 and j == 0):
                    pass
                else:
                    proposed_dir = self.get_dir_from_coords((i, j))
                    # print(f"proposed {proposed_dir}")
                    if self.check_moves_adaptor(selectedWorker, dir_type, proposed_dir):
                        valid_moves_lst.append(proposed_dir)
                        # print(valid_moves_lst)
        return valid_moves_lst
    
    def enumerate_full_moves(self, selectedWorker):
        '''Returns list of valid moves for the selected worker in the form:
        [position after move (tuple),  step direction (letter), build direction (letter)]
        '''
        valid_moves_lst = []
        valid_steps = self.enumerate_moves(selectedWorker, "move")

        for valid_step in valid_steps:
            # worker's position after proposed step
            proposed_currPos_row = selectedWorker.get_position()[0] + self.direction_dict[valid_step][0]
            proposed_currPos_col = selectedWorker.get_position()[1] + self.direction_dict[valid_step][1]

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i == 0 and j == 0):
                        pass
                else:
                    proposed_build_dir = self.get_dir_from_coords((i, j))
                    # Get valid build directions using worker's (fake) position after proposed step
                    if self.check_moves_adaptor(selectedWorker, "build", proposed_build_dir, proposal=(proposed_currPos_row, proposed_currPos_col)):
                        # Both step direction and build direction are valid
                        valid_step_letter = valid_step
                        valid_build_letter = proposed_build_dir

                        proposed_pos = (proposed_currPos_row, proposed_currPos_col)

                        valid_moves_lst.append([proposed_pos, valid_step_letter, valid_build_letter])
        return valid_moves_lst
    
    def get_height_score(self, worker1_pos, worker2_pos):
       return self._board.get_tile_level(worker1_pos[0], worker1_pos[1]) + self._board.get_tile_level(worker2_pos[0], worker2_pos[1])

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

        distance_from_movedW_to_w1 = max(abs(movedWorkerPos[0] - otherPlayer_w1_pos[0]), abs(movedWorkerPos[1] - otherPlayer_w1_pos[1]))
        distance_from_nonMW_to_w1 = max(abs(nonMovedWorkerPos[0] - otherPlayer_w1_pos[0]), abs(nonMovedWorkerPos[1] - otherPlayer_w1_pos[1]))
        
        distance_from_movedW_to_w2 = max(abs(movedWorkerPos[0] - otherPlayer_w2_pos[0]), abs(movedWorkerPos[1] - otherPlayer_w2_pos[1]))
        distance_from_nonMW_to_w2 = max(abs(nonMovedWorkerPos[0] - otherPlayer_w2_pos[0]), abs(nonMovedWorkerPos[1] - otherPlayer_w2_pos[1]))

        distance_score = min(distance_from_movedW_to_w1, distance_from_nonMW_to_w1) + min(distance_from_movedW_to_w2, distance_from_nonMW_to_w2)
        return 8 - distance_score

    def get_curr_score(self, workers_lst):
        worker1_pos = workers_lst[0].get_position()
        worker2_pos = workers_lst[1].get_position()

        height_score = self.get_height_score(worker1_pos, worker2_pos)
        center_score = self.get_center_score(worker1_pos, worker2_pos)
        distance_score = self.get_distance_score(worker1_pos, worker2_pos)

        return f"({height_score}, {center_score}, {distance_score})"

    def get_dir_from_coords(self, val):
        '''Helper function to return key for any value'''
        for key, value in self.direction_dict.items():
            if val == value:
                return key
        return None
    
    def get_coords_from_key(self, key):
        '''Helper function to return value for any key'''
        return self.direction_dict[key]

    def update_board_step(self, worker_oldPos, worker_newPos, selectedWorker):
        self._board.update_tile(worker_oldPos)
        self._board.update_tile(worker_newPos, selectedWorker) # passes selectedWorker reference to new tile

    def update_board_build(self, build_pos):
        self._board.update_tile_build(build_pos)

    
    def display_board(self):
        self.caretaker.show_board()

    def save_board(self):
        self.caretaker.save()

    def undo_board(self):
        result = self.caretaker.undo()
        return result

    def redo_board(self):
        return self.caretaker.redo()
    
    def update_workers(self, workers):
        for worker in workers:
            for i in range(5):
                for j in range(5):
                    if self._board.tiles[i][j].has_worker() and self._board.tiles[i][j].worker.get_letter() == worker.get_letter():
                        worker.row = self._board.tiles[i][j].worker.row
                        worker.col = self._board.tiles[i][j].worker.col