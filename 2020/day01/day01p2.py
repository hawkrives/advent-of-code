with open('./day01.txt', 'r', encoding='utf-8') as infile:
  data = [int(point) for point in infile.read().split() if point]

import sqlite3

conn = sqlite3.connect(':memory:')
conn.row_factory = sqlite3.Row

conn.execute('''
create table data (
  value int not null
)
''')

with conn:
  for point in data:
    conn.execute('''
      insert into data (value)
      values (?)
    ''', [point])

curs = conn.cursor()

curs.execute('''
SELECT a.value * b.value * c.value AS product
     , a.value as a
     , b.value as b
     , c.value as c
FROM data a, data b, data c
WHERE a.rowid NOT IN (b.rowid, c.rowid)
  AND b.rowid NOT IN (a.rowid, c.rowid)
  AND a.value + b.value + c.value = 2020
''')

print('match:', dict(curs.fetchone()))

