# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 18:02:29 2021

@author: matisse
"""

import board, pieces, numpy

class Heuristique:

    # Les tableaux indiquent les points marqués pour la position des pièces d'échecs sur l'échiquier.



    CAVALIER_TABLE = numpy.array([
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,   0,   5,   5,   0, -20, -40],
        [-30,   5,  10,  15,  15,  10,   5, -30],
        [-30,   0,  15,  20,  20,  15,   0, -30],
        [-30,   5,  15,  20,  20,  15,   0, -30],
        [-30,   0,  10,  15,  15,  10,   0, -30],
        [-40, -20,   0,   0,   0,   0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ])

    FOU_TABLE = numpy.array([
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,   5,   0,   0,   0,   0,   5, -10],
        [-10,  10,  10,  10,  10,  10,  10, -10],
        [-10,   0,  10,  10,  10,  10,   0, -10],
        [-10,   5,   5,  10,  10,   5,   5, -10],
        [-10,   0,   5,  10,  10,   5,   0, -10],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ])

    

  

    @staticmethod
    def evaluate(board):
        material = Heuristique.get_material_score(board)

       
        cavalier = Heuristique.get_piece_position_score(board, pieces.Cavalier.PIECE_TYPE, Heuristique.CAVALIER_TABLE)
        fou = Heuristique.get_piece_position_score(board, pieces.Fou.PIECE_TYPE, Heuristique.FOU_TABLE)
       
        

        return material + cavalier + fou

    # Retourne le score pour la position du type de pièce donné.
    @staticmethod
    def get_piece_position_score(board, piece_type, table):
        blanc = 0
        noir = 0
        for x in range(8):
            for y in range(8):
                piece = board.chesspieces[x][y]
                if (piece != 0):
                    if (piece.piece_type == piece_type):
                        if (piece.color == pieces.Piece.BLANC):
                            blanc += table[x][y]
                        else:
                            noir += table[7 - x][y]

        return blanc - noir
    
    @staticmethod
    def get_material_score(board):
        blanc = 0
        noir = 0
        for x in range(8):
            for y in range(8):
                piece = board.chesspieces[x][y]
                if (piece != 0):
                    if (piece.color == pieces.Piece.BLANC):
                        blanc += piece.value
                    else:
                        noir += piece.value

        return blanc - noir


class IA:

    INFINITE = 20000

    @staticmethod
    def get_ia_move(chessboard, invalid_moves):
        best_move = 0
        best_score = IA.INFINITE
        for move in chessboard.get_possible_moves(pieces.Piece.NOIR):
            if (IA.is_invalid_move(move, invalid_moves)):
                continue

            copy = board.Board.clone(chessboard)
            copy.perform_move(move)

            score = IA.alphabeta(copy, 2, -IA.INFINITE, IA.INFINITE, True)
            if (score < best_score):
                best_score = score
                best_move = move

        # Checkmate.
        if (best_move == 0):
            return 0

        copy = board.Board.clone(chessboard)
        copy.perform_move(best_move)
        if (copy.is_check(pieces.Piece.NOIR)):
            invalid_moves.append(best_move)
            return IA.get_ai_move(chessboard, invalid_moves)

        return best_move

    @staticmethod
    def is_invalid_move(move, invalid_moves):
        for invalid_move in invalid_moves:
            if (invalid_move.equals(move)):
                return True
        return False

    @staticmethod
    def minimax(board, profondeur, maximizing):
        if (profondeur == 0):
            return Heuristique.evaluate(board)

        if (maximizing):
            best_score = -IA.INFINITE
            for move in board.get_possible_moves(pieces.Piece.BLANC):
                copy = board.Board.clone(board)
                copy.perform_move(move)

                score = IA.minimax(copy, profondeur-1, False)
                best_score = max(best_score, score)

            return best_score
        else:
            best_score = IA.INFINITE
            for move in board.get_possible_moves(pieces.Piece.NOIR):
                copy = board.Board.clone(board)
                copy.perform_move(move)

                score = IA.minimax(copy, profondeur-1, True)
                best_score = min(best_score, score)

            return best_score

    @staticmethod
    def alphabeta(chessboard, profondeur, a, b, maximizing):
        if (profondeur == 0):
            return Heuristique.evaluate(chessboard)

        if (maximizing):
            best_score = -IA.INFINITE
            for move in chessboard.get_possible_moves(pieces.Piece.BLANC):
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)

                best_score = max(best_score, IA.alphabeta(copy, profondeur-1, a, b, False))
                a = max(a, best_score)
                if (b <= a):
                    break
            return best_score
        else:
            best_score = IA.INFINITE
            for move in chessboard.get_possible_moves(pieces.Piece.NOIR):
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)

                best_score = min(best_score, IA.alphabeta(copy, profondeur-1, a, b, True))
                b = min(b, best_score)
                if (b <= a):
                    break
            return best_score


class Move:

    def __init__(self, xfrom, yfrom, xto, yto, castling_move):
        self.xfrom = xfrom
        self.yfrom = yfrom
        self.xto = xto
        self.yto = yto
        self.castling_move = castling_move

    # Renvoie vrai si (xfrom,yfrom) et (xo,yto) sont identiques.
    def equals(self, other_move):
        return self.xfrom == other_move.xfrom and self.yfrom == other_move.yfrom and self.xto == other_move.xto and self.yto == other_move.yto

    def to_string(self):
        return "(" + str(self.xfrom) + ", " + str(self.yfrom) + ") -> (" + str(self.xto) + ", " + str(self.yto) + ")"