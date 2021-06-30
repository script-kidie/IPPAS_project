from puzzle import *
from gui import *


def start_application():
    """
    starts the procces of presenting the puzzle in a interface

    :return: integer (1 or 0 determines if the code returns to the start menu or exits the code)
    """
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

    # define the layout for the starting page
    layout1 = [
        [sg.Text("Selecteer een puzzel soort")],
        [sg.Button("kruiwoord puzzel", key="-KRUIS-"), sg.Button("woord zoeker (WIP)", key="-ZOEK-")]
    ]
    window1 = sg.Window("Soort selectie", layout1)
    window1.finalize()

    # check what puzzle kind is selected
    while True:
        event, values = window1.Read()

        if event == sg.WIN_CLOSED:
            sys.exit()

        if event == "-ZOEK-":
            option = 0
            break

        if event == "-KRUIS-":
            option = 1
            break

    # close the starting window
    window1.close()

    # define the layout for the second page
    layout2 = [
        [sg.Text("Selecteer een puzzel grote"), sg.Text("(puzzles groter dan 17 kunnen lang duren om te genereren)",
                                                        text_color="lightgreen")],
        [sg.Slider(range=(2, 20), size=(50, 10), orientation="h",
                   key="slider")],
        [sg.Button("genereer puzzel", key="-GEN-")]
    ]

    window2 = sg.Window("grote selectie", layout2)
    window2.Finalize()

    # fetch what size of puzzle the user has selected
    while True:
        event, values = window2.Read()

        if event == sg.WIN_CLOSED:
            sys.exit()

        elif event == "-GEN-":
            puzzle_size = values["slider"]
            window2.close()
            break

    # define puzzle parameters according to the users inputted size
    try:
        if 2 <= puzzle_size <= 9:
            word_count = puzzle_size
            min_word_length = 3
            max_word_length = 8
            min_crossings = option
            max_crossings = 1

        elif 10 <= puzzle_size <= 17:
            word_count = puzzle_size
            min_word_length = 3
            max_word_length = 10
            min_crossings = option
            max_crossings = 2

        elif puzzle_size >= 18:
            word_count = puzzle_size
            min_word_length = 3
            max_word_length = 12
            min_crossings = option
            max_crossings = 4

    # exit the code if the user quits the select size page
    except NameError:
        sys.exit()

    # generate the puzzle
    puzzle_grid, h_coordinates, v_coordinates, h_words, v_words, grid_size = \
        puzzle.generate_puzzle(word_count, min_word_length, max_word_length, min_crossings, max_crossings, option)

    # generate the GUI
    return gui.make_puzzle_page(grid_size, puzzle_grid, h_coordinates, v_coordinates, h_words, v_words, option)


# define a value that determines if the code continues
application_continue = start_application()

while application_continue == 1:
    application_continue = start_application()
