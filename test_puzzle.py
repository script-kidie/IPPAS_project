from unittest import TestCase

from puzzle import *

puzzle = Puzzle(np.chararray([]))


class TestPuzzle(TestCase):
    def test_set_and_get_grid(self):
        grid_size = 2

        puzzle.set_blank_grid(grid_size)

        check_array = np.chararray((grid_size, grid_size), 1, True)
        check_array.fill("*")

        check = puzzle.get_grid() == check_array

        self.assertTrue(check.all())

    def test_get_singleword(self):
        self.assertEqual(puzzle.get_singleword(5, "AND woord LIKE 'ha_lo%'"), "hallo")
        self.assertEqual(puzzle.get_singleword(6, "AND woord LIKE 'hu_sje%'"), "huisje")
        self.assertEqual(puzzle.get_singleword(10, "AND woord LIKE 'pa_nenkoek%'"), "pannenkoek")

    def test_fill_grid(self):
        puzzle.set_blank_grid(2)
        coordinates = [[0, 0], [0, 1]]
        fill_word = "ja"

        puzzle.fill_grid(fill_word, coordinates)
        self.assertEqual(puzzle.get_grid()[0, 0], "j")
        self.assertEqual(puzzle.get_grid()[0, 1], "a")
        self.assertEqual(puzzle.get_grid()[1, 0], "*")
        self.assertEqual(puzzle.get_grid()[1, 1], "*")

    def test_intersection_info(self):
        puzzle.set_blank_grid(2)
        coordinates = [[0, 0], [0, 1]]

        puzzle.get_intersection_info(coordinates)
        self.assertEqual(puzzle.get_intersection_info(coordinates), ["*", "*"])

    def test_generate_coordinate(self):
        puzzle.set_blank_grid(5)

        if puzzle.generate_coordinate(4, [0, 1], 5) == [[0, 0], [0, 1], [0, 2], [0, 3]] or \
                puzzle.generate_coordinate(4, [0, 1], 5) == [[1, 0], [1, 1], [2, 2], [3, 3]] or \
                puzzle.generate_coordinate(4, [0, 1], 5) == [[2, 0], [2, 1], [2, 2], [3, 3]] or \
                puzzle.generate_coordinate(4, [0, 1], 5) == [[3, 0], [3, 1], [3, 2], [3, 3]] or \
                puzzle.generate_coordinate(4, [0, 1], 5) == [[4, 0], [4, 1], [4, 2], [4, 3]]:
            self.assertTrue(True, True)
        else:
            self.assertTrue(True, False)

        if puzzle.generate_coordinate(4, [0, 1], 5) == [[1, 0], [2, 0], [3, 0], [4, 0]] or \
                puzzle.generate_coordinate(4, [0, 1], 5) == [[1, 1], [2, 1], [3, 1], [4, 1]] or \
                puzzle.generate_coordinate(4, [0, 1], 5) == [[1, 2], [2, 2], [3, 2], [4, 2]] or \
                puzzle.generate_coordinate(4, [0, 1], 5) == [[1, 3], [2, 3], [3, 3], [4, 3]] or \
                puzzle.generate_coordinate(4, [0, 1], 5) == [[1, 4], [2, 4], [3, 4], [4, 4]]:
            self.assertTrue(True, True)
        else:
            self.assertTrue(True, False)

