import unittest
from morelli import Morelli
from copy import deepcopy
from MonteCarlo import MonteCarlo
from pprint import pprint
from Rules import board_value
import random
import time

class TestMorelli(unittest.TestCase):

    def setUp(self):
        self.game = Morelli(dim=11, testing=True, gui=False)

        self.game.board.reset_test_env()

    def test_creation(self):
        self.assertEqual(len(self.game.board._cells), 11, "Wrong cell Size")

    def test_move_check(self):

        from_cell = self.game.board._cells[0][3]

        to_cell_topf = self.game.board._cells[1][3]
        to_cell_topf2 = self.game.board._cells[2][3]
        to_cell_topf3 = self.game.board._cells[3][3]

        to_cell_topg = self.game.board._cells[1][5]
        to_cell_topg2 = self.game.board._cells[3][5]

        self.game.board.print()


        #self.assertFalse(self.game.board.move(from_cell, to_cell_topf), "Did move when should not have")
        #self.assertFalse(self.game.board.move(from_cell, to_cell_topf2), "Did move when should not have")
        
        self.assertTrue(self.game.board.move(from_cell, to_cell_topg), "Supossed to move, did not")

        self.assertFalse(self.game.board.move(from_cell, to_cell_topg2), "Should have said it was empty")

        self.game.board.reset_test_env()

        self.assertTrue(self.game.board.move(from_cell, to_cell_topg2), "Supossed to move, did not 2")

    def test_move_mod(self):

        self.game.board.reset_test_env()

        to_cell_eat = self.game.board._cells[1][4]

        from_cell = self.game.board._cells[0][3]

        self.assertEqual(self.game.board._cells[1][3].get_holding().color_str(), "white", "Start piece bad color")

        self.game.board.move(from_cell, to_cell_eat)

        self.assertEqual(self.game.board._cells[1][3].get_holding().color_str(), "black", "Did not capture white piece")

        self.game.board.move(self.game.board._cells[1][3], self.game.board._cells[2][4])
        
        self.assertEqual(self.game.board._cells[1][2].get_holding().color_str(), "black", "Pieces chaging color1")
        self.assertEqual(self.game.board._cells[1][4].get_holding().color_str(), "black", "Pieces chaging color2")


    def test_next_state(self):

        self.game.board.reset_test_env()

        #self.game.board._cells[1][2].set_empty()

        initial_board = deepcopy(self.game.board)

        this_board = self.game.board

        #w_piece = self._cells[1][3].set_holding(Piece(self._players[1]))

        avaiable_moves_p1 = self.game.board.avaiable_moves(this_board._players[0], flat=True)

        moves_states = []
        for legal_play in avaiable_moves_p1:
            #next_play_board = MonteCarlo.next_state(this_board, legal_play)
            #self.assertFalse(next_play_board == initial_board, "Board of next play are the same")
           #pprint(legal_play[1].pos)
            if(legal_play[1].pos == [1,4]):
                #print("Player 0 number of cells : %d" % len(this_board.get_player_cells(next_play_board._players[0])))
                #print("Player 1 number of cells : %d" % len(this_board.get_player_cells(next_play_board._players[1])))
                
                print("BEFORE BOARD")
                this_board.print()
                print("After Board")

                self.assertFalse(MonteCarlo.next_state(this_board, legal_play) == this_board, "Board of next play are the same")

                print("Found equal 1,4")
                print("Init board value", end=". ")
                pprint(board_value(initial_board))
                print(", 1,4 move board val", end=". ")
                #pprint(board_value(next_play_board))
            #moves_states.append( (legal_play, next_play_board) )
    

class TestMorelliCreation(unittest.TestCase):

    def setUp(self):
        self.game = Morelli(dim=11, testing=True, gui=False)

    def test_proper_creation(self):
        numb_pieces = [0, 0]

        for cell_line in self.game.board._cells:
            for cell in cell_line:
                if(not cell.is_empty()):
                    if(cell.get_holding().color_str() == 'white'):
                        numb_pieces[0] += 1
                    elif(cell.get_holding().color_str() == 'black'):
                        numb_pieces[1] += 1

        self.assertEqual(numb_pieces[0] + numb_pieces[1], self.game.dim*4 - 4, "Incorrect number of pieces placeds" )
        self.assertEqual(numb_pieces[0], numb_pieces[1], "Different number of pieces for players")

        for y in range(1, len(self.game.board._cells[0]) - 1):
            cell = self.game.board._cells[0][y]
            op_cell = self.game.board._cells[self.game.dim - 1][y]
            if(not cell.is_empty()):
                self.assertNotEqual(cell.get_holding().color_str(), op_cell.get_holding().color_str(), "Opossing cell not oposite color." )

        for x in range(1, len(self.game.board._cells[0]) -1):
            cell = self.game.board._cells[x][0]
            op_cell = self.game.board._cells[x][self.game.dim - 1]
            if(not cell.is_empty()):
                self.assertNotEqual(cell.get_holding().color_str(), op_cell.get_holding().color_str(), "Opossing cell not oposite color." )

class TestMorelliMoves(unittest.TestCase):

    def setUp(self):
        self.game = Morelli(dim=11, testing=True, gui=True)

    def test_many_moves(self):
        moves_made = 0

        aval_moves = self.game.board.avaiable_moves(self.game.board._players[0])

        while len(aval_moves) > 0:
            from_cell, to_cell_l = random.choice(list(aval_moves.items()))
            to_cell = random.choice(to_cell_l)
            self.assertNotEqual(self.game.board.move(from_cell, to_cell), False, "Did not move on aval move")

            moves_made += 1
            aval_moves = self.game.board.avaiable_moves(self.game.board._players[random.randint(0,1)])
            print('before draw')
            self.game.game_draw()
            print('after draw')
            time.sleep(0.5)

        self.assertTrue(moves_made > 15, "Not enough moves made")
        print('Made %d moves' % (moves_made))

if __name__ == '__main__':
    unittest.main()
