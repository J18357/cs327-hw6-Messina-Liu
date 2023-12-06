from worker import Worker
from exceptions import InvalidDirectionError

class PlayerContext:
    def __init__(self):
        self._player = None

    def setPlayerStrategy(self, playerStrat):
        # TODO: validate that playerStrat is a real strategy?
        self._player = playerStrat
    
    def movePlayer(self):
        self._player.move()

class Player:
    def __init__(self):
        self.workers = [Worker()]
        # self.move = MoveCommand()

    def _initialize_workers(self):
        self.tiles[1][1].worker = Worker("Y", 1, 1)
        self.tiles[1][3].worker = Worker("B", 1, 3)
        self.tiles[3][1].worker = Worker("A", 3, 1)
        self.tiles[3][3].worker = Worker("Z", 3, 1)
    
    def move(self):
        pass

class HumanPlayer(Player):
    def move(self):
        # TODO: Prompts for 
        # Specs say we should check valid directions for move and build BEFORE we call move_worker on player
        self._step_direction = self._select_direction("move")
        self._build_direction = self._select_direction("build")
        print(f"{self._step_direction},{self._build_direction}\n")

# TODO: CHECK if we shoudl implement strategy pattern?
    def _select_direction(self, dir_type):
        '''dir_type: String, either "move" or "build"'''

        valid_direction = None
        
        while valid_direction is None:
            try:
                dir_input = input(f"Select a direction to {dir_type} (n, ne, e, se, s, sw, w, nw)\n")
                if dir_input.lower() in self._valid_directions:
                    dir_input = dir_input.lower()
                    # TODO
                    valid_direction = self._selectedPlayer.check_valid_move(self._worker_name, dir_type, dir_input)
                else:
                    raise ValueError # TODO: Check if should be AttributeError
            except ValueError:
                print("Not a valid direction")
            except InvalidDirectionError as ex:
                print(f"Cannot move {ex.dir_type}.")
        return(valid_direction)
        

