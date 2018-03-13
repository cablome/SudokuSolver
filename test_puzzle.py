from unittest import TestCase

from SudokuSolver import Puzzle

# Initial grid values as row/column/value tuples
# This puzzle is solvable with only hidden/naked singles
singles_only = [(0, 1, 8), (0, 4, 9), (0, 6, 3),
                (1, 0, 3), (1, 3, 5), (1, 6, 1), (1, 8, 8),
                (2, 2, 6), (2, 3, 3), (2, 4, 4),
                (3, 0, 5), (3, 7, 7), (3, 8, 4),
                (5, 0, 7), (5, 1, 1), (5, 8, 9),
                (6, 4, 5), (6, 5, 6), (6, 6, 8),
                (7, 0, 6), (7, 2, 1), (7, 5, 2), (7, 8, 7),
                (8, 2, 5), (8, 4, 7), (8, 7, 3)]

singles_only_solution = [2, 8, 7, 6, 9, 1, 3, 4, 5,
                         3, 4, 9, 5, 2, 7, 1, 6, 8,
                         1, 5, 6, 3, 4, 8, 7, 9, 2,
                         5, 3, 8, 2, 1, 9, 6, 7, 4,
                         9, 6, 4, 7, 8, 5, 2, 1, 3,
                         7, 1, 2, 4, 6, 3, 5, 8, 9,
                         4, 7, 3, 9, 5, 6, 8, 2, 1,
                         6, 9, 1, 8, 3, 2, 4, 5, 7,
                         8, 2, 5, 1, 7, 4, 9, 3, 6]

singles_only_info = [['X', 8, 'X', 'X', 9, 'X', 3, 'X', 'X'],
                     [3, 'X', 'X', 5, 'X', 'X', 1, 'X', 8],
                     ['X', 'X', 6, 3, 4, 'X', 'X', 'X', 'X'],
                     [5, 'X', 'X', 'X', 'X', 'X', 'X', 7, 4],
                     ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                     [7, 1, 'X', 'X', 'X', 'X', 'X', 'X', 9],
                     ['X', 'X', 'X', 'X', 5, 6, 8, 'X', 'X'],
                     [6, 'X', 1, 'X', 'X', 2, 'X', 'X', 7],
                     ['X', 'X', 5, 'X', 7, 'X', 'X', 3, 'X']]

singles_only_1 = [(0, 2, 9), (0, 4, 8), (0, 5, 2),
                  (1, 6, 7), (1, 8, 3),
                  (2, 4, 7), (2, 5, 4), (2, 7, 9), (2, 8, 1),
                  (3, 5, 3),
                  (4, 0, 4), (4, 1, 3), (4, 3, 1), (4, 4, 5), (4, 5, 9), (4, 7, 7), (4, 8, 2),
                  (5, 3, 4),
                  (6, 0, 2), (6, 1, 5), (6, 3, 6), (6, 4, 3),
                  (7, 0, 8), (7, 2, 4),
                  (8, 3, 2), (8, 4, 4), (8, 6, 6)]

singles_only_1_solution = None

twins_and_triples = [(0, 4, 3), (0, 5, 5), (0, 6, 2),
                     (1, 1, 5), (1, 4, 4), (1, 7, 1),
                     (2, 1, 3), (2, 4, 1), (2, 5, 8),
                     (3, 0, 8), (3, 8, 7),
                     (4, 0, 1), (4, 1, 4), (4, 4, 5), (4, 7, 9), (4, 8, 3),
                     (5, 0, 3), (5, 8, 4),
                     (6, 3, 2), (6, 4, 9), (6, 7, 4),
                     (7, 1, 2), (7, 4, 7), (7, 7, 6),
                     (8, 2, 9), (8, 3, 5), (8, 4, 8)]

naked_pairs = [(0, 0, 4), (0, 6, 9), (0, 7, 3), (0, 8, 8),
               (1, 1, 3), (1, 2, 2), (1, 4, 9), (1, 5, 4), (1, 6, 1),
               (2, 1, 9), (2, 2, 5), (2, 3, 3), (2, 6, 2), (2, 7, 4),
               (3, 0, 3), (3, 1, 7), (3, 3, 6), (3, 5, 9), (3, 8, 4),
               (4, 0, 5), (4, 1, 2), (4, 2, 9), (4, 5, 1), (4, 6, 6), (4, 7, 7), (4, 8, 3),
               (5, 0, 6), (5, 2, 4), (5, 3, 7), (5, 5, 3), (5, 7, 9),
               (6, 0, 9), (6, 1, 5), (6, 2, 7), (6, 5, 8), (6, 6, 3),
               (7, 2, 3), (7, 3, 9), (7, 6, 4),
               (8, 0, 2), (8, 1, 4), (8, 4, 3), (8, 6, 7), (8, 8, 9)]

