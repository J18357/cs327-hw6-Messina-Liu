from worker import Worker
from move import Move
import random
from abc import abstractmethod

class Player:
    def __init__(self, player, game): # game

        self._valid_directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
        self._selectedWorker = None
        self.game = game
        self.moveCommand = Move()
        self._initialize_workers(player)

    def _initialize_workers(self, player):
        """initialize workers within a given player"""
        # initialize workers within a player
        if player == 1:
            self.workers = [Worker("A", 3, 1), Worker("B", 1, 3)]
        elif player == 2:
            self.workers = [Worker("Y", 1, 1), Worker("Z", 3, 3)]
        
        # update the board
        for worker in self.workers:
            self.game.update_board_step([0,0], worker.get_position(), worker)

    def get_workers(self):
        """returns a list of the workers of the player"""
        return self.workers
    
    def is_players_worker(self, input_worker):
        """check if a given worker belongs to the player"""
        for worker in self.workers:
            if worker.letter == input_worker:
                return True
        return False
    
    def _select_this_worker(self, input_letter):
        '''Returns this player's worker corresponding to the worker's letter.
         Assumes that the letter does correspond to this player'''
        for worker in self.workers:
            if worker.letter == input_letter:
                return worker
        return None
        
    def check_winner(self):
        """checks if either of the player's workers are on level 3 (if yes then they win)"""
        for worker in self.workers:
            workerPos = worker.get_position()
            if self.game.get_tile_level(workerPos) == 3:
                return True
        return False
    
    def check_loser(self):
        """checks if either of the player's workers can move (if no then they lose)"""
        if len(self.game.enumerate_moves(self.workers[0], "move")) == 0 and len(self.game.enumerate_moves(self.workers[1], "move")) == 0:
            print("here is we")
            return True
        else:
            return False
        
    @abstractmethod
    def move(self):
        pass

class HumanPlayer(Player):

    # TODO: move some of this to abstract player class
    def move(self):

        # Might move worker selection checks into separate helper method for HumanPlayer
        selectedWorker = None
        while selectedWorker is None:
            workerInput = input("Select a worker to move\n") # TODO: Check TypeError?
            if workerInput not in ["A", "B", "Y", "Z"]:
                print("Not a valid worker")
            elif not self.is_players_worker(workerInput):
                print("That is not your worker")
            else:
                worker_to_check = self._select_this_worker(workerInput)
                # check if the selected worker is capable of moving
                # note: at least one worker should be capable of moving since we checked gameOver() before this turn/move
                valid_moves_lst = self.game.enumerate_moves(self._select_this_worker(workerInput), "move")
                if len(valid_moves_lst) == 0:
                    print("That worker cannot move")
                else:
                    selectedWorker = worker_to_check
        self._selectedWorker = selectedWorker
            
        # Specs say we should check valid directions for move and build BEFORE we call move_worker on player
        step_direction = self._select_direction("move")
        self.moveCommand.execute(self.game, selectedWorker, step_direction=step_direction)

        # building after the player moves
        build_direction = self._select_direction("build")
        self.moveCommand.execute(self.game, selectedWorker, build_direction=build_direction)
        
        letter_to_print = self._selectedWorker.get_letter()
        return f"{letter_to_print},{step_direction},{build_direction}"



    def _select_direction(self, dir_type):
        '''dir_type: String, either "move" or "build"'''

        valid_direction = None
        while valid_direction is None:
            try:
                dir_input = input(f"Select a direction to {dir_type} (n, ne, e, se, s, sw, w, nw)\n")
                if dir_input.lower() in self._valid_directions:
                    dir_input = dir_input.lower()
                    if self.game.check_move_dir(self._selectedWorker, dir_type, dir_input) == False:
                        print(f"Cannot {dir_type} {dir_input}")
                    else:
                        valid_direction = dir_input
                else:
                    raise ValueError # TODO: Check if should be AttributeError
            except ValueError:
                print("Not a valid direction")
        return(valid_direction)


