from puzzle import *
from gui import *

puzzle = puzzle(np.chararray([]))
gui = Gui()

word_count = 12

puzzle_grid, h_coordinates, v_coordinates, h_words, v_words, grid_size = puzzle.generate_puzzle(word_count, 3, 5, 1, 2)


def get_first_grid_points(h_coordinates, v_coordinates):
    first_grid_points = []

    # print(f"h = {h_coordinates}")
    # print(f"v = {v_coordinates}")

    for lst in h_coordinates:
        first_grid_points.append(lst[0])

    for lst in v_coordinates:
        first_grid_points.append(lst[0])
    # print(f"f = {first_grid_points}")
    return first_grid_points


gui.make_puzzle_page(grid_size, puzzle_grid, get_first_grid_points(h_coordinates, v_coordinates),
                     h_words, v_words, h_coordinates, v_coordinates)
