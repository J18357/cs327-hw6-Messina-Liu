class InvalidDirectionError(Exception):
    "Indicates that move direction for the selected player's worker is invalid."
    def __init__(self, dir_type):
        super().__init__()
        self.dir_type = dir_type
