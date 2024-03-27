import unittest

from src.algorithms.simplex_method.function import main


class TestCase(unittest.TestCase):

    def test_tableau_empty(self):
        tableau = [[0., -1., -1., 0., 0.],
                   [24., 6., 4., 1., 0.],
                   [6., 3., -2., 0., 1.]]
        basic_var = [1, 2]
        self.assertEqual({'optimal_solution': [0.0, 6.0, 0.0, 18.0], 'optimal_value': -6.0},
                         main(tableau, basic_var))
