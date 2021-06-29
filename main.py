import sys
from puzzle import *
from gui import *

puzzle = Puzzle(np.chararray([]), [])
gui = Gui()

# create a custom theme for easier overview of where what color is used
sg.LOOK_AND_FEEL_TABLE["MyCreatedTheme"] = {"BACKGROUND": "#315259",
                                            "TEXT": "black",
                                            "INPUT": "white",
                                            "TEXT_INPUT": "black",
                                            "SCROLL": "#99CC99",
                                            "BUTTON": ("black", "#A0B52F"),
                                            "PROGRESS": ("#D1826B", "#CC8019"),
                                            "BORDER": 1, "SLIDER_DEPTH": 0,
                                            "PROGRESS_DEPTH": 0, }

sg.theme("MyCreatedTheme")  # implement the customized theme

layout = [
    [sg.Text("Selecteer een puzzel grote (puzzles groter dan 15 kunnen lang duren om te genereren)")],
    [sg.Slider(range=(2, 20), size=(50, 10), orientation="h",
               key="slider")],
    [sg.Button("genereer puzzel", key="-GEN-")]
]
window = sg.Window("slider test", layout, finalize=True)
window.Finalize()

while True:
    event, values = window.Read()

    if event == sg.WIN_CLOSED:
        break
    elif event == "-GEN-":
        puzzle_size = values["slider"]
        break

# puzzle_size = int(puzzle_size)

# define puzzle parameters
try:
    if 2 <= puzzle_size <= 9:
        word_count = puzzle_size
        min_word_length = 3
        max_word_length = 8
        min_crossings = 1
        max_crossings = 1

    elif 10 <= puzzle_size <= 17:
        word_count = puzzle_size
        min_word_length = 3
        max_word_length = 10
        min_crossings = 1
        max_crossings = 2

    elif puzzle_size >= 18:
        word_count = puzzle_size
        min_word_length = 3
        max_word_length = 12
        min_crossings = 1
        max_crossings = 10
except NameError:
    sys.exit()


# generate the puzzle
puzzle_grid, h_coordinates, v_coordinates, h_words, v_words, grid_size = puzzle.generate_puzzle(word_count,
                                                                                                min_word_length,
                                                                                                max_word_length,
                                                                                                min_crossings,
                                                                                                max_crossings)
# generate the GUI
gui.make_puzzle_page(grid_size, puzzle_grid, h_coordinates, v_coordinates, h_words, v_words)
