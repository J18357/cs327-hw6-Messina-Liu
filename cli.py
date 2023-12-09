import sys
from game import Game
from player import Player
# from tile import Tile
# import pickle
from exceptions import InvalidDirectionError

class Menu:
    """Display a menu and respond to choices when run."""

    # Store the currently selected account
    selected_account = None

    def __init__(self):
        """initialize menu with options"""
        self._game = Game()
        self._valid_directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
        self._turn = 1
        self._gameOver = False
        # initialize the players
        self.players = [Player(1), Player(2)]

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
        while not self._gameOver:
            if self.check_game_ended() != 0:
                self._gameOver = True
            
            # displays turn number and player
            self._display_menu()

            # + playerContext.setStrategy(human)
            # + maybe in Run(), strategy.move()
            # TODO: put worker selection in separate method

            # TODO: take out?
            # if action:
            #     action()
            # else:
            #     print("{0} is not a valid choice".format(choice))
        
        # game over
        if self.check_game_ended == 1:
            winnerColor = "white"
        else:
            winnerColor = "blue"
        print(f"{winnerColor} has won")
        self.restart()
    
    def check_game_ended(self):
        '''If there is a winner, returns the winner's player number, otherwise returns 0'''
        isWinner = 0
        for playerNum in [1,2]:
            if self.players[playerNum].check_winner():
                isWinner = playerNum
            elif self.players[playerNum].check_loser():
                isWinner = 3-playerNum
            else:
                isWinner = 0
        return isWinner
    
    def restart(self):
        restartInput = input("Would you like to play again?\n")
        if restartInput == "yes":
            self.game = Game()
            self._gameOver = False
            self.players = [Player(1), Player(2)]
            self.turn = 1
            self.run()
        else:
            self._quit()
    
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

    # TODO: catch AttributeError from restart input > exit
