import PySimpleGUI as sg
import random


class Gui:

    def get_first_grid_points(self, h_coordinates, v_coordinates):
        h_first_grid_points = []
        v_first_grid_points = []

        for lst in h_coordinates:
            h_first_grid_points.append(lst[0])

        for lst in v_coordinates:
            v_first_grid_points.append(lst[0])

        return h_first_grid_points, v_first_grid_points

    def make_puzzle_words(self, h_words, v_words, first_grid_points, grid_size):
        str1 = "Gehuselde Horizontale woorden:\n"
        str2 = "Gehuselde Verticaale woorden:\n"

        h_coordinates, v_coordinates = first_grid_points
        word_number = 1

        for row in range(grid_size):
            for cel in range(grid_size):

                point_coordinates = [row, cel]

                if point_coordinates in h_coordinates:
                    word = h_words[h_coordinates.index(point_coordinates)]
                    word = random.sample(word, len(word))
                    s_word = ""
                    for c in word:
                        if c == "\n":
                            continue
                        s_word += c
                    str1 = (str1 + f"  {word_number}.{s_word}\n")

                if point_coordinates in v_coordinates:
                    word = v_words[v_coordinates.index(point_coordinates)]
                    word = random.sample(word, len(word))
                    s_word = ""
                    for c in word:
                        if c == "\n":
                            continue
                        s_word += c
                    str2 = (str2 + f"  {word_number}.{s_word}\n")

                if point_coordinates in v_coordinates or point_coordinates in h_coordinates:
                    word_number += 1

        return str(str1 + str2)

    def make_puzzle_page(self, grid_size, puzzle, h_coordinates, v_coordinates, h_words, v_words):

        box_area = 25

        puzzle_words = self.make_puzzle_words(h_words, v_words,
                                              self.get_first_grid_points(h_coordinates, v_coordinates), grid_size)

        sg.LOOK_AND_FEEL_TABLE["MyCreatedTheme"] = {"BACKGROUND": "#315259",
                                                    "TEXT": "black",
                                                    "INPUT": "white",
                                                    "TEXT_INPUT": "black",
                                                    "SCROLL": "#99CC99",
                                                    "BUTTON": ("black", "#A0B52F"),
                                                    "PROGRESS": ("#D1826B", "#CC8019"),
                                                    "BORDER": 1, "SLIDER_DEPTH": 0,
                                                    "PROGRESS_DEPTH": 0, }
        sg.theme("MyCreatedTheme")
        layout = [
            [sg.Text("Een verse kruiswoordpuzzel voor jou :]")],
            [sg.Graph((round(47*grid_size), round(47*grid_size)), (0, round(26*grid_size)), (round(26*grid_size), 0),
                      key="puzzle", change_submits=True, drag_submits=False), sg.Text(puzzle_words)],
            [sg.Button("Exit"), sg.Text("Vul hier uw letter in :"), sg.Input(key="-IN-", size=(3, 3)),
             sg.Text("(max 1 letter)")]
        ]

        window = sg.Window("Bram's kruiswoord machine", layout, finalize=True)

        p = window["puzzle"]

        word_number = 1
        non_black_posistions = []

        for row in range(grid_size):
            for cel in range(grid_size):
                if puzzle[row][cel] != "*":
                    p.draw_rectangle((cel * box_area + 11, row * box_area + 9),
                                     (cel * box_area + box_area + 11, row * box_area + box_area + 9),
                                     line_color="black")

                    non_black_posistions.append([cel, row])
                else:
                    p.draw_rectangle((cel * box_area + 11, row * box_area + 9),
                                     (cel * box_area + box_area + 11, row * box_area + box_area + 9),
                                     line_color="black", fill_color="black")

                point_coordinates = [row, cel]
                if point_coordinates in self.get_first_grid_points(h_coordinates, v_coordinates)[0]\
                        or point_coordinates in self.get_first_grid_points(h_coordinates, v_coordinates)[1]:
                    p.draw_text(f"{word_number}", (cel * box_area + 15, row * box_area + 13))
                    word_number += 1

        while True:  # Event Loop
            event, values = window.read()

            if event in (sg.WIN_CLOSED, "Exit"):
                break

            mouse = values["puzzle"]

            if event == "puzzle":
                if mouse == (None, None):
                    continue

                box_x = mouse[0] // box_area
                box_y = mouse[1] // box_area
                if [box_x, box_y] not in non_black_posistions:
                    continue

                if len(values["-IN-"]) > 1:
                    sg.popup(title="Teveel letters", auto_close=True, auto_close_duration=5,
                             custom_text="U mag maar 1 letter invoeren")
                    continue

                letter_location = (box_x * box_area + box_area, box_y * box_area + 23.5)

                p.draw_rectangle((box_x * box_area+1 + 11, box_y * box_area+7 + 9),
                                 (box_x * box_area-1 + box_area + 11,
                                  box_y * box_area-1 + box_area + 9),
                                 line_color="#315259", fill_color="#315259")

                p.draw_text(f"{values['-IN-']}",
                            letter_location, font="Courier 20")

        window.close()

