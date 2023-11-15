import sys

import pygame

from const import *
from game import Game
from move import Move
from square import Square

'''
with open('CaroKann.txt') as f:
	CaroKann = f.readlines()

currentpage = 0
CaroKannPage = 10
with open('RuyLopez.txt') as f:
	RuyLopez = f.readlines()

RuyLopezPage = 10
with open('SicilianDefense.txt') as f:
	SicilianDefense = f.readlines()
SicilianDefensePage = 10


def menu():
	global story, CaroKann, diffPage, CaroKannPage, RuyLopez, RuyLopezPage, SicilianDefense, SicilianDefensePage
	print('Welcome to Trevors Chess')
	print('Choose a Opening/Defense, or start a new game:')
	print('1. Caro-Kann Defense')
	print('2. Ruy Lopez Opening')
	print('3. Sicilian Defense')
	print('4. Start a new game')
	choice = input('\nEnter a choice: ')
	
	if choice == '1':
		story = CaroKann
		diffPage = CaroKannPage
	elif choice == '2':
		story = RuyLopez
		diffPage = RuyLopezPage
	elif choice == '3':
		story = SicilianDefense
		diffPage = SicilianDefensePage
	elif choice == '4':
		main
		
		
		
		
def readPage():
	global story, diffPage, currentpage
	for i in range(currentpage, currentpage + diffPage):
		print(story[i].strip('\n'))
	print('\nN: Next Page\nP: Previous Page\nM: Menu')
	choice = input('>')
	if choice == 'N':
		currentpage += diffPage
	elif choice == 'P':
		currentpage -= diffPage
	elif choice == 'M':
		menu()


menu()
while True:
	readPage()
'''


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):

        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        while True:
            # show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # if clicked square has a piece ?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if event.pos[0] > 0 and event.pos[0] < WIDTH:
                        motion_row = event.pos[1] // SQSIZE
                        motion_col = event.pos[0] // SQSIZE

                        game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                # click release
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valid move ?
                        if board.valid_move(dragger.piece, move):
                            # normal capture
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)

                            # sounds
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()

                    dragger.undrag_piece()

                # key press
                elif event.type == pygame.KEYDOWN:

                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()

                    if SQSIZE == SQSIZE:
                        round(SQSIZE)

                    # changing themes
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.mainloop()
