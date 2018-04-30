import unittest
from morelli import Morelli
#from Player import *
#from Cell import *


class TestMorelli(unittest.TestCase):

    def setUp(self):
        self.game = Morelli(dim=11, testing=True)

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


if __name__ == '__main__':
    unittest.main()
