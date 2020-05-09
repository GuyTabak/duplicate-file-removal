# playground for sqlite
import sqlite3

conn = sqlite3.connect('example.db')
c = conn.cursor()
# c.execute('''CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)''')
# c.execute("INSERT INTO stocks VALUES ('2006-01-05', 'BUY', 'RHAT', 100, 35.14)")
conn.commit()
# conn.close()

c.execute('SELECT * FROM stocks WHERE symbol=?', ('RHAT',))
print(c.fetchone())

# Larger example that inserts many records at a time
purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
             ]
c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
conn.commit()

if __name__ == "__main__":
    print("yay")
