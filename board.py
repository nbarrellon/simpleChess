# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 18:03:10 2021

@author: matisse
"""

import pieces, ia

class Board:

    WIDTH = 8
    HEIGHT = 8

    def __init__(self, chesspieces, white_king_moved, black_king_moved):
        self.chesspieces = chesspieces
        self.white_king_moved = white_king_moved
        self.black_king_moved = black_king_moved

    @classmethod
    def clone(cls, chessboard):
        chesspieces = [[0 for x in range(Board.WIDTH)] for y in range(Board.HEIGHT)]
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = chessboard.chesspieces[x][y]
                if (piece != 0):
                    chesspieces[x][y] = piece.clone()
        return cls(chesspieces, chessboard.white_king_moved, chessboard.black_king_moved)

    @classmethod
    def new(cls):
        chess_pieces = [[0 for x in range(Board.WIDTH)] for y in range(Board.HEIGHT)]    
        # Creation du Cavalier noir
        chess_pieces[Board.WIDTH-2][0] = pieces.Cavalier(Board.WIDTH-2, 0, pieces.Piece.NOIR)

        # Creation du Fou noir
        chess_pieces[Board.WIDTH-3][0] = pieces.Fou(Board.WIDTH-3, 0, pieces.Piece.NOIR)

        # Creation des deux rois 
        chess_pieces[4][Board.HEIGHT-1] = pieces.King(4, Board.HEIGHT-1, pieces.Piece.BLANC)
        chess_pieces[4][0] = pieces.King(4, 0, pieces.Piece.NOIR)
       

        return cls(chess_pieces, False, False)

    def get_possible_moves(self, color):
        moves = []
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = self.chesspieces[x][y]
                if (piece != 0):
                    if (piece.color == color):
                        moves += piece.get_possible_moves(self)

        return moves

    def perform_move(self, move):
        piece = self.chesspieces[move.xfrom][move.yfrom]
        piece.x = move.xto
        piece.y = move.yto
        self.chesspieces[move.xto][move.yto] = piece
        self.chesspieces[move.xfrom][move.yfrom] = 0

       


        if (piece.piece_type == pieces.King.PIECE_TYPE):
            if (piece.color == pieces.Piece.BLANC):
                self.white_king_moved = True
            else:
                self.black_king_moved = True

    # Retourne si la couleur donnée est cochée.
    def is_check(self, color):
        other_color = pieces.Piece.BLANC
        if (color == pieces.Piece.BLANC):
            other_color = pieces.Piece.NOIR

        for move in self.get_possible_moves(other_color):
            copy = Board.clone(self)
            copy.perform_move(move)

            king_found = False
            for x in range(Board.WIDTH):
                for y in range(Board.HEIGHT):
                    piece = copy.chesspieces[x][y]
                    if (piece != 0):
                        if (piece.color == color and piece.piece_type == pieces.King.PIECE_TYPE):
                            king_found = True

            if (not king_found):
                return True

        return False

    # Retourne la pièce à la position donnée ou 0 si : Pas de pièce ou hors limites.
    def get_piece(self, x, y):
        if (not self.in_bounds(x, y)):
            return 0

        return self.chesspieces[x][y]

    def in_bounds(self, x, y):
        return (x >= 0 and y >= 0 and x < Board.WIDTH and y < Board.HEIGHT)

    def to_string(self):
        string =  "    A  B  C  D  E  F  G  H\n"
        string += "    -----------------------\n"
        for y in range(Board.HEIGHT):
            string += str(8 - y) + " | "
            for x in range(Board.WIDTH):
                piece = self.chesspieces[x][y]
                if (piece != 0):
                    string += piece.to_string()
                else:
                    string += ".. "
            string += "\n"
        return string + "\n"