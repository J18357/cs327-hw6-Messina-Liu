from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from copy import deepcopy

from tile import Tile

# class Originator:
#     """
#     The Originator holds some important state that may change over time. It also
#     defines a method for saving the state inside a memento and another method
#     for restoring the state from it.
#     """
#     _state = None
#     """
#     For the sake of simplicity, the originator's state is stored inside a single
#     variable.
#     """

class Board:
    def __init__(self):

        # initializing the tiles
        self.tiles = []
        for i in range(5):
            row = []
            for j in range(5):
                row.append(Tile())
            self.tiles.append(row)

    def update_tile(self, tilePos, worker=None):
        """updates a tile's worker"""
        tile_to_update = self.tiles[tilePos[0]][tilePos[1]]
        tile_to_update.set_worker(worker)
    
    def update_tile_build(self, tilePos):
        """increases a tile's level"""
        tile_to_build = self.tiles[tilePos[0]][tilePos[1]]
        tile_to_build.incr_level()

    def get_otherPlayer_positions(self, worker1_pos, worker2_pos):
        """determines the position of the other player's workers [other_worker_1, other_worker_2]"""
        otherPlayer_pos_lst = []
        for i in range(5):
            for j in range(5):
                if self.tiles[i][j].has_worker() and [i,j] != worker1_pos and [i,j] != worker2_pos:
                    otherPlayer_pos_lst.append([i,j])                
        return otherPlayer_pos_lst


    def save(self):
        """Saves the current board inside a memento."""
        return ConcreteMemento(deepcopy(self))

    def restore(self, memento: Memento):
        """
        Restores the Originator's state from a memento object.
        """
        self.tiles = memento.get_state().tiles

    def display_board(board):
        for i in range(5):
            print("+--+--+--+--+--+")
            for j in range(5):
                print(f"|{board.tiles[i][j].level}",end='')
                if (board.tiles[i][j].has_worker() == False):
                    print(" ", end='')
                else:
                    print(f"{board.tiles[i][j].worker.get_letter()}",end='')

            print("|")
        print("+--+--+--+--+--+")


class Memento(ABC):
    """ The Memento interface provides a way to retrieve the memento's metadata, such
      as creation date or name. However, it doesn't expose the Originator's state."""

    @abstractmethod
    def get_date(self) -> str:
        pass


class ConcreteMemento(Memento):
    def __init__(self, state: Board):
        self._state = state
        self._date = str(datetime.now())[:19]

    def get_state(self) -> Board:
        """The Originator/Board uses this method when restoring its state."""
        return self._state

    def get_date(self) -> str:
        """returns the date of the memento's creation"""
        return self._date


class Caretaker:
    """The Caretaker doesn't depend on the Concrete Memento class. Therefore, it
    doesn't have access to the Boards's state, stored inside the memento. It
    works with all mementos via the base Memento interface."""

    def __init__(self, originator: Board):
        self._mementos = []
        self._originator = originator
        self._index = -1

    def save(self):
        """saves the board inside a list"""
        # remove any "future" backups since we changed the "history"
        while len(self._mementos) - 1 > self._index:
            self._mementos.pop()

        # appends the saved board to the front of the list
        self._mementos.append(self._originator.save())
        self._index += 1

    def undo(self):
        """goes to previous saved board, returns True if undo is successful"""

        # if there is no board that is previously saved, don't do anything
        if not len(self._mementos) or len(self._mementos) == 1:
            return False
        if self._index - 1 < 0:
            return False

        # gets previous backup board and updates the game's board
        memento = self._mementos[self._index - 1]
        self._index -= 1
        self._originator.restore(memento)
        return True

    def redo(self):
        """goes to future saved board, returns True if redo is successful"""

        # if there is no board that is in the future, don't do anythin
        if self._index == len(self._mementos)-1:
            return False
        
        # gets the future backup board and updates the game's board
        memento = self._mementos[self._index + 1]
        self._index += 1
        self._originator.restore(memento)
        return True
        

    def show_board(self):
        """display's the current board"""
        self._originator.display_board()