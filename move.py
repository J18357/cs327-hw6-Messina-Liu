from worker import Worker
# from board import Board
from abc import ABC, abstractmethod

class Command():
    """The command interface decleares a method for executing a command"""

    @abstractmethod
    def execute(self):
        pass

class Move(Command):
    '''A command pattern'''
    def __init__(self):
        self.direction_dict = {"n":(-1,0), 
                               "ne":(-1,1),
                               "e":(0,1),
                               "se":(1,1),
                               "s":(1,0),
                               "sw":(1,-1),
                               "w":(0,-1),
                               "nw":(-1,-1)}
        self._move = None
        
    def human_move(self, command: Command):
        self._move = command
    
    def execute(self, selectedWorker, step_direction, build_direction):
        currPos = selectedWorker.get_position()
        step_dir = self.direction_dict[step_direction]
        selectedWorker.step(currPos[0]+step_dir[0], currPos[1]+step_dir[1])
        # TODO: # the board updates itself as the player moves, or else we get circular dependency
        # board.update() return to the game to do that

        # # building
        # self.build(self, selectedWorker, build_direction)

# can't build here or worker or else get circular dependency when try to access board


# Invoker = the player, def move_worker(self, command: Command)
# Command is the interface with abstract method def execute(self) ***skip
# Simple command inherits command to create execute, has innit for payload then execute for doing something ***this is move