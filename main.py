from iqfit.board import Board
from iqfit.piece import Piece
import pprint as pp
import numpy as np

if __name__ == "__main__":
    board = Board(2, 5)
    print(board)
    pieces = Piece.iqfit_pieces()
    blue = pieces["Blue"]