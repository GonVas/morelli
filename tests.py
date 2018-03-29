import unittest
from morelli import Morelli
#from Player import *
#from Cell import *


class TestMorelli(unittest.TestCase):

    def setUp(self):
        self.game = Morelli(dim=11, testing=True)

        self.game.reset_test_env()

    def test_creation(self):
        self.assertEqual(len(self.game._cells), 11, "Wrong cell Size")

    def test_move(self):

        from_cell = self.game._cells[0][3]

        to_cell_topf = self.game._cells[1][3]
        to_cell_topf2 = self.game._cells[2][3]
        to_cell_topf3 = self.game._cells[3][3]

        to_cell_topg = self.game._cells[1][5]
        to_cell_topg2 = self.game._cells[3][5]

        self.assertFalse(self.game.move(from_cell, to_cell_topf), "Did move when should not have")
        self.assertFalse(self.game.move(from_cell, to_cell_topf2), "Did move when should not have")
        
        self.assertTrue(self.game.move(from_cell, to_cell_topg), "Supossed to move, did not")

        self.assertFalse(self.game.move(from_cell, to_cell_topg2), "Should have said it was empty")

        self.game.reset_test_env()

        self.assertTrue(self.game.move(from_cell, to_cell_topg2), "Supossed to move, did not 2")



if __name__ == '__main__':
    unittest.main()
