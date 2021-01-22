import kivy
# kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scatter import Scatter
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from .board import Board
from .piece import Piece
from .iqfit import IQFIT
import time
import pprint as pp


class IQFITApp(App):

    def build(self):
        main_window = FloatLayout(size=(500, 500))

        title_label = Label(text="IQFIT solver",size_hint=(.5, .25),pos_hint= {'center_y': 0.95, 'center_x': 0.5})
        main_window.add_widget(title_label)

        iqfit_pieces = Piece.iqfit_pieces()

        pieces_grid = PiecesGrid(pieces=iqfit_pieces,cols=2,rows=len(iqfit_pieces)//2,size_hint=(.3, .7),pos_hint= {'center_y': 0.4, 'center_x': 0.8})
        main_window.add_widget(pieces_grid)

        board_grid = BoardGrid(pieces=pieces_grid,cols=10,rows=5,spacing=2,size_hint=(.55, .55),pos_hint= {'center_y': 0.4, 'center_x': 0.325})
        main_window.add_widget(board_grid)
        

        return main_window

class PieceButton(ToggleButton):
        def __init__(self,piece:Piece, **kwargs):
                super(PieceButton,self).__init__(**kwargs)
                self.piece = [Piece(piece.name,coords) for coords in piece.get_transformations()]
                self.name = piece.name

class PiecesGrid(GridLayout):

    def __init__(self,pieces, **kwargs):
        super(PiecesGrid, self).__init__(**kwargs)
        for piece in pieces:
            piece_button = PieceButton(text=piece,piece=pieces[piece],group="iqfit_pieces",background_down="")
            piece_button.bind(on_press = self.piece_selection)
            self.add_widget(piece_button)
            self.selected = None
            self.iqfit_pieces = pieces
            

    def piece_selection(self,piece_button):
        iqfit_pieces = Piece.iqfit_pieces()
        if piece_button == self.selected:
            self.selected = None
            piece_button.background_color = (1,1,1,1)
        else:
            if self.selected is not None : self.selected.background_color = (1,1,1,1)
            self.selected = piece_button
            piece_button.background_color = piece_button.name.lower()


        

class BoardGrid(GridLayout):
    def __init__(self,pieces:PiecesGrid, **kwargs):
        super(BoardGrid, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        self.grid = {}
        self.invgrid = {}
        self.pieces = pieces
        self.rotation = 0

        for i in range(self.rows*self.cols):
            board_button = Button(text=f"{i}",border=(25,25,25,25))
            board_button.bind(on_press=self.select_piece)
            self.grid[board_button]={"id":i,"hovered":False,"border_point ":None,"selected":None}
            self.invgrid[i] = board_button
            self.add_widget(board_button)

    def on_mouse_pos(self, window, pos):
        # print(self.grid.keys())
        for board_button in self.grid.keys():
            inside = board_button.collide_point(*pos)
            if self.grid[board_button]["hovered"] == inside:
                continue
            self.grid[board_button]["border_point"] = pos
            self.grid[board_button]["hovered"] = inside
            if inside:
                self.dispatch('on_enter',board_button)
            else:
                self.dispatch('on_leave',board_button)

    
    def on_enter(self,board_button):
        print(f"On enter {board_button.text}")
        if self.pieces.selected is None:
            return
        else:
            col,row = self.grid[board_button]["id"]%self.cols,self.grid[board_button]["id"]//self.cols
            selected_name = self.pieces.selected.text
            selected_coords = self.pieces.iqfit_pieces[selected_name].get_transformations_2D()[self.rotation]
            selected_grid_coords=set(self.grid[board_button]["id"]+x+self.cols*y if col+x<=self.cols-1  else self.rows*self.cols+1 for x,y in selected_coords)
            if selected_grid_coords.issubset(self.invgrid.keys()):
                for id_ in selected_grid_coords:
                    if self.grid[self.invgrid[id_]]["selected"] is None:
                        self.invgrid[id_].background_color=selected_name.lower()
        pass

    def on_leave(self,board_button):
        print(f"On leave {board_button.text}")
        if self.pieces.selected is None:
            return
        else:
            col,row = self.grid[board_button]["id"]%self.cols,self.grid[board_button]["id"]//self.cols
            selected_name = self.pieces.selected.text
            selected_coords = self.pieces.iqfit_pieces[selected_name].get_transformations_2D()[self.rotation]
            selected_grid_coords=set(self.grid[board_button]["id"]+x+self.cols*y if col+x<=self.cols-1  else self.rows*self.cols+1 for x,y in selected_coords)
            if selected_grid_coords.issubset(self.invgrid.keys()):
                for id_ in selected_grid_coords:
                        if self.grid[self.invgrid[id_]]["selected"] is None:
                            self.invgrid[id_].background_color=(1,1,1,1)

    def select_piece(self,board_button):
        if self.pieces.selected is None:
            return
        else:
            col,row = self.grid[board_button]["id"]%self.cols,self.grid[board_button]["id"]//self.cols
            selected_name = self.pieces.selected.name
            selected_coords = self.pieces.iqfit_pieces[selected_name].get_transformations_2D()[self.rotation]
            selected_grid_coords=set(self.grid[board_button]["id"]+x+self.cols*y if col+x<=self.cols-1  else self.rows*self.cols+1 for x,y in selected_coords)
            if selected_grid_coords.issubset(self.invgrid.keys()):
                for id_ in selected_grid_coords:
                    selected_button = self.invgrid[id_]
                    if self.grid[selected_button]["selected"] is not None:
                        return
                    self.grid[selected_button]["selected"] = self.pieces.selected.piece[self.rotation]
        pass

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if text == "r":
            self.rotation=(self.rotation+1)%8
        if text=="s":
            pp.pprint(self.pieces_on_board())
    def pieces_on_board(self):
        return set(b["selected"].name for _,b in self.grid.items() if b["selected"] is not None)
