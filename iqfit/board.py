from itertools import product
from .piece import Piece

class Board:
    def __init__(self, width=10,height=5):
        self.width = width
        self.height = height
        self.shape = width,height

    def __str__(self):
        return f"Board(width={self.width}, height={self.height})"
        
    def __repr__(self):
        return f"Board(width={self.width}, height={self.height})"

    def get_coordinates(self):
        return set(product(range(self.width),range(self.height)))

    def get_piece_coordinates(self,piece:Piece):
        return