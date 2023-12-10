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
    
    def execute(self, game, selectedWorker, step_direction=None, build_direction=None):
        if not step_direction is None:
            currPos = selectedWorker.get_position()
            step_dir = self.direction_dict[step_direction]
            new_pos_row = currPos[0]+step_dir[0]
            new_pos_col = currPos[1]+step_dir[1]
            game.update_board_step(currPos, [new_pos_row, new_pos_col], selectedWorker)
            selectedWorker.step(new_pos_row, new_pos_col)
        elif not build_direction is None:
            currPos = selectedWorker.get_position()
            build_dir = self.direction_dict[build_direction]
            build_pos_row = currPos[0]+build_dir[0]
            build_pos_col = currPos[1]+build_dir[1]
            
            game.update_board_build([build_pos_row, build_pos_col])
        else:
            print("No direction to move was given")
        
        # TODO: score?