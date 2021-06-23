from puzzle import *
from gui import *

puzzle = Puzzle(np.chararray([]))
gui = Gui()

# define puzzle parameters
word_count = 12
min_word_length = 3
max_word_length = 10
min_crossings = 1
max_crossings = 1

# generate the puzzle
puzzle_grid, h_coordinates, v_coordinates, h_words, v_words, grid_size = puzzle.generate_puzzle(word_count,
                                                                                                min_word_length,
                                                                                                max_word_length,
                                                                                                min_crossings,
                                                                                                max_crossings)
# generate the GUI
gui.make_puzzle_page(grid_size, puzzle_grid, h_coordinates, v_coordinates, h_words, v_words)
