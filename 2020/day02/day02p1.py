sample = '''
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
'''

import sqlite3

def main(data):
  conn = sqlite3.connect('./day02p1.db')
  conn.row_factory = sqlite3.Row

  conn.execute('''
    create table if not exists data (
      min int not null,
      max int not null,
      char text not null,
      password text not null
    )
  ''')

  with conn:
    curs = conn.cursor()
    curs.execute('select count(*) from data')
    if curs.fetchone()[0] == 0:
      for line in data.split('\n'):
        line = line.strip()
        if not line:
          continue
        bounds, char, password = line.split()
        lower, upper = bounds.split('-')
        char = char[0]

        conn.execute('''
          insert into data (min, max, char, password)
          values (?, ?, ?, ?)
        ''', [int(lower), int(upper), char, password])

  curs = conn.cursor()

  curs.execute('''
    SELECT count(*) FROM (
      SELECT min
        , max
        , char
        , password
        , replace(password, char, '') as replaced
      FROM data
    ) processed
    WHERE password != replaced
      AND length(password) - length(replaced) >= min
      AND length(password) - length(replaced) <= max
  ''')

  for record in curs:
    print(dict(record))

if __name__ == '__main__':
  with open('./day02.txt', 'r', encoding='utf-8') as infile:
    data = infile.read()

  #main(sample)
  main(data)
