import sys
from game import Game
from player import PlayerContext, HumanCreator, RandomAICreator, HeuristicAICreator

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
        self._undo_redo = enable_undo_redo == "on"
        self._score_enable = enable_score == "on"
        self._white_player_type = white_player_type
        self._blue_player_type = blue_player_type
        # initialize the players
        self.players = [self._set_player_strat(white_player_type, 1), self._set_player_strat(blue_player_type, 2)]

        # save the game
        self._game.save_board()
        
    def _set_player_strat(self, player_type, playerNum):
        # Assumes that player_type is valid
        if  player_type == "human":
            return (HumanCreator(playerNum, game=self._game))
        elif player_type == "random":
            return (RandomAICreator(playerNum, game=self._game))
        elif player_type == "heuristic":
            return (HeuristicAICreator(playerNum, game=self._game))
    
    def get_curr_player(self):
        """returns the current player number (1 or 2)"""
        return (self._turn+1) % 2 + 1
    
    def _display_menu(self):
        """display's game information"""
        
        self._game.display_board()
        
        # print the turn and current player
        print(f"Turn: {self._turn}, {self.display_player()}", end="")

        # if score display is enabled, print score
        if (self._score_enable):
            print(f", {self._game.get_curr_score(self.players[self.get_curr_player() - 1].get_workers())}")
        else:
            print()

    
    def display_player(self):
        # displays player 1 or 2
        if self.get_curr_player() == 1:
            return f"white ({self.players[0].get_workers()[0].get_letter()}{self.players[0].get_workers()[1].get_letter()})"
        else:
            return f"blue ({self.players[1].get_workers()[0].get_letter()}{self.players[1].get_workers()[1].get_letter()})"
    

    def run(self):
        """Display the menu and respond to choices."""
        while not self._gameOver:
            if self.check_game_ended() != 0:
                self._gameOver = True
                self._display_menu()
                break
            
            # displays turn number and player
            self._display_menu()

            # asks for undo/redo if that is enabled
            if self._undo_redo == True and self.players[self.get_curr_player() - 1].player_type_human():
                undo_redo_next = input("undo, redo, or next\n")
                while (undo_redo_next not in  ["undo", "redo", "next"]):
                    undo_redo_next = input("undo, redo, or next\n")
                
                # if player presses undo
                if undo_redo_next == "undo":
                    # if we are at turn 2 and blue is human and white is AI, don't do anything
                    if self._turn != 2 or self.players[self.get_curr_player() % 2].player_type_human() == True:
                        # if the other player is an AI, undo twice, if human, once
                        if self.players[self.get_curr_player() % 2].player_type_human() == False:
                            if self._game.undo_board():
                                self._game.undo_board()
                                self._turn -= 2
                        elif self._game.undo_board():
                            self._turn -= 1
                        self.update_workers()

                # if player presses redo
                elif undo_redo_next == "redo":
                    # if the other player is an AI, redo twice, if human, once
                    if self.players[self.get_curr_player() % 2].player_type_human() == False:
                        if self._game.redo_board():
                            self._game.redo_board()
                            self._turn += 2
                    elif self._game.redo_board():
                        self._turn += 1
                    self.update_workers()

                # if the player presses next
                else:
                    self.players[self.get_curr_player() - 1].movePlayer()
                    if (self._score_enable):
                        print(f" {self._game.get_curr_score(self.players[self.get_curr_player() - 1].get_workers())}")
                    else:
                        print()
                    self._turn = self._turn + 1

            # if undo/redo is not enabled
            else:
                self.players[self.get_curr_player() - 1].movePlayer()
                if (self._score_enable):
                    print(f" {self._game.get_curr_score(self.players[self.get_curr_player() - 1].get_workers())}")
                else:
                    print()
                self._turn = self._turn + 1

        
        # game over
        if self.check_game_ended() == 1:
            winnerColor = "white"
        else:
            winnerColor = "blue"
        print(f"{winnerColor} has won")
        self.restart()
    
    def update_workers(self):
        """updates a player's workers"""
        for player in self.players:
            self._game.update_workers(player.get_workers())
    
    def check_game_ended(self):
        '''If there is a winner, returns the winner's player number, otherwise returns 0'''
        isWinner = 0
        for i in [0,1]:
            if self.players[i].check_winner():
                isWinner = i+1
                return isWinner
            elif self.players[i].check_loser():
                isWinner = 3 - (i+1)
                return isWinner
            else:
                isWinner = 0
        return isWinner
    
    def restart(self):
        """if player types in 'yes' then a new game begins with same command line areguments"""
        restartInput = input("Play again?\n")
        try:
            if restartInput == "yes":
                Menu(self._white_player_type, self._blue_player_type, "on" if self._undo_redo else "off", "on" if self._score_enable else "off").run()
            else:
                self._quit()
        except AttributeError:
            self._quit()

    def _quit(self):
        sys.exit(0)


if __name__ == "__main__":
    player_types = ["human", "random", "heuristic"]
    white_player_type = "human"
    blue_player_type = "human"
    enable_undo_redo = "off"
    enable_score = "off"

    if sys.argv[1:]:
        if sys.argv[1] in player_types:
            white_player_type = sys.argv[1]
        if sys.argv[2:]:
            if sys.argv[2] in player_types:
                blue_player_type = sys.argv[2]
            if sys.argv[3:]:
                if sys.argv[3] == "on":
                    enable_undo_redo = sys.argv[3]
                if sys.argv[4]:
                    if sys.argv[4] == "on":
                        enable_score = sys.argv[4]
    Menu(white_player_type, blue_player_type, enable_undo_redo, enable_score).run()