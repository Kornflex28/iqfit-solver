from itertools import product
from .piece import Piece

class Board:
    def __init__(self, width=10,height=5):
        self.width = width
        self.height = height
        self.shape = width,height
        self.current_board = {(x,y):None for x,y in product(range(self.width),range(self.height))}
        self.coordinates = set(self.current_board.keys())

    def __str__(self):
        rep = f"Board(width={self.width}, height={self.height})"
        for y in range(self.height):
            rep += "\n"
            for x in range(self.width):
                if self.current_board[(x,y)] is not None:
                    rep+=self.current_board[(x,y)][0]
                else :
                    rep+="*"
        return rep
        
    def __repr__(self):
        return f"Board(width={self.width}, height={self.height})"

    def get_empty_coordinates(self):
        return {(x,y) for (x,y),p in self.current_board.items() if p is None}

    def translate_piece(self,dx,dy,piece:Piece):
        return Piece(piece.name,{(x+dx,y+dy,z) for x,y,z in piece.coordinates})

    def get_piece_coordinates(self,piece:Piece):
        return

    def put_piece_on_board(self,piece:Piece):
        if piece.get_2D_coordinates().issubset(self.get_empty_coordinates()):
            for x,y in piece.get_2D_coordinates():
                self.current_board[(x,y)]=piece.name
        return self
    