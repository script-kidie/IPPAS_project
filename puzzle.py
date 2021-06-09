import sqlite3, random


class Puzzle:

    def __init__(self, difficulty):
        self.cels = difficulty

    def get_singleword(self, length):
        con = sqlite3.connect("woordenboek.db")
        c = con.cursor()

        c.execute(f"SELECT * FROM woorden WHERE length(woord) == {length+1} ORDER BY RANDOM() Limit 1" )

        return c.fetchone()[0]


    def get_cells(self, amount, max_lenght, min_lenght):
        cel_lst_h = []
        cel_lst_v = []

        h_amount = amount - random.randint(round(amount/3), round(amount/2))
        v_amount = amount - h_amount

        for i in range(round(h_amount)):
            randint = random.randint(min_lenght, max_lenght)
            cel_lst_h.append(self.get_singleword(randint))

        for i in range(round(v_amount)):
            randint = random.randint(min_lenght, max_lenght)
            cel_lst_v.append(self.get_singleword(randint))

        return cel_lst_h, cel_lst_v



p1 = Puzzle(1)
print(p1.get_cells(10, 7, 3))
