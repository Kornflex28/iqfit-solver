from .board import Board
from .piece import Piece
import copy


class IQFIT:
    def __init__(self, init_board=Board(10, 5), pieces=Piece.iqfit_pieces()):
        self.init_board = init_board
        self.available_pieces = set(
            pieces)-set(init_board.current_board.values())
        self.iqfit_pieces = Piece.iqfit_pieces()

    def __repr__(self):
        return f"Problem(init_board={self.init_board.__repr__()},pieces={self.available_pieces})"

    def __str__(self):
        return f"Problem:\n--------\n{self.init_board}\n--------\nPieces available: {self.available_pieces})"

    def get_solutions(self):

        def select(X, coordinates_map, r):
            cols = []
            for j in coordinates_map[r]:
                for i in X[j]:
                    for k in coordinates_map[i]:
                        if k != j:
                            X[k].remove(i)
                cols.append(X.pop(j))
            return cols

        def deselect(X, coordinates_map, r, cols):
            for j in reversed(coordinates_map[r]):
                X[j] = cols.pop()
                for i in X[j]:
                    for k in coordinates_map[i]:
                        if k != j:
                            X[k].add(i)

        def solve(X, coordinates_map, solution=[]):
            if not X:
                yield list(solution)
            else:
                c = min(X, key=lambda c: len(X[c]))
                for r in list(X[c]):
                    solution.append(r)
                    cols = select(X, coordinates_map, r)
                    for s in solve(X, coordinates_map, solution):
                        yield s
                    deselect(X, coordinates_map, r, cols)
                    solution.pop()

        coordinates_map = {}
        idx = 0
        for i,p_name in enumerate(self.available_pieces):
            for j,piece in enumerate(self.init_board.get_possible_coordinates(self.iqfit_pieces[p_name])):
                coordinates_map[idx]=[p_name]+list(piece.get_2D_coordinates())
                idx+=1
        
        X = self.init_board.get_empty_coordinates().union(self.available_pieces)
        X = {j: set() for j in X}
        for i in coordinates_map:
            for j in coordinates_map[i]:
                X[j].add(i)

        print("Solving problem...")
        return solve(X,coordinates_map),coordinates_map
    
    def get_final_board(self):
        solutions,coordinates_map = self.get_solutions()
        sol = next(solutions)
        final_board = copy.deepcopy(self.init_board)
        for p in sol:
            final_board.from_2D_put_piece_on_board(coordinates_map[p][0],set(coordinates_map[p][1:]))
        return final_board