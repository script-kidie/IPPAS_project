from puzzle import *
from gui import *

puzzle = puzzle(np.chararray([]))
gui = Gui()

word_count = 2
min_word_length = 3
max_word_length = 3
min_crossings = 1
max_crossings = 2

puzzle_grid, h_coordinates, v_coordinates, h_words, v_words, grid_size = puzzle.generate_puzzle(word_count,
                                                                                                min_word_length,
                                                                                                max_word_length,
                                                                                                min_crossings,
                                                                                                max_crossings)

gui.make_puzzle_page(grid_size, puzzle_grid, h_coordinates, v_coordinates, h_words, v_words)
