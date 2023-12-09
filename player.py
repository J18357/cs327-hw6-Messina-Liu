from worker import Worker
# from game import Game
from exceptions import InvalidDirectionError



class Player:
    def __init__(self, player, game): # game
        self._initialize_workers(player)
        self._valid_directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
        self._selectedWorker = None
        self.game = game
        # self.move = MoveCommand()

    def _initialize_workers(self, player):
        """initialize workers within a given player"""
        # initialize workers within a player
        if player == 1:
            self.workers = [Worker("A", 3, 1), Worker("B", 1, 3)]
        elif player == 2:
            self.workers = [Worker("Y", 1, 1), Worker("Z", 3, 3)]

    def get_workers(self):
        """returns a list of the workers of the player"""
        return self.workers
    
    def is_players_worker(self, input_worker):
        """check if a given worker belongs to the player"""
        for worker in self.workers:
            if worker.letter == input_worker:
                return True
        return False
    
    def move(self):
        pass
    
    def _select_this_worker(self, input_letter):
        '''Returns this player's worker corresponding to the worker's letter.
         Assumes that the letter does correspond to this player'''
        for worker in self.workers:
            if worker.letter == input_letter:
                return worker
        return None
        
    def check_winner(self):
        for worker in self.workers:
            workerPos = worker.get_position()
            if self.game.get_tile_level(workerPos) == 3:
                return True
        return False
    
    def check_loser(self):
        if len(self.game.enumerate_moves(self.workers[0])) == 0 and len(self.game.enumerate_moves(self.workers[1])) == 0:
            return True
        else:
            return False

class HumanPlayer(Player):

    # TODO: move some of this to abstract player class
    def move(self):

        # Might move worker selection checks into separate helper method for HumanPlayer
        selectedWorker = None
        while selectedWorker is None:
            workerInput = input("Select a worker to move\n") # TODO: Check TypeError?
            if workerInput not in ["A", "B", "Y", "Z"]:
                print("Not a valid worker\n")
            elif not self.is_players_worker(workerInput):
                print("That is not your worker\n")
            else:
                worker_to_check = self._select_this_worker(workerInput)
                # check if the selected worker is capable of moving
                # note: at least one worker should be capable of moving since we checked gameOver() before this turn/move
                valid_moves_lst = self.game.enumerate_moves(self._select_this_worker(workerInput))
                if len(valid_moves_lst) == 0:
                    print("That worker cannot move\n")
                else:
                    selectedWorker = worker_to_check
        self._selectedWorker = selectedWorker
            
        # Specs say we should check valid directions for move and build BEFORE we call move_worker on player
        self._step_direction = self._select_direction("move")
        self._build_direction = self._select_direction("build")
        print(f"{self._step_direction},{self._build_direction}\n")

    def _select_direction(self, dir_type):
        '''dir_type: String, either "move" or "build"'''

        valid_direction = None
        
        while valid_direction is None:
            try:
                dir_input = input(f"Select a direction to {dir_type} (n, ne, e, se, s, sw, w, nw)\n")
                if dir_input.lower() in self._valid_directions:
                    dir_input = dir_input.lower()
                    if self.game._check_move_dir(self._selectedWorker, dir_type, dir_input) == False:
                        print(f"Cannot {dir_type} {dir}.")
                    else:
                        valid_direction = dir_input
                else:
                    raise ValueError # TODO: Check if should be AttributeError
            except ValueError:
                print("Not a valid direction")
            # except InvalidDirectionError as ex:
                # print(f"Cannot {ex.dir_type} {ex.dir}.")
        return(valid_direction)
    
    def enum_moves(self):
        pass
        
class RandomAI(Player):
    pass

class HeuristicAI(Player):
    pass

class PlayerContext:
    def __init__(self, player_type_with_params: Player):
        '''For encapsulation of Player class from Client'''
        self._player = player_type_with_params

    # def setPlayerStrategy(self, playerStrat):
    #     # TODO: validate that playerStrat is a real strategy?
    #     self._player = playerStrat
    
    def movePlayer(self):
        self._player.move()
    
    def check_winner(self):
        return self._player.check_winner()
    
    def check_loser(self):
        return self._player.check_loser()
    
    def get_workers(self):
        return self._player.get_workers()