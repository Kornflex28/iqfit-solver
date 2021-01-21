from itertools import product
from .piece import Piece


class Board:
    def __init__(self, width=10, height=5):
        self.width = width
        self.height = height
        self.shape = width, height
        self.current_board = {(x, y): None for x, y in product(
            range(self.width), range(self.height))}
        self.coordinates = set(self.current_board.keys())

    def __str__(self):
        rep = f"Board(width={self.width}, height={self.height})"
        for y in range(self.height):
            rep += "\n"
            for x in range(self.width):
                if self.current_board[(x, y)] is not None:
                    rep += self.current_board[(x, y)][0]
                else:
                    rep += "*"
        return rep

    def __repr__(self):
        return f"Board(width={self.width}, height={self.height})"

    def get_empty_coordinates(self):
        return {(x, y) for (x, y), p in self.current_board.items() if p is None}

    def put_piece_on_board(self, piece: Piece):
        if piece.get_2D_coordinates().issubset(self.get_empty_coordinates()):
            for x, y in piece.get_2D_coordinates():
                self.current_board[(x, y)] = piece.name
        else:
            print(f"Piece {piece.name} can't fit on board.")
        return self.current_board

    def from_2D_put_piece_on_board(self, name,coords_2D):
        if coords_2D.issubset(self.get_empty_coordinates()):
            for x, y in coords_2D:
                self.current_board[(x, y)] = name
        else:
            print(f"Piece {name} can't fit on board.")
        return self.current_board

    def get_possible_coordinates(self, piece: Piece):
        piece_transfomartions = piece.get_transformations()
        possible_coordinates = []
        for coords in piece_transfomartions:
            p = Piece(piece.name, coords)
            for dx in range(self.width-p.width+1):
                for dy in range(self.height-p.height+1):
                    dp = p.translate_piece(dx, dy)
                    dp_2D_coords = dp.get_2D_coordinates()
                    if dp_2D_coords.issubset(self.get_empty_coordinates()) and dp not in possible_coordinates:
                        possible_coordinates.append(dp)
        return possible_coordinates

