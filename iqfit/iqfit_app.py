import kivy
# kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from .board import Board
from .piece import Piece
from .iqfit import IQFIT


class IQFITApp(App):

    def build(self):
        main_window = FloatLayout(size=(500, 500))

        button = Label(text="IQFIT solver",size_hint=(.5, .25),pos_hint= {'center_y': 0.95, 'center_x': 0.5})
        main_window.add_widget(button)

        iqfit_pieces = Piece.iqfit_pieces()

        pieces_grid = PiecesGrid(pieces=iqfit_pieces,cols=2,rows=len(iqfit_pieces)//2,size_hint=(.3, .7),pos_hint= {'center_y': 0.4, 'center_x': 0.8})
        main_window.add_widget(pieces_grid)

        board_grid = BoardGrid(cols=10,rows=5,size_hint=(.55, .55),pos_hint= {'center_y': 0.4, 'center_x': 0.325})
        main_window.add_widget(board_grid)
        

        return main_window

class PiecesGrid(GridLayout):
    def __init__(self,pieces, **kwargs):
        super(PiecesGrid, self).__init__(**kwargs)
        for piece in pieces:
            piece_button = Button(text=piece)
            piece_button.bind(on_press = self.piece_selection)
            self.add_widget(piece_button)
            

    def piece_selection(self,instance):
        iqfit_pieces = Piece.iqfit_pieces()
        print(iqfit_pieces[instance.text])

class BoardGrid(GridLayout):
    def __init__(self, **kwargs):
        super(BoardGrid, self).__init__(**kwargs)
        self.grid = {}
        for i in range(self.rows*self.cols):
            piece_button = Button(text=f"{i}")
            piece_button.bind(on_press = self.piece_selection)
            self.grid[piece_button]=i
            self.add_widget(piece_button)
            

    def piece_selection(self,instance):
        iqfit_pieces = Piece.iqfit_pieces()
        print(self.grid[instance])

