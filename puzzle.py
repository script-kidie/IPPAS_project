import sqlite3, random
import numpy as np


class Puzzle:

    def __init__(self, difficulty, grid):
        self.difficulty = difficulty
        self.grid = grid

    def get_singleword(self, length, condition):
        con = sqlite3.connect("woordenboek.db")
        c = con.cursor()

        c.execute(f"SELECT * FROM woorden WHERE length(woord) == {length+1} {condition} ORDER BY RANDOM() Limit 1;")

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

    def intersection_check(self, coordinates):
        grid = self.get_grid()
        intersections = []

        for c in coordinates:
            if grid[c[0]][c[1]] == "*":
                intersections.append("*")
            else:
                intersections.append(c)

        if intersections.count("*") == len(intersections):
            return 1
        else:
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

    def get_crossword(self, amount, min_lenght, max_lenght, grid_size, used_coordinates, h_words, min_crossings):
        for i in range(round(amount)):
            word_lenght = random.randint(min_lenght, max_lenght)

            invalid_coordinates = True
            while invalid_coordinates:
                invalid_coordinates = False

                coordiantes = self.generate_coordiante(word_lenght, [0, 1], grid_size)
                intersection_info = self.intersection_check(coordiantes)

                for coordinate in coordiantes:
                    if coordinate in used_coordinates\
                            or intersection_info.count("*") >= word_lenght + 1 - min_crossings:
                        invalid_coordinates = True
                        break

            used_coordinates.append(coordiantes)

            condition = "AND WHERE woord LIKE "
            for i in intersection_info:
                if i == "*":
                    condition = (condition + "_")
                else:
                    condition = (condition + f"{i}")

            word = self.get_singleword(word_lenght, condition)
            h_words.append(word)

            self.fill_grid(word, coordiantes)

            return used_coordinates, h_words

    def fill_in_crosswords(self, word_count, min_lenght, max_lenght, min_crossings, grid_size):

        h_words = []
        v_words = []

        h_amount = word_count - random.randint(round(word_count / 3), round(word_count / 2))
        v_amount = word_count - h_amount

        h_amount -= min_crossings
        v_amount -= min_crossings

        h_coordinates = []
        v_coordinates = []

        for i in range(min_crossings):
            h_coordinates, h_words = self.get_crossword(self, h_amount, min_lenght, max_lenght, grid_size,
                                                        h_coordinates, h_words, 0)

            v_coordinates, v_words = self.get_crossword(self, v_amount, min_lenght, max_lenght, grid_size,
                                                        v_coordinates, v_words, 0)

        h_coordinates, h_words = self.get_crossword(self, h_amount, min_lenght, max_lenght, grid_size, h_coordinates,
                                                    h_words, min_crossings)

        v_coordinates, v_words = self.get_crossword(self, v_amount, min_lenght, max_lenght, grid_size, v_coordinates,
                                                    v_words, min_crossings)

        print(f"h={h_words} \n v={v_words}")

        return 1

    def generate_puzzle(self, word_count, min_lenght, max_lenght, min_crossings):
        grid_size = max_lenght + 2

        self.generate_grid(grid_size)
        print(self.get_grid())
        self.fill_in_crosswords(word_count, min_lenght, max_lenght, min_crossings, grid_size)

        return self.get_grid()


p1 = Puzzle(1, np.chararray([]))

print(p1.generate_puzzle(10, 3, 10, 2))