naked_pairs_solution = [4, 6, 1, 5, 7, 2, 9, 3, 8,
                        7, 3, 2, 8, 9, 4, 1, 5, 6,
                        8, 9, 5, 3, 1, 6, 2, 4, 7,
                        3, 7, 8, 6, 2, 9, 5, 1, 4,
                        5, 2, 9, 4, 8, 1, 6, 7, 3,
                        6, 1, 4, 7, 5, 3, 8, 9, 2,
                        9, 5, 7, 2, 4, 8, 3, 6, 1,
                        1, 8, 3, 9, 6, 7, 4, 2, 5,
                        2, 4, 6, 1, 3, 5, 7, 8, 9]

hidden_pairs = [(1,0,9),(1,2,4),(1,3,6),(1,5,7),
                (2,1,7),(2,2,6), (2,3,8),(2,5,4),(2,6,1),
                (3,0,3),(3,2,9),(3,3,7),(3,5,1),(3,7,8),
                (4,2,8),(4,6,3),
                (5,1,5),(5,3,3),(5,5,8),(5,6,7),(5,8,2),
                (6,2,7),(6,3,5),(6,5,2),(6,6,6),(6,7,1),
                (7,3,4),(7,5,3),(7,6,2),(7,8,8)]

hidden_pairs_solution = [5,8,3,2,1,9,4,6,7,
                         9,1,4,6,3,7,8,2,5,
                         2,7,6,8,5,4,1,3,9,
                         3,4,9,7,2,1,5,8,6,
                         7,2,8,9,6,5,3,4,1,
                         6,5,1,3,4,8,7,9,2,
                         4,9,7,5,8,2,6,1,3,
                         1,6,5,4,9,3,2,7,8,
                         8,3,2,1,7,6,9,5,4]

foo = [(0, 3, 7), (0, 8, 1),
       (1, 1, 6), (1, 4, 3), (1, 8, 9),
       (2, 0, 1), (2, 4, 4), (2, 5, 6),
       (3, 5, 3), (3, 6, 9), (3, 8, 7),
       (4, 0, 4), (4, 1, 3), (4, 4, 1), (4, 7, 5), (4, 8, 2),
       (5, 0, 9), (5, 2, 5), (5, 3, 6),
       (6, 3, 3), (6, 4, 6), (6, 8, 5),
       (7, 0, 7), (7, 4, 2), (7, 7, 8),
       (8, 0, 5), (8, 5, 9)]

foo_solution = [3, 5, 8, 7, 9, 2, 4, 6, 1,
                2, 6, 4, 8, 3, 1, 5, 7, 9,
                1, 7, 9, 5, 4, 6, 2, 3, 8,
                6, 8, 1, 2, 5, 3, 9, 4, 7,
                4, 3, 7, 9, 1, 8, 6, 5, 2,
                9, 2, 5, 6, 7, 4, 8, 1, 3,
                8, 4, 2, 3, 6, 7, 1, 9, 5,
                7, 9, 6, 1, 2, 5, 3, 8, 4,
                5, 1, 3, 4, 8, 9, 7, 2, 6]

twins_and_triples_solution = [4, 7, 1, 6, 3, 5, 2, 8, 9,
                              9, 5, 8, 7, 4, 2, 3, 1, 6,
                              2, 3, 6, 9, 1, 8, 4, 7, 5,
                              8, 9, 5, 4, 6, 3, 1, 2, 7,
                              1, 4, 2, 8, 5, 7, 6, 9, 3,
                              3, 6, 7, 1, 2, 9, 8, 5, 4,
                              7, 8, 3, 2, 9, 6, 5, 4, 1,
                              5, 2, 4, 3, 7, 1, 9, 6, 8,
                              6, 1, 9, 5, 8, 4, 7, 3, 2]


class TestPuzzle(TestCase):
    def test_info(self):
        p = Puzzle(singles_only)
        self.assertEqual(p.info(), singles_only_info)

    def test_solve(self):
        test_singles = Puzzle(singles_only)
        self.assertEqual(test_singles.solve(), singles_only_solution)

    def test_solve_1(self):
        test_pairs = Puzzle(singles_only_1)
        self.assertEqual(test_pairs.solve(), singles_only_1_solution)

    def test_solve_foo(self):
        test_foo = Puzzle(foo)
        self.assertEqual(test_foo.solve(), foo_solution)

    def test_solve_naked_pairs(self):
        test_naked_pairs = Puzzle(naked_pairs)
        self.assertEqual(test_naked_pairs.solve(), naked_pairs_solution)

    def test_solve_hidden_pairs(self):
        test_hidden_pairs = Puzzle(hidden_pairs)
        self.assertEqual(test_hidden_pairs.solve(), hidden_pairs_solution)

    def test_solve_2_3(self):
        test_2_3 = Puzzle(twins_and_triples)
        self.assertEqual(test_2_3.solve(), twins_and_triples_solution)
