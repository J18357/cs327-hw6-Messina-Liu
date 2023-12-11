from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime


from tile import Tile
# from worker import Worker

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
        tile_to_update = self.tiles[tilePos[0]][tilePos[1]]
        tile_to_update.set_worker(worker)
    
    def update_tile_build(self, tilePos):
        tile_to_build = self.tiles[tilePos[0]][tilePos[1]]
        tile_to_build.incr_level()

    def get_otherPlayer_positions(self, worker1_pos, worker2_pos):
        otherPlayer_pos_lst = []
        for i in range(5):
            for j in range(5):
                if self.tiles[i][j].has_worker() and [i,j] != worker1_pos and [i,j] != worker2_pos:
                    otherPlayer_pos_lst.append([i,j])                
        return otherPlayer_pos_lst


    def save(self):
        """
        Saves the current state inside a memento.
        """
        return ConcreteMemento(self.deepcopy(self.tiles))

    def restore(self, memento: Memento):
        """
        Restores the Originator's state from a memento object.
        """

        self = memento #.get_state()
        # print(f"Originator: My state has changed to: {display_board(self.tiles)}")

    def deepcopy(self, tiles):
        copied_board = Board()

        for i in range(5):
            for j in range(5):
                copied_board.tiles[i][j].worker = tiles[i][j].worker
                copied_board.tiles[i][j].level = tiles[i][j].level

        return copied_board


class Memento(ABC):
    """
    The Memento interface provides a way to retrieve the memento's metadata,
    such as creation date or name. However, it doesn't expose the Originator's
    state.
    """

    @abstractmethod
    def get_date(self) -> str:
        pass


class ConcreteMemento(Memento):
    def __init__(self, state: Board):
        self._state = state
        # self._index = index
        self._date = str(datetime.now())[:19]

    def get_state(self) -> Board:
        """
        The Originator uses this method when restoring its state.
        """
        return self._state

    def get_date(self) -> str:
        return self._date


class Caretaker:
    """
    The Caretaker doesn't depend on the Concrete Memento class. Therefore, it
    doesn't have access to the originator's state, stored inside the memento. It
    works with all mementos via the base Memento interface.
    """

    def __init__(self, originator: Board):
        self._mementos = []
        self._originator = originator
        self._index = -1

    def save(self):
        # print("\nCaretaker: Saving Originator's state...")
        if len(self._mementos) - 1 > self._index:
            self._mementos[self._index + 1] = self._originator.save()
        else:
            self._mementos.append(self._originator.save())
        self._index += 1

    def undo(self):
        if not len(self._mementos) or len(self._mementos) == 1:
            return False

        memento = self._mementos[self._index - 1]
        self._index -= 1
        # print("this is memento")
        # self.show_board()
        # print(f"Caretaker: Restoring state to: {memento.get_date()}")
        self._originator.restore(memento)
        return True

    def redo(self):
        if self._index == len(self._mementos)-1:
            return False
        
        memento = self._mementos[self._index + 1]
        self._index += 1

        # print(f"Caretaker: Restoring state to: {memento.get_date()}")
        self._originator.restore(memento)
        return True
        

    def show_board(self):
        # print("Caretaker: Here's the list of mementos:")
        # for memento in self._mementos:
        # print(self._index)
        display_board(self._mementos[self._index].get_state())


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





# from tile import Tile

# class Board:
#     def __init__(self):

#         # initializing the tiles
#         self.tiles = []
#         for i in range(5):
#             row = []
#             for j in range(5):
#                 row.append(Tile())
#             self.tiles.append(row)
    
#     def update_tile(self, tilePos, worker=None):
#         tile_to_update = self.tiles[tilePos[0]][tilePos[1]]
#         tile_to_update.set_worker(worker)
    
#     def update_tile_build(self, tilePos):
#         tile_to_build = self.tiles[tilePos[0]][tilePos[1]]
#         tile_to_build.incr_level()

#     def get_otherPlayer_positions(self, worker1_pos, worker2_pos):
#         otherPlayer_pos_lst = []
#         for i in range(5):
#             for j in range(5):
#                 if self.tiles[i][j].has_worker() and [i,j] != worker1_pos and [i,j] != worker2_pos:
#                     otherPlayer_pos_lst.append([i,j])                
#         return otherPlayer_pos_lst
        