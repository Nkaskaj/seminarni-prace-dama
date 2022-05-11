import pygame
from .piece import Piece
from .constants import AQUA, CRIMSON, ROWS, COLS
from anytree import Node, PreOrderIter, RenderTree, search

class Man(Piece):
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        self._color = val

    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, val):
        self._team = val

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

    def get_possible_moves(self, y, x, board, despawning, end_check):
        despawn_check = 0
        right_node = False
        left_node = False
        root = Node(str(y) + str(x))
        root2 = Node(str(y) + str(x))
        if board.squares[y][x].piece is not None:
            if self.team == "w":
                if y - 1 >= 0 and x + 1 < COLS:
                    if board.squares[y-1][x+1].piece is None:
                        right_node = True
                    elif y - 2 >= 0 and x + 2 < COLS:
                        if board.squares[y-2][x+2].piece is None and board.squares[y-1][x+1].piece.team == "b":
                            Node(str(y-2) + str(x+2) + str(y-1) + str(x+1), parent=root)
                            Node(str(y-2) + str(x+2) + str(y-1) + str(x+1), parent=root2)
                            self.chaining(y-2, x+2, str(y-1) + str(x+1), board, root)

                if y - 1 >= 0 and x - 1 >= 0:
                    if board.squares[y-1][x-1].piece is None:
                        left_node = True
                    elif y - 2 >= 0 and x - 2 >= 0:
                        if board.squares[y-2][x-2].piece is None and board.squares[y-1][x-1].piece.team == "b":
                            Node(str(y-2) + str(x-2) + str(y-1) + str(x-1), parent=root)
                            Node(str(y-2) + str(x-2) + str(y-1) + str(x-1), parent=root2)
                            self.chaining(y-2, x-2, str(y-1) + str(x-1), board, root)

                if right_node and left_node == True:
                    Node(str(y-1) + str(x+1), parent=root)
                    Node(str(y-1) + str(x+1), parent=root2)
                    Node(str(y-1) + str(x-1), parent=root)
                    Node(str(y-1) + str(x-1), parent=root2)

                if root.is_leaf == True:
                    if right_node == True:
                        Node(str(y-1) + str(x+1), parent=root)
                        Node(str(y-1) + str(x+1), parent=root2)
                    elif left_node == True:
                        Node(str(y-1) + str(x-1), parent=root)
                        Node(str(y-1) + str(x-1), parent=root2)

            if self.team == "b":
                if y + 1 < ROWS and x + 1 < COLS:
                    if board.squares[y+1][x+1].piece is None:
                        right_node = True
                    elif y + 2 < ROWS and x + 2 < COLS:
                        if board.squares[y+2][x+2].piece is None and board.squares[y+1][x+1].piece.team == "w":
                            Node(str(y+2) + str(x+2) + str(y+1) + str(x+1), parent=root)
                            Node(str(y+2) + str(x+2) + str(y+1) + str(x+1), parent=root2)
                            self.chaining(y+2, x+2, str(y+1) + str(x+1),board, root)

                if y + 1 < ROWS and x - 1 >= 0:
                    if board.squares[y+1][x-1].piece is None:
                        left_node = True
                    elif y + 2 < ROWS and x - 2 >= 0:
                        if board.squares[y+2][x-2].piece is None and board.squares[y+1][x-1].piece.team == "w":
                            Node(str(y+2) + str(x-2) + str(y+1) + str(x-1), parent=root)
                            Node(str(y+2) + str(x-2) + str(y+1) + str(x-1), parent=root2)
                            self.chaining(y+2, x-2, str(y+1) + str(x-1), board, root)

                    if right_node and left_node == True:
                        Node(str(y+1) + str(x+1), parent=root)
                        Node(str(y+1) + str(x+1), parent=root2)
                        Node(str(y+1) + str(x-1), parent=root)
                        Node(str(y+1) + str(x-1), parent=root2)
                    
                    if root.is_leaf == True:
                        if right_node == True:
                            Node(str(y+1) + str(x+1), parent=root)
                            Node(str(y+1) + str(x+1), parent=root2)
                        elif left_node == True:
                            Node(str(y+1) + str(x-1), parent=root)
                            Node(str(y+1) + str(x-1), parent=root2)

            print(RenderTree(root))
            print(RenderTree(root2))

            possible_moves=[]
            s = str(root2.leaves)
            for i in range(s.count("')")):
                sub = s.find("')")
                if(s[sub-3:sub-2]) == "/":
                    possible_moves.append(s[sub-2:sub])
                else:
                    possible_moves.append(s[sub-4:sub-2])
                    if despawn_check == 0 and despawning == s[sub-4:sub-2]:
                        despawn_check = 1
                        despawning = despawning + (s[sub-2:sub])
                s = s[sub+1:]
            print(str(possible_moves))
            possible_end_moves=[]
            if root.is_leaf == False:
                possible_end_moves.append(str(y) + str(x))
            s = str(root.leaves)
            for i in range(s.count("')")):
                sub = s.find("')")
                if(s[sub-3:sub-2]) == "/":
                    possible_end_moves.append(s[sub-2:sub])
                else:
                    possible_end_moves.append(s[sub-4:sub-2])
                    if despawn_check == 0 and despawning == s[sub-4:sub-2]:
                        despawn_check = 1
                        despawning = despawning + (s[sub-2:sub])
                s = s[sub+1:]

            if despawning is not None:
                killed = []
                s = str(search.find_by_attr(root, despawning))
                for i in range(s.count("/")):
                    sub = s.find("/")
                    if "/" not in s[sub+1:sub+5]:
                        if ")" not in s[sub+1:sub+5]:
                            killed.append((s[sub+3:sub+5]))
                    s = s[sub+1:] 
                return killed
            if end_check == True:
                print("POS-END-MOV: " + str(possible_end_moves))
                return possible_end_moves
            else:
                print("POS-MOV: " + str(possible_moves))
                return possible_moves
        
    def chaining(self, y, x, last_killed, board, root):
        fronta=[]
        fronta.append(str(y) + str(x) + last_killed)
        while fronta:
            y = int(fronta[0][0])
            x = int(fronta[0][1])
            if self.team == "w":
                if y - 2 >= 0 and x + 2 < COLS and board.squares[y-1][x+1].piece is not None:
                    if board.squares[y-2][x+2].piece is None and board.squares[y-1][x+1].piece.team == "b":
                        Node(str(y-2) + str(x+2) + str(y-1) + str(x+1), parent=search.find_by_attr(root, str(y) + str(x) + fronta[0][2:4]))
                        fronta.append(str(y-2) + str(x+2) + str(y-1) + str(x+1))

                if y - 2 >= 0 and x - 2 >= 0 and board.squares[y-1][x-1].piece is not None:
                    if board.squares[y-2][x-2].piece is None and board.squares[y-1][x-1].piece.team == "b":
                        Node(str(y-2) + str(x-2) + str(y-1) + str(x-1), parent=search.find_by_attr(root, str(y) + str(x) + fronta[0][2:4]))
                        fronta.append(str(y-2) + str(x-2) + str(y-1) + str(x-1))

            if self.team == "b":
                if y + 2 < ROWS and x + 2 < COLS and board.squares[y+1][x+1].piece is not None:
                    if board.squares[y+2][x+2].piece is None and board.squares[y+1][x+1].piece.team == "w":
                        Node(str(y+2) + str(x+2) + str(y+1) + str(x+1), parent=search.find_by_attr(root, str(y) + str(x) + fronta[0][2:4]))
                        fronta.append(str(y+2) + str(x+2) + str(y+1) + str(x+1))

                if y + 2 < ROWS and x - 2 >= 0 and board.squares[y+1][x-1].piece is not None:
                    if board.squares[y+2][x-2].piece is None and board.squares[y+1][x-1].piece.team == "w":
                        Node(str(y+2) + str(x-2) + str(y+1) + str(x-1), parent=search.find_by_attr(root, str(y) + str(x) + fronta[0][2:4]))
                        fronta.append(str(y+2) + str(x-2) + str(y+1) + str(x-1))

            fronta.pop(0)