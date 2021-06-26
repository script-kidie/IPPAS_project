import PySimpleGUI as sg
import random


class Gui:

    def get_first_grid_points(self, h_coordinates, v_coordinates):
        """
        gathers the first points of each coordinate vertical and horizontal coordinate set

        :param h_coordinates: list (list with all the coordinates used for horizontal words)
        :param v_coordinates: list (list with all the coordinates used for vertical words)
        :return: list, list (contain the first individual coordinate points of the horizontal or vertical words)
        """
        h_first_grid_points = []  # create list where all the first horizontal points will be stored
        v_first_grid_points = []  # create list where all the first vertical points will be stored

        # store all the first coordinate points
        for lst in h_coordinates:
            h_first_grid_points.append(lst[0])

        for lst in v_coordinates:
            v_first_grid_points.append(lst[0])

        return h_first_grid_points, v_first_grid_points

    def get_puzzle_words(self, first_coordinate_point, coordinates, words, word_number):
        """
        generates part of the words that are presented on the side of the puzzle

        :param first_coordinate_point: list (list of the first individual points of coordinates)
        :param coordinates: list (list of coordinates used by words)
        :param words: list (list of words used by coordinates)
        :param word_number: integer (number of the word corresponding to the number on the puzzle)
        :return: string (part of the words that will be presented at the side of the puzzle)
        """

        string = ""  # make an empty string that the code will use to build a bigger string
        if first_coordinate_point in coordinates:  # loop trough all the first coordinate points
            # fetch the corresponding word of the current point
            word = words[coordinates.index(first_coordinate_point)]

            # clean up the string so no "\n" chars are present and the word is randomly shuffled
            word = "".join("".join(random.sample(word, len(word))).split("\n"))

            # concatenate the string with the number and the shuffled word
            string = (string + f"  {word_number}.{word}\n")
        return string

    def make_puzzle_words(self, h_words, v_words, first_grid_points, grid_size):
        """
        builds the string that will be presented at the side of the puzzle

        :param h_words: list (list that contains all te used horizontal words)
        :param v_words: list (list that contains all te used vertical words)
        :param first_grid_points: list (list that contains all te first individual coordinate points)
        :param grid_size: integer (dimension sizes of the grid)
        :return: string (string presented on the side of the puzzle)
        """
        str1 = "Gehuselde Horizontale woorden:\n"
        str2 = "Gehuselde Verticaale woorden:\n"

        h_coordinates, v_coordinates = first_grid_points
        word_number = 1

        # build the string we want to present
        for row in range(grid_size):
            for cel in range(grid_size):

                point_coordinate = [row, cel]  # define the coordinate we want to check

                str1 = str1 + self.get_puzzle_words(point_coordinate, h_coordinates, h_words, word_number)

                str2 = str2 + self.get_puzzle_words(point_coordinate, v_coordinates, v_words, word_number)

                if point_coordinate in v_coordinates or point_coordinate in h_coordinates:
                    word_number += 1

        return str(str1 + str2)

    def make_puzzle_page(self, grid_size, puzzle, h_coordinates, v_coordinates, h_words, v_words):

        box_area = 25  # define the area of the box

        # define the string we want to put on the side of the puzzle
        puzzle_words = self.make_puzzle_words(h_words, v_words,
                                              self.get_first_grid_points(h_coordinates, v_coordinates), grid_size)

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

        # create the layout of the GUI with dynamically sized puzzle grid
        layout = [
            [sg.Text("Een verse kruiswoordpuzzel voor jou :]")],
            [sg.Graph((round(47*grid_size), round(47*grid_size)), (0, round(26*grid_size)), (round(26*grid_size), 0),
                      key="puzzle", change_submits=True, drag_submits=False), sg.Text(puzzle_words)],
            [sg.Button("Exit"), sg.Text("Vul hier uw letter in :"), sg.Input(key="-IN-", size=(3, 3)),
             sg.Text("(max 1 letter)")]
        ]

        # define what teh puzzle window will use
        window = sg.Window("Bram's kruiswoord machine", layout, finalize=True)
        # window.Maximize()  # make the window full screen

        p = window["puzzle"]

        word_number = 1

        non_black_positions = []  # create a list that stores coordinates that represent a square that isn't black

        # loop trough all the positions in the grid
        for row in range(grid_size):
            for cel in range(grid_size):
                if puzzle[row][cel] != "*":  # if the grid positions doesnt contain a letter draw a black square
                    p.draw_rectangle((cel * box_area + 3, row * box_area + 5),
                                     (cel * box_area + box_area + 3, row * box_area + box_area + 5),
                                     line_color="black", fill_color="white")

                    non_black_positions.append([cel, row])  # store the coordinates

                # draw a small number at the top left of the square if it is the begging of a word
                point_coordinates = [row, cel]  # define the coordinates
                if point_coordinates in self.get_first_grid_points(h_coordinates, v_coordinates)[0]\
                        or point_coordinates in self.get_first_grid_points(h_coordinates, v_coordinates)[1]:
                    # draw the number on the coordinates
                    p.draw_text(f"{word_number}", (cel * box_area + 7, row * box_area + 9))

                    word_number += 1

        # reads the values of the grid and the text input
        while True:  # Event Loop
            event, values = window.read()

            # close the window if the exit button or the X on the top right is pressed
            if event in (sg.WIN_CLOSED, "Exit"):
                break

            mouse = values["puzzle"]  # collect raw data on the mousses position on the puzzle grid

            if event == "puzzle":  # if a event takes place on the grid check further
                if mouse == (None, None):  # if the mouse position is not on the grid continue
                    continue

                # calculate the position of the mouse
                box_x = mouse[0] // box_area
                box_y = mouse[1] // box_area

                # if the coordinates of the mouse are on a black square ignore all inputs
                if [box_x, box_y] not in non_black_positions:
                    continue

                # give a pop up if the input is more than one character and ignore inputs
                if len(values["-IN-"]) > 1:
                    sg.popup(title="Teveel letters", auto_close=True, auto_close_duration=5,
                             custom_text="U mag maar 1 letter invoeren")
                    continue

                # define the position of the letter
                letter_location = (box_x * box_area + box_area-9, box_y * box_area + box_area-9)

                # remove the already placed letter in the square
                p.draw_rectangle((box_x * box_area + 4, box_y * box_area + 12),
                                 (box_x * box_area + box_area + 2,
                                  box_y * box_area + box_area + 4),
                                 line_color="white", fill_color="white")

                # draw the input letter on the puzzle grid
                p.draw_text(f"{values['-IN-']}",
                            letter_location, font="Courier 20")
            # close the window for good practice if the code is finished
        window.close()
