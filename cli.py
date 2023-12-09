import sys
from game import Game
# from tile import Tile
# import pickle
# from bank import Bank
# from decimal import Decimal
# from transaction import Transaction
from exceptions import InvalidDirectionError

class Menu:
    """Display a menu and respond to choices when run."""

    # Store the currently selected account
    selected_account = None

    def __init__(self):
        """initialize menu with options"""
        self.game = Game()
        self._valid_directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
        self._turn = 1

        # TODO: we might be able to delete choices
        self._choices = {
            # "undo": self._undo,   # TODO: create undo function
            # "redo": self._redo,   # TODO: create redo function
            # "next": self._next ,  # TODO: create next function         
            "9": self._quit,                
        }
        
    def get_curr_player(self):
        """returns the current player"""
        return (self._turn+1) % 2 + 1
    
    def _display_menu(self):
        # print the game board
        self.game.display_board()

        # print the turn and current player
        print(f"Turn: {self._turn}, {self.game.display_player(self.get_curr_player())}", end="")

        # TODO: if score display is enabled, print score
        # if (sys.argv[4] == "on"):
        #     self._board.display_score()
        # else:
        #     print()

        print()
    
    def run(self):
        """Display the menu and respond to choices."""
        while True:
            # displays turn number and player
            self._display_menu()

            # asks for worker
            worker = input("Select a worker to move\n")
            # checks if selected worker is valid, reprompting if needed
            while self.game.is_valid_worker(self.get_curr_player(), worker) == False:
                worker = input("Select a worker to move\n")

            # Moves the worker selected

            # checks if selected direction is valid, reprompting if needed

            # + playerContext.setStrategy(human)
            # + maybe in Run(), strategy.move()
            # TODO: put worker selection in separate method

            # TODO: take out?
            # if action:
            #     action()
            # else:
            #     print("{0} is not a valid choice".format(choice))


    # def _save(self):
    #     with open("Bank_save.pickle", "wb") as f:
    #         pickle.dump(self._bank, f)

    # def _load(self):
    #     with open("Bank_save.pickle", "rb") as f:   
    #         self._bank = pickle.load(f)

    def _quit(self):
        sys.exit(0)


if __name__ == "__main__":
    Menu().run()
