import sqlite3, random
import numpy as np

class puzzle:

    grid: list

    def __init__(self, grid):
        self.grid = grid

    def get_grid(self):
        return self.grid

    def set_grid(self, grid):
        self.grid = grid

    def get_singleword(self, length, condition):
        con = sqlite3.connect("woordenboek.db")
        c = con.cursor()

        c.execute(f"SELECT * FROM woorden WHERE LENGTH(woord) == {length+1} {condition} ORDER BY RANDOM() Limit 1;")

        return c.fetchone()[0]

    def set_blank_grid(self, grid_size):
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

    def get_crossword(self, min_lenght, max_lenght, grid_size, used_coordinates, words, min_crossings, max_crossings,
                      axis, currently_faulty_coordinates, repeats):
        if repeats > 50:
            return TypeError
        else:
            word_lenght = random.randint(min_lenght, max_lenght)

            used_point_lst = []
            for used_coordinate_set in used_coordinates:
                for used_point in used_coordinate_set:
                    used_point_lst.append(used_point)

            gen_coordiantes = self.generate_coordiante(word_lenght, axis, grid_size)
            intersection_info = self.get_intersection_info(gen_coordiantes)

            for point in gen_coordiantes:
                if point in used_point_lst or\
                        gen_coordiantes in currently_faulty_coordinates\
                        or intersection_info.count("*") >= word_lenght + 1 - min_crossings\
                        or intersection_info.count("*") < word_lenght - max_crossings:

                    currently_faulty_coordinates.append(gen_coordiantes)
                    repeats += 1
                    return self.get_crossword(min_lenght, max_lenght, grid_size, used_coordinates, words, min_crossings,
                                              max_crossings, axis, currently_faulty_coordinates, repeats)

            if intersection_info.count("*") == word_lenght:
                condition = ""
            else:   # create condition
                condition = "AND woord LIKE '"
                for i in intersection_info:
                    if i == "*":
                        condition = (condition + "_")
                    else:
                        condition = (condition + f"{i}")

                condition = (condition + "%'")

            try:
                woord = self.get_singleword(word_lenght, condition)
                words.append(woord)
                used_coordinates.append(gen_coordiantes)

                self.fill_grid(woord, gen_coordiantes)
            except TypeError:
                currently_faulty_coordinates.append(gen_coordiantes)
                repeats += 1
                return self.get_crossword(min_lenght, max_lenght, grid_size, used_coordinates, words, min_crossings,
                                          max_crossings, axis, currently_faulty_coordinates, repeats)

            return used_coordinates, words

    def fill_in_crosswords(self, word_count, min_length, max_length, min_crossings, max_crossings, grid_size):
        h_words = []
        v_words = []

        h_coordinates = []
        v_coordinates = []

        # generate vertical and horizontal words so the other words can be crossed with the minimal amount of crossings
        try:
            initial_min_crossings = 0
            for i in range(min_crossings):

                h_coordinates, h_words = self.get_crossword(min_length, max_length, grid_size, h_coordinates, h_words,
                                                            initial_min_crossings, max_crossings, [0, 1], [], 0)
                initial_min_crossings += 1

                v_coordinates, v_words = self.get_crossword(min_length, max_length, grid_size, v_coordinates, v_words,
                                                            initial_min_crossings, max_crossings, [1, 0], [], 0)

            for i in range(int(word_count-(word_count/2)-min_crossings)):

                h_coordinates, h_words = self.get_crossword(min_length, max_length, grid_size, h_coordinates, h_words,
                                                            min_crossings, max_crossings, [0, 1], [], 0)

                v_coordinates, v_words = self.get_crossword(min_length, max_length, grid_size, v_coordinates, v_words,
                                                            min_crossings, max_crossings, [1, 0], [], 0)

            return h_coordinates, v_coordinates, h_words, v_words

        except TypeError:
            self.set_blank_grid(grid_size)
            return self.fill_in_crosswords(word_count, min_length, max_length, min_crossings, max_crossings, grid_size)

    def generate_puzzle(self, word_count, min_lenght, max_lenght, min_crossings, max_crossings):
        if word_count > max_lenght:
            grid_size = word_count + 2
        else:
            grid_size = max_lenght + 2

        self.set_blank_grid(grid_size)

        h_coordinates, v_coordinates, h_words, v_words = self.fill_in_crosswords(word_count, min_lenght, max_lenght,
                                                                                 min_crossings, max_crossings,grid_size)
        print(self.get_grid())
        return self.get_grid(), h_coordinates, v_coordinates, h_words, v_words, grid_size
