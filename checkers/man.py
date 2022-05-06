import pygame
from .piece import Piece
from .constants import AQUA, CRIMSON
from anytree import Node, PreOrderIter

class Man(Piece):
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        self._color = val

    @property
    def default_color(self):
        return self._default_color

    @default_color.setter
    def default_color(self, val):
        self._default_color = val

    def draw_piece(self, square, win):
        pygame.draw.ellipse(
            win,
            self._color,
            (square.x * square.size + square.size / 5,
            square.y * square.size + square.size / 5,
            square.size / 5 * 3,
            square.size / 5 * 3)
            )

    def get_possible_moves(self, y, x, board):
        root = None
        root = Node(str(y) + str(x))
        #Logika (for) - pokud ano, tak ->
        if board.squares[y][x].piece is not None:
            if self.default_color == AQUA:
                if x + 1 < 8:
                    if board.squares[y-1][x+1].piece is None:
                        new = Node(str(y-1) + str(x+1), parent=root)
                if y - 1 > -2:
                    if board.squares[y-1][x-1].piece is None and x-1 >= 0:
                        new = Node(str(y-1) + str(x-1), parent=root)
            if self.default_color == CRIMSON:
                if x + 1 < 8:
                    if board.squares[y+1][x+1].piece is None:
                        new = Node(str(y+1) + str(x+1), parent=root)
                if y - 1 > -2:
                    if board.squares[y+1][x-1].piece is None and x-1 >= 0:
                        new = Node(str(y+1) + str(x-1), parent=root)
            return [node.name for node in PreOrderIter(root)]