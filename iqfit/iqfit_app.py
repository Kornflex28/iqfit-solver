import kivy
# kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scatter import Scatter
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Rectangle

from .board import Board
from .piece import Piece
from .iqfit import IQFIT
import time
import pprint as pp


class IQFITApp(App):

    def build(self):
        main_window = FloatLayout(size=(1920, 1080))

        with main_window.canvas:
            self.rect = Rectangle(source='./images/background.png',size=main_window.size)

        logo = Image(source ='./images/logo.png',size_hint=(0.1,0.1),pos_hint= {'center_y': 0.9, 'center_x': 0.1})
        main_window.add_widget(logo)

        title_label = Label(text="IQFIT solver",font_size='30sp',bold=True,valign='middle',size_hint=(.5, .25),pos_hint= {'center_y': 0.95, 'center_x': 0.5})
        main_window.add_widget(title_label)

        instructions_label = Label(text="Select pieces and place them on the board.\nPress R to rotate pieces (in 2D and 3D)\nWhen done press Solve to see solution.",font_size='20sp',bold=True,halign='left',valign='middle',size_hint=(.5, .25),pos_hint= {'center_y': 0.75, 'center_x': 0.3})
        main_window.add_widget(instructions_label)

        iqfit_pieces = Piece.iqfit_pieces()

        pieces_grid = PiecesGrid(pieces=iqfit_pieces,cols=2,rows=len(iqfit_pieces)//2,size_hint=(.3, .7),pos_hint= {'center_y': 0.4, 'center_x': 0.8})
        self.pieces_grid = pieces_grid
        main_window.add_widget(pieces_grid)

        board_grid = BoardGrid(pieces=pieces_grid,cols=10,rows=5,spacing=2,size_hint=(.55, .55),pos_hint= {'center_y': 0.4, 'center_x': 0.325})
        self.board_grid = board_grid
        main_window.add_widget(board_grid)

        clear_button = Button(text="Clear board",size_hint=(.15, .08),pos_hint= {'center_y': 0.05, 'center_x': 0.5},background_color="red")
        clear_button.bind(on_press = self.clear_board)
        main_window.add_widget(clear_button)

        solve_button = Button(text="Solve board",size_hint=(.15, .08),pos_hint= {'center_y': 0.05, 'center_x': 0.3},background_color="green")
        solve_button.bind(on_press = self.solve_board)
        main_window.add_widget(solve_button)
    
        return main_window

    def clear_board(self,clear_button=None):
        for board_button in self.board_grid.grid:
            self.board_grid.grid[board_button]["selected"] = None
            board_button.background_color=(1,1,1,1)
        pass

    def solve_board(self,solve_button=None):
        init_pieces = {}
        for board_button in self.board_grid.grid:
            grid_spot = self.board_grid.grid[board_button]
            selected_piece = grid_spot["selected"]
            if selected_piece is not None:
                col,row = grid_spot["id"]%self.board_grid.cols,grid_spot["id"]//self.board_grid.cols
                if selected_piece not in init_pieces:
                    init_pieces[selected_piece]=(row,col)
                else :
                    init_pieces[selected_piece]=(min(init_pieces[selected_piece][0],row),min(init_pieces[selected_piece][1],col))

        init_board = Board(self.board_grid.cols,self.board_grid.rows)
        for i_piece,(dy,dx) in init_pieces.items():
            init_board.put_piece_on_board(i_piece.translate_piece(dx,dy))

        pb = IQFIT(init_board,Piece.iqfit_pieces())
        final_board = pb.get_final_board()

        self.clear_board()
        for (x,y),p_name in final_board.current_board.items():
            b_id = x+y*self.board_grid.cols
            self.board_grid.invgrid[b_id].background_color=p_name.lower()

        pass

class PieceButton(ToggleButton):
        def __init__(self,piece:Piece, **kwargs):
                super(PieceButton,self).__init__(**kwargs)
                self.piece = [Piece(piece.name,coords) for coords in piece.get_transformations()]
                self.name = piece.name

class PiecesGrid(GridLayout):

    def __init__(self,pieces, **kwargs):
        super(PiecesGrid, self).__init__(**kwargs)
        for piece in pieces:
            piece_button = PieceButton(piece=pieces[piece],group="iqfit_pieces",background_normal=f"./images/iqfit-pieces/{piece}.png",background_down=f"./images/iqfit-pieces/{piece}")
            piece_button.bind(on_press = self.piece_selection)
            self.add_widget(piece_button)
            self.selected = None
            self.iqfit_pieces = pieces
            

    def piece_selection(self,piece_button):
        iqfit_pieces = Piece.iqfit_pieces()
        color_map = {"Blue": [0.0, 0.0, 1.0, .1],
                    "Yellow": [1.0, 1.0, 0.0, .1],
                    "Red": [1.0, 0.0, 0.0, .1],
                    "DeepSkyBlue": [0.0, 0.7490196078431373, 1.0, .1],
                    "Magenta": [1.0, 0.0, 1.0, 1.0],
                    "Orange": [1.0, 0.6470588235294118, 0.0, .1],
                    "Lime": [0.0, 1.0, 0.0, 1.0],
                    "Green": [0.0, 0.5019607843137255, 0.0, .1],
                    "Cyan": [0.0, 1.0, 1.0, 1.0],
                    "Purple": [0.5019607843137255, 0.0, 0.5019607843137255, .1]
                    }
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
            board_button = Button()
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
        # print(f"On enter {board_button.text}")
        if self.pieces.selected is None:
            return
        else:
            col,row = self.grid[board_button]["id"]%self.cols,self.grid[board_button]["id"]//self.cols
            selected_name = self.pieces.selected.name
            selected_coords = self.pieces.iqfit_pieces[selected_name].get_transformations_2D()[self.rotation]
            selected_grid_coords=set(self.grid[board_button]["id"]+x+self.cols*y if col+x<=self.cols-1  else self.rows*self.cols+1 for x,y in selected_coords)
            if selected_grid_coords.issubset(self.invgrid.keys()):
                for id_ in selected_grid_coords:
                    if self.grid[self.invgrid[id_]]["selected"] is None:
                        self.invgrid[id_].background_color=selected_name.lower()
        pass

    def on_leave(self,board_button):
        # print(f"On leave {board_button.text}")
        if self.pieces.selected is None:
            return
        else:
            col,row = self.grid[board_button]["id"]%self.cols,self.grid[board_button]["id"]//self.cols
            selected_name = self.pieces.selected.name
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
