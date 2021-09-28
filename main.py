# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 18:01:13 2021

@author: matisse
"""

import board, pieces, ia

# Renvoie un objet de déplacement basé sur l'entrée de l'utilisateur. Il ne vérifie pas si le déplacement est valide.
def get_utilisateur_move():
    tour_str = input("Votre tour: ")
    tour_str = tour_str.replace(" ", "")

    try:
        xfrom = lettre_to_xpos(tour_str[0:1])
        yfrom = 8 - int(tour_str[1:2]) # Le tableau est dessiné "à l'envers", donc inversez la coordonnée y.
        xto = lettre_to_xpos(tour_str[2:3])
        yto = 8 - int(tour_str[3:4]) # Le tableau est dessiné "à l'envers", donc inversez la coordonnée y.
        return ia.Move(xfrom, yfrom, xto, yto, False)
    except ValueError:
        print("Format Invalide")
        return get_utilisateur_move()

# Renvoie un mouvement valide basé sur la saisie de l'utilisateur.
def get_valid_utilisateur_move(board):
    while True:
        move = get_utilisateur_move()
        valid = False
        possible_moves = board.get_possible_moves(pieces.Piece.BLANC)
        # aucun mouvement possible
        if (not possible_moves):
            return 0

        for possible_move in possible_moves:
            if (move.equals(possible_move)):
                move.castling_move = possible_move.castling_move
                valid = True
                break

        if (valid):
            break
        else:
            print("Mouvement Invalide")
    return move

# Convertit une lettre (A-H) en position x sur l'échiquier.
def lettre_to_xpos(lettre):
    lettre = lettre.upper()
    if lettre == 'A':
        return 0
    if lettre == 'B':
        return 1
    if lettre == 'C':
        return 2
    if lettre == 'D':
        return 3
    if lettre == 'E':
        return 4
    if lettre == 'F':
        return 5
    if lettre == 'G':
        return 6
    if lettre == 'H':
        return 7

    raise ValueError("Lettre Invalide.")
#
# Point d'entrée.
#
board = board.Board.new()
print(board.to_string()) 

while True:
    move = get_valid_utilisateur_move(board)
    if (move == 0):
        if (board.is_check(pieces.Piece.BLANC)):
            print("Checkmate. Les noirs ont gagnés.")
            break
        else:
            print("Pat.")
            break

    board.perform_move(move)

    print("Tour utilisateur: " + move.to_string())
    print(board.to_string())

    IA_move = ia.IA.get_ia_move(board, [])
    if (IA_move == 0):
        if (board.is_check(pieces.Piece.NOIR)):
            print("Checkmate.Les blancs ont gagnés.")
            break
        else:
            print("Pat.")
            break

    board.perform_move(IA_move)
    print("Tour IA: " + IA_move.to_string())
    print(board.to_string())