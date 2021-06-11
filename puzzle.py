import sqlite3, random
import numpy as np


class Puzzle:

    def __init__(self, difficulty):
        self.difficulty = difficulty

    def get_singleword(self, length):
        con = sqlite3.connect("woordenboek.db")
        c = con.cursor()

        c.execute(f"SELECT * FROM woorden WHERE length(woord) == {length+1} ORDER BY RANDOM() Limit 1")

        return c.fetchone()[0]

    # def get_cells(self, amount, max_lenght, min_lenght):
    #     cel_lst_h = []
    #     cel_lst_v = []
    #
    #     h_amount = amount - random.randint(round(amount/3), round(amount/2))
    #     v_amount = amount - h_amount
    #
    #     for i in range(round(h_amount)):
    #         randint = random.randint(min_lenght, max_lenght)
    #         cel_lst_h.append(self.get_singleword(randint))
    #
    #     for i in range(round(v_amount)):
    #         randint = random.randint(min_lenght, max_lenght)
    #         cel_lst_v.append(self.get_singleword(randint))
    #
    #     return cel_lst_h, cel_lst_v

    def generate_grid(self, max_lenght):
        grid = np.chararray((max_lenght,max_lenght))
        grid.fill("*")
        return grid

    def fill_grid(self, word, coordinates, max_lenght):
        grid = self.generate_grid(max_lenght)

        for i in range(len(word)):
            c_pos = coordinates[i]
            grid[(c_pos[0])][(c_pos[1])] = word[i]

        return grid



coor = [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6]]

p1 = Puzzle(1)
print(p1.fill_grid("halloo", coor, 7))
