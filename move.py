
from worker import Worker
from board import Board

class Move():
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
    
    def execute(self, selectedWorker, step_direction, build_direction):
        currPos = selectedWorker.get_position()
        step_dir = self.direction_dict[step_direction]
        selectedWorker.step(currPos[0]+step_dir[0], currPos[1]+step_dir[1])
        # TODO:
        # board.update()