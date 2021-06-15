import sqlite3, random
import numpy as np


class Puzzle:

    def __init__(self, difficulty, grid):
        self.difficulty = difficulty
        self.grid = grid

    def get_singleword(self, length):
        con = sqlite3.connect("woordenboek.db")
        c = con.cursor()

        c.execute(f"SELECT * FROM woorden WHERE length(woord) == {length+1} ORDER BY RANDOM() Limit 1")

        return c.fetchone()[0]


    def get_grid(self):
        return self.grid

    def set_grid(self, grid):
        self.grid = grid

    def generate_grid(self, max_lenght):
        grid = np.chararray((max_lenght, max_lenght), 1, True)
        grid.fill("*")

        self.set_grid(grid)
        return grid

    def fill_grid(self, word, coordinates):
        newgrid = self.get_grid()

        for i in range(len(word)):
            c_pos = coordinates[i]
            newgrid[(c_pos[0])][(c_pos[1])] = word[i]
            print(newgrid[(c_pos[0])][(c_pos[1])])

        self.set_grid(newgrid)
        return newgrid

    def intersection_check(self, coordinates):
        grid = self.get_grid()
        intersections = []
        for c in coordinates:
            if grid[c[0]][c[1]] == "*":
                continue
            else:
                intersections.append(c)

        if len(intersections) == 0:
            return 1
        else:
            return intersections

    def generate_coordiante(self, word_lenght, axis, grid_size):
        grid = self.get_grid()
        coordinates = []
        tmp = []
        for i in range(grid_size-word_lenght):
            tmp.append(grid[i])

        rows = np.shape(tmp)[0]
        colum_lenght = np.shape(tmp)[1]

        print(rows, colum_lenght)

        if axis == [0, 1]:
            start = [random.randint(0, colum_lenght), random.randint(0, rows)]
        else:
            start = [random.randint(0, rows), random.randint(0, colum_lenght)]

        coordinates.append(start)

        for i in range(word_lenght-1):
            start = start[0] + axis[0], start[1] + axis[1]
            coordinates.append(start)


    def get_crosswords(self, amount, min_lenght, max_lenght):

        h_words = []

        v_word = []

        h_amount = amount - random.randint(round(amount/3), round(amount/2))
        v_amount = amount - h_amount

        for i in range(round(h_amount)):
            h_word_lenght = random.randint(min_lenght, max_lenght)
            h_words.append(self.get_singleword(h_word_lenght))

        for i in range(round(v_amount)):
            v_word_lenght = random.randint(min_lenght, max_lenght)
            v_word.append(self.get_singleword(v_word_lenght))

        return h_words, v_word

    def generate_puzzle(self):
        pass


coor = [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6]]

p1 = Puzzle(1, np.chararray([]))
p1.generate_grid(15)
p1.generate_coordiante(8, [1,0], 15)
