import PySimpleGUI as sg
import random
import string


class Gui:

    def make_puzzle_words(self, h_words, v_words):
        str1 = "Horizontale woorden:\n"
        str2 = "Verticaale woorden:\n"
        word_number = 1

        for word in h_words:
            str1 = (str1 + f"  {word_number}.{word}")
            word_number += 1

        for word in v_words:
            str2 = (str2 + f"  {word_number}.{word}")
            word_number += 1

        return str(str1 + str2)

    def make_puzzle_page(self, grid_size, puzzle, first_grid_points, h_words, v_words, h_coordinates, v_coordinates):

        box_area = 25

        puzzle_words = self.make_puzzle_words(h_words, v_words)

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
            [sg.Button("Exit"), sg.Input(key="-IN-", size=(3, 3))]
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
                if point_coordinates in first_grid_points:
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

