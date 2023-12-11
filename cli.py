import sys
from game import Game
from player import PlayerContext, HumanPlayer, RandomAI, HeuristicAI
# import pickle
from exceptions import InvalidDirectionError

class Menu:
    """Display a menu and respond to choices when run."""

    # Store the currently selected account
    selected_account = None

    def __init__(self, white_player_type, blue_player_type, enable_undo_redo, enable_score):
        """initialize menu with options"""
        self._game = Game()
        self._valid_directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
        self._turn = 1
        self._gameOver = False
        self._undo_redo = True if enable_undo_redo == "on" else False
        # initialize the players
        print(f"player 1 type: {white_player_type}, player 2 type: {blue_player_type}")
        self.players = [self._set_player_strat(white_player_type, 1), self._set_player_strat(blue_player_type, 2)]

        # save the game
        self._game.save_board()
        
    def _set_player_strat(self, player_type, playerNum):
        # Assumes that player_type is valid
        if  player_type == "human":
            return PlayerContext(HumanPlayer(playerNum, game=self._game))
        elif player_type == "random":
            return PlayerContext(RandomAI(playerNum, game=self._game))
        elif player_type == "heurestic":
            return PlayerContext(HeuristicAI(playerNum, game=self._game))
    
    def get_curr_player(self):
        """returns the current player number (1 or 2)"""
        return (self._turn+1) % 2 + 1
    
    def _display_menu(self):
        # print the game board
        # workers_lst = self.get_all_workers()
        self._game.display_board()
        
        # print the turn and current player
        print(f"Turn: {self._turn}, {self.display_player()}", end="")

        # TODO: if score display is enabled, print score
        if (sys.argv[4] == "on"):
            print(f", {self._game.get_curr_score(self.players[0].get_workers())}")
        else:
            print()

    
    def display_player(self):
        # displays player 1 or 2
        if self.get_curr_player() == 1:
            return f"white ({self.players[0].get_workers()[0].get_letter()}{self.players[0].get_workers()[1].get_letter()})"
        else:
            return f"blue ({self.players[1].get_workers()[0].get_letter()}{self.players[1].get_workers()[1].get_letter()})"
        
    def get_all_workers(self):
        """returns all workers [p1_worker1, p1_worker2, p2_worker1, p2_worker2]"""
        all_workers = []
        for worker in self.players[0].get_workers():
            all_workers.append(worker)
        for worker in self.players[1].get_workers():
            all_workers.append(worker)
        return all_workers
    
    # TODO: in cli.py under display menu
    def display_score(self):
        print()
    
    def run(self):
        """Display the menu and respond to choices."""
        while not self._gameOver:
            if self.check_game_ended() != 0:
                self._gameOver = True
            
            # displays turn number and player
            self._display_menu()

            # asks for undo/redo if that is enabled
            if self._undo_redo == True and self.players[self.get_curr_player() - 1].player_type_human():
                undo_redo_next = input("undo, redo, or next\n")
                while (undo_redo_next not in  ["undo", "redo", "next"]):
                    undo_redo_next = input("undo, redo, or next\n")
                    
                if undo_redo_next == "undo":
                    if self.players[self.get_curr_player() % 2].player_type_human() == False:
                        if self._game.undo_board():
                            self._game.undo_board()
                            self._turn -= 2
                    elif self._game.undo_board():
                        self._turn -= 1
                elif undo_redo_next == "redo":
                    if self.players[self.get_curr_player() % 2].player_type_human() == False:
                        if self._game.redo_board():
                            self._game.redo_board()
                            self._turn += 2
                    elif self._game.redo_board():
                        self._turn += 1
                else:
                    self.players[self.get_curr_player() - 1].movePlayer()
                    self._turn = self._turn + 1
            else:
                self.players[self.get_curr_player() - 1].movePlayer()
                self._turn = self._turn + 1
        
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
        for i in [0,1]:
            if self.players[i].check_winner():
                isWinner = i+1
            elif self.players[i].check_loser():
                isWinner = 3 - (i+1)
            else:
                isWinner = 0
        return isWinner
    
    def restart(self):
        restartInput = input("Would you like to play again?\n")
        if restartInput == "yes":
            self._game = Game()
            self._gameOver = False
            # TODO: Reset players / worker positions
            # self.players = [Player(1), Player(2)]
            self.turn = 1
            self.run()
        else:
            self._quit()

    def _quit(self):
        sys.exit(0)


if __name__ == "__main__":
    white_player_type = "human"
    blue_player_type = "human"
    enable_undo_redo = "off"
    enable_score = "off"

    if sys.argv[1:]:   # test if there are atleast 1 argument (beyond [0])
        white_player_type = sys.argv[1]
        if sys.argv[2:]:
            blue_player_type = sys.argv[2]
            if sys.argv[3:]:
                enable_undo_redo = sys.argv[3]
                if sys.argv[4]:
                    enable_score = sys.argv[4]
    
    Menu(white_player_type, blue_player_type, enable_undo_redo, enable_score).run()

    # TODO: catch AttributeError from restart input > exit