class RandomAI(Player):
    def move(self):
        '''
        Randomly chooses a move from set of allowed moves
        (1) randomly choose a worker
        (2) choose a move from worker's set of allowed moves for step and build
        '''
        
        selectedWorkerNum = random.choice([0,1])
        self._selectedWorker = self.workers[selectedWorkerNum]
        
        workers_valid_moves = self.game.enumerate_moves(self._selectedWorker, "move")
        if len(workers_valid_moves) == 0:
            # if worker is unable to move, select the other worker
            self._selectedWorker = self.workers[(selectedWorkerNum + 1) % 2]
            # find other worker's valud moves
            workers_valid_moves = self.game.enumerate_moves(self._selectedWorker, "move")
    
        step_direction = random.choice(workers_valid_moves)

        self.moveCommand.execute(self.game, self._selectedWorker, step_direction=step_direction)

        worker_valid_builds = self.game.enumerate_moves(self._selectedWorker, "build")
        # we know this worker can at least build on their previous position, so we don't need to check for no valid builds
        build_direction = random.choice(worker_valid_builds)
        self.moveCommand.execute(self.game, self._selectedWorker, build_direction=build_direction)
        
        letter_to_print = self._selectedWorker.get_letter()
        return f"{letter_to_print},{step_direction},{build_direction}"


class HeuristicAI(Player):
    def move(self):
        
        # get a list of all possible moves for each of the player's workers
        worker1_moves_lst = self.game.enumerate_full_moves(self.workers[0])
        worker2_moves_lst = self.game.enumerate_full_moves(self.workers[1])

        # determine the "best" move to make (sum of scores)
        worker1_max_move_lst = self.get_move_score(0, worker1_moves_lst)
        worker2_max_move_lst = self.get_move_score(1, worker2_moves_lst)

        # compare max move_score from each worker's list
        # ex: move = [position_after_move=(3,4), step_dir="n", build_dir="s"]
        if worker1_max_move_lst[1] > worker2_max_move_lst[1]:
            step_letter = worker1_max_move_lst[0][1]
            build_letter = worker1_max_move_lst[0][2]
            self._selectedWorker = self.workers[0]
        else:
            step_letter = worker2_max_move_lst[0][1]
            build_letter = worker2_max_move_lst[0][2]
            self._selectedWorker = self.workers[1]

        # step_direction = self.game.get_coords_from_key(step_letter)
        self.moveCommand.execute(self.game, self._selectedWorker, step_direction=step_letter)

        # build_direction = self.game.get_coords_from_key(build_letter)
        self.moveCommand.execute(self.game, self._selectedWorker, build_direction=build_letter)

        letter_to_print = self._selectedWorker.get_letter()
        return f"{letter_to_print},{step_letter},{build_letter}"

    def get_move_score(self, selectedWorkerNum, valid_moves_lst):
        '''Returns list containing the (valid) move with the maximum move_score for the selected worker of the form:
        [move (list), move_score (int)]
        '''
        max_move_score = 0
        max_move = None
        for move in valid_moves_lst:
            # ex: move = [position_after_move=(3,4), step_dir="n", build_dir="s"]
            nonMovedWorkerPos = self.workers[selectedWorkerNum].get_position()
            movedWorkerPos = move[0]

            # height_score: sum of the heights of the buildings a player's workers stand on
            height_score = self.game.get_height_score(nonMovedWorkerPos, movedWorkerPos)

            # center_score: 
            center_score = self.game.get_center_score(nonMovedWorkerPos, movedWorkerPos)
            
            # distance_score: sum of the minimum distance to the opponent's workers
            distance_score = self.game.get_distance_score(movedWorkerPos, nonMovedWorkerPos)

            c1 = 3
            c2 = 2
            c3 = 1
            move_score = c1*height_score + c2*center_score + c3*distance_score
            if move_score >= max_move_score:
                max_move = move
                max_move_score = move_score
        return [max_move, max_move_score]

class PlayerContext:
    def __init__(self, player_type_with_params: Player):
        '''For encapsulation of Player class from Client'''
        self._player = player_type_with_params
    
    def movePlayer(self):
        print(self._player.move(), end="")
        self._player.game.save_board()
    
    def check_winner(self):
        return self._player.check_winner()
    
    def check_loser(self):
        return self._player.check_loser()
    
    def get_workers(self):
        return self._player.get_workers()
    
    def player_type_human(self):
        return str(type(self._player).__name__) == "HumanPlayer"