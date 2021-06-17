import sqlite3, random
import numpy as np


class Puzzle:

    def __init__(self, difficulty, grid):
        self.difficulty = difficulty
        self.grid = grid

    def get_singleword(self, length, condition):
        con = sqlite3.connect("woordenboek.db")
        c = con.cursor()

        c.execute(f"SELECT * FROM woorden WHERE LENGTH(woord) == {length+1} {condition} ORDER BY RANDOM() Limit 1;")

        return c.fetchone()[0]

    def get_grid(self):
        return self.grid

    def set_grid(self, grid):
        self.grid = grid

    def generate_grid(self, grid_size):
        grid = np.chararray((grid_size, grid_size), 1, True)
        grid.fill("*")

        self.set_grid(grid)
        return grid

    def fill_grid(self, word, coordinates):
        newgrid = self.get_grid()

        for i in range(len(word)-1):
            c_pos = coordinates[i]
            newgrid[(c_pos[0])][(c_pos[1])] = word[i]

        self.set_grid(newgrid)
        return newgrid

    def get_intersection_info(self, coordinates):
        grid = self.get_grid()
        intersections = []

        for c in coordinates:
            intersections.append(grid[c[0]][c[1]])

        return intersections

    def generate_coordiante(self, word_lenght, axis, grid_size):
        grid = self.get_grid()
        coordinates = []
        tmp = []
        for i in range(grid_size-word_lenght):
            tmp.append(grid[i])

        index_rows = np.shape(tmp)[0] - 1
        index_colum = np.shape(tmp)[1] - 1

        if axis == [0, 1]:
            start = [random.randint(0, index_colum), random.randint(0, index_rows)]
        else:
            start = [random.randint(0, index_rows), random.randint(0, index_colum)]

        coordinates.append(start)

        for i in range(word_lenght-1):
            start = start[0] + axis[0], start[1] + axis[1]
            coordinates.append(start)

        return coordinates

    def get_crossword(self, amount, min_lenght, max_lenght, grid_size, used_coordinates, h_words, min_crossings, axis):
        for i in range(round(amount)):
            word_lenght = random.randint(min_lenght, max_lenght)

            used_point_lst = []
            for used_coordinate_set in used_coordinates:
                for used_point in used_coordinate_set:
                    used_point_lst.append(used_point)

            invalid_coordinates = True
            while invalid_coordinates:

                invalid_coordinates = False

                gen_coordiantes = self.generate_coordiante(word_lenght, axis, grid_size)
                intersection_info = self.get_intersection_info(gen_coordiantes)

                print(f"used_point_lst: {used_point_lst}")
                for point in gen_coordiantes:
                    print(f"point={point}")
                    if point in used_point_lst or intersection_info.count("*") >= word_lenght + 1 - min_crossings:
                        invalid_coordinates = True
                        break

            used_coordinates.append(gen_coordiantes)

            if intersection_info.count("*") == word_lenght:
                condition = ""
            else:   # create condition
                condition = "AND woord LIKE '%"
                for i in intersection_info:
                    if i == "*":
                        condition = (condition + "_")
                    else:
                        condition = (condition + f"{i}")

                condition = (condition + "%'")
                print(f"condition: {condition}")
            try:
                woord = self.get_singleword(word_lenght, condition)
                print(f"lenght:{word_lenght}")
                print(f"woord:{woord}")
                h_words.append(woord)

                self.fill_grid(woord, gen_coordiantes)

                print(self.get_grid())
                print("\n")
            except TypeError:
                return self.get_crossword(amount, min_lenght, max_lenght, grid_size, used_coordinates, h_words,
                                           min_crossings, axis)

            return used_coordinates, h_words

    def fill_in_crosswords(self, word_count, min_lenght, max_lenght, min_crossings, grid_size):

        h_words = []
        v_words = []

        h_amount = word_count - random.randint(round(word_count / 3), round(word_count / 2))
        v_amount = word_count - h_amount

        print(f"min crossing = {min_crossings}")
        # h_amount -= min_crossings
        # v_amount -= min_crossings

        h_coordinates = []
        v_coordinates = []

        for i in range(min_crossings):
            print(f"horziantaal getV")
            h_coordinates, h_words = self.get_crossword(h_amount, min_lenght, max_lenght, grid_size,
                                                        h_coordinates, h_words, 0, [0, 1])
            print(f"verticaal getV")
            v_coordinates, v_words = self.get_crossword(v_amount, min_lenght, max_lenght, grid_size,
                                                        v_coordinates, v_words, 0, [1, 0])
        print("for loop over -----------\n\n")

        print(f"horziantaal getV")
        h_coordinates, h_words = self.get_crossword(h_amount, min_lenght, max_lenght, grid_size, h_coordinates,
                                                    h_words, min_crossings, [0, 1])
        print(f"verticaal getV")
        v_coordinates, v_words = self.get_crossword(v_amount, min_lenght, max_lenght, grid_size, v_coordinates,
                                                    v_words, min_crossings, [1, 0])

        print(f"h={h_words} \n v={v_words}")

        return 1

    def generate_puzzle(self, word_count, min_lenght, max_lenght, min_crossings):
        grid_size = max_lenght + 2

        self.generate_grid(grid_size)
        self.fill_in_crosswords(word_count, min_lenght, max_lenght, min_crossings, grid_size)

        return self.get_grid()


p1 = Puzzle(1, np.chararray([]))

print(p1.generate_puzzle(10, 3, 10, 2))
