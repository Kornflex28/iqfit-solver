from iqfit.board import Board
from iqfit.piece import Piece
import pprint as pp
import numpy as np

if __name__ == "__main__":
    b = Board(4,4)
    pieces = [Piece("Blue",{(0,0,0),(0,0,1),(1,0,0),(2,0,0),(2,0,1),(1,1,0)}),
              Piece("Yellow",{(0,0,0),(0,0,1),(1,0,0),(2,0,0),(3,0,0),(2,1,0),(3,1,0)}),
              Piece("Red",{(0,0,0),(0,0,1),(1,0,0),(2,0,0),(3,0,0),(3,0,1),(0,1,0)}),
              Piece("Sky",{(0,0,0),(0,0,1),(1,0,0),(2,0,0),(2,0,1),(3,0,0),(0,1,0)}),
              Piece("Magenta",{(0,0,0),(1,0,0),(1,0,1),(2,0,0),(3,0,0),(0,1,0),(1,1,0)}),
              Piece("Orange",{(0,0,0),(1,0,0),(1,0,1),(2,0,0),(3,0,0),(3,0,1),(1,1,0)}),
              Piece("Green",{(0,0,0),(0,0,1),(1,0,0),(2,0,0),(2,0,1),(0,1,0)}),
              Piece("Forest",{(0,0,0),(1,0,0),(1,0,1),(2,0,0),(2,0,1),(1,1,0)}),
              Piece("Cyan",{(0,0,0),(1,0,0),(1,0,1),(2,0,0),(2,0,1),(3,0,0),(1,1,0)}),
              Piece("Purple",{(0,0,0),(0,0,1),(1,0,0),(1,0,1),(2,0,0),(2,1,0)})
    ]
    for p in pieces:
        print(p)
        # pp.pprint(p.to_array()[:,:,0])
    # a = p.to_array()
    # a_rot = Piece.from_array_rotate_3D(a)
    # print("z=0")
    # print(a[:,:,0])
    # print("z=1")
    # print(a[:,:,1])
    # print("\nz=0")
    # print(a_rot[:,:,0])
    # print("z=1")
    # print(a_rot[:,:,1])
    # print("\nz=0")
    # print(Piece.from_array_rotate_3D(a_rot)[:,:,0])
    # print("z=1")
    # print(Piece.from_array_rotate_3D(a_rot)[:,:,1])
