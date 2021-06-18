import sqlite3, random
import numpy as np

con = sqlite3.connect("woordenboek.db")
c = con.cursor()

c.execute(f"SELECT * FROM woorden WHERE LENGTH(woord) == 6 AND woord LIKE '_t____%'ORDER BY RANDOM() Limit 1;")

print(c.fetchone())