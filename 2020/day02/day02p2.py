sample = '''
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
'''

import sqlite3

def main(data):
  conn = sqlite3.connect('./day02p2.db')
  conn.row_factory = sqlite3.Row
  
  conn.execute('''
    create table if not exists data (
      pos1 int not null check (pos1 > 0),
      pos2 int not null check (pos2 > 0),
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
        pos1, pos2 = bounds.split('-')
        char = char[0]
    
        conn.execute('''
          insert into data (pos1, pos2, char, password)
          values (?, ?, ?, ?)
        ''', [int(pos1), int(pos2), char, password])
  
  curs = conn.cursor()
  
  curs.execute('''
    SELECT count(*) FROM (
      SELECT pos1
        , pos2
        , char
        , password
        , substr(password, pos1, 1) as c1
        , substr(password, pos2, 1) as c2
      FROM data
    ) processed
    WHERE (char = c1 AND char != c2)
       OR (char = c2 AND char != c1)
  ''')
  
  for record in curs:
    print(dict(record))


if __name__ == '__main__':
  with open('./day02.txt', 'r', encoding='utf-8') as infile:
    data = infile.read()

  #main(sample)
  main(data)
