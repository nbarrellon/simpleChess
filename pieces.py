# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 18:01:16 2021

@author: matisse
"""

import board, ia

class Piece():

    BLANC = "B"
    NOIR = "N"

    def __init__(self, x, y, color, piece_type, value):
        self.x = x
        self.y = y
        self.color = color
        self.piece_type = piece_type
        self.value = value

    # Retourne tous les mouvements diagonaux pour cette pièce. Ceci ne devrait donc
    # être utilisé que par le Fou
    def get_possible_diagonal_moves(self, board):
        moves = []

        for i in range(1, 8):
            if (not board.in_bounds(self.x+i, self.y+i)):
                break
            piece = board.get_piece(self.x+i, self.y+i)
            moves.append(self.get_move(board, self.x+i, self.y+i))
            if (piece != 0):
                break

        for i in range(1, 8):
            if (not board.in_bounds(self.x+i, self.y-i)):
                break

            piece = board.get_piece(self.x+i, self.y-i)
            moves.append(self.get_move(board, self.x+i, self.y-i))
            if (piece != 0):
                break

        for i in range(1, 8):
            if (not board.in_bounds(self.x-i, self.y-i)):
                break

            piece = board.get_piece(self.x-i, self.y-i)
            moves.append(self.get_move(board, self.x-i, self.y-i))
            if (piece != 0):
                break

        for i in range(1, 8):
            if (not board.in_bounds(self.x-i, self.y+i)):
                break

            piece = board.get_piece(self.x-i, self.y+i)
            moves.append(self.get_move(board, self.x-i, self.y+i))
            if (piece != 0):
                break

        return self.remove_null_from_list(moves)

        # Un déplacement n'est pas valide s'il est hors limites, ou si une pièce de la même couleur est
        # en train d'être mangée.
    def get_move(self, board, xto, yto):
        move = 0
        if (board.in_bounds(xto, yto)):
            piece = board.get_piece(xto, yto)
            if (piece != 0):
                if (piece.color != self.color):
                    move = ia.Move(self.x, self.y, xto, yto, False)
            else:
                move = ia.Move(self.x, self.y, xto, yto, False)
        return move

    # Retourne la liste des coups débarrassés de tous les 0.
    def remove_null_from_list(self, l):
        return [move for move in l if move != 0]

    def to_string(self):
        return self.color + self.piece_type + " "


class Cavalier(Piece):

    PIECE_TYPE = "C"
    VALUE = 320

    def __init__(self, x, y, color):
        super(Cavalier, self).__init__(x, y, color, Cavalier.PIECE_TYPE, Cavalier.VALUE)

    def get_possible_moves(self, board):
        moves = []

        moves.append(self.get_move(board, self.x+2, self.y+1))
        moves.append(self.get_move(board, self.x-1, self.y+2))
        moves.append(self.get_move(board, self.x-2, self.y+1))
        moves.append(self.get_move(board, self.x+1, self.y-2))
        moves.append(self.get_move(board, self.x+2, self.y-1))
        moves.append(self.get_move(board, self.x+1, self.y+2))
        moves.append(self.get_move(board, self.x-2, self.y-1))
        moves.append(self.get_move(board, self.x-1, self.y-2))

        return self.remove_null_from_list(moves)

    def clone(self):
        return Cavalier(self.x, self.y, self.color)


class Fou(Piece):

    PIECE_TYPE = "F"
    VALUE = 330

    def __init__(self, x, y, color):
        super(Fou, self).__init__(x, y, color, Fou.PIECE_TYPE, Fou.VALUE)

    def get_possible_moves(self, board):
        return self.get_possible_diagonal_moves(board)

    def clone(self):
        return Fou(self.x, self.y, self.color)

class King(Piece):

    PIECE_TYPE = "K"
    VALUE = 20000

    def __init__(self, x, y, color):
        super(King, self).__init__(x, y, color, King.PIECE_TYPE, King.VALUE)

    def get_possible_moves(self, board):
        moves = []

        moves.append(self.get_move(board, self.x+1, self.y))
        moves.append(self.get_move(board, self.x+1, self.y+1))
        moves.append(self.get_move(board, self.x, self.y+1))
        moves.append(self.get_move(board, self.x-1, self.y+1))
        moves.append(self.get_move(board, self.x-1, self.y))
        moves.append(self.get_move(board, self.x-1, self.y-1))
        moves.append(self.get_move(board, self.x, self.y-1))
        moves.append(self.get_move(board, self.x+1, self.y-1))

        moves.append(self.get_top_castling_move(board))
        moves.append(self.get_bottom_castling_move(board))

        return self.remove_null_from_list(moves)

    def get_top_castling_move(self, board):
        if (self.color == Piece.BLANC and board.white_king_moved):
            return 0
        if (self.color == Piece.NOIR and board.black_king_moved):
            return 0

        piece = board.get_piece(self.x, self.y-3)
        

        return 0

    def get_bottom_castling_move(self, board):
        if (self.color == Piece.BLANC and board.white_king_moved):
            return 0
        if (self.color == Piece.NOIR and board.black_king_moved):
            return 0

        piece = board.get_piece(self.x, self.y+4)
        
        return 0


    def clone(self):
        return King(self.x, self.y, self.color)