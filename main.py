from iqfit.board import Board
from iqfit.piece import Piece
from iqfit.iqfit import IQFIT
import pprint as pp
import numpy as np


if __name__ == "__main__":
    board = Board(10, 5)
    iqfit_pieces = Piece.iqfit_pieces()
    green = Piece("Green",iqfit_pieces["Green"].get_transformations()[1])
    blue = Piece("Blue",iqfit_pieces["Blue"].get_transformations()[6])
    sky = Piece("Sky",iqfit_pieces["Sky"].get_transformations()[0])
    orange = Piece("Orange",iqfit_pieces["Orange"].get_transformations()[0])
    board.put_piece_on_board(green)
    board.put_piece_on_board(blue.translate_piece(2,2))
    board.put_piece_on_board(sky.translate_piece(5,2))
    board.put_piece_on_board(orange.translate_piece(dx=6))


    pb = IQFIT(board,iqfit_pieces)

    final_board = pb.get_final_board()
    print(pb.init_board)
    print(final_board)