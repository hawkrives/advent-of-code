import sqlite3
import pathlib

def main():
  conn = sqlite3.connect(':memory:')
  
  conn.execute('''
    create table seat (
      row int not null,
      col int not null,
      occ bool not null,
      flr bool not null,
      primary key (row, col)
    )
  ''')

  conn.execute('''
    create table state as
    select * from seat
  ''')

  conn.execute('''
    create view board as
    with data as (
      select row
           , col
           , case
               when flr = true then '.'
               when occ = true then '#' 
               when occ = false then 'L'
               else ' '
             end cell
      from seat 
      order by row, col
    )

    , rows as (
      select row
           , group_concat(cell, '') as cell
      from data
      group by row
      order by row
    )

    select group_concat(cell, char(10)) as board
    from rows
  ''')
  
  conn.execute('''
    create view pboard as
    with data as (
      select row
           , col
           , case
               when flr = true then '.'
               when occ = true then '#' 
               when occ = false then 'L'
               else ' '
             end cell
      from state 
      order by row, col
    )

    , rows as (
      select row
           , group_concat(cell, '') as cell
      from data
      group by row
      order by row
    )

    select group_concat(cell, char(10)) as board
    from rows
  ''')
  
  conn.execute('''
    create view occupied as
    select
        c.row
      , c.col
      , c.occ
      , (
            coalesce(nw.occ, 0) 
          + coalesce(n.occ, 0)
          + coalesce(ne.occ, 0)
          + coalesce(w.occ, 0)       
          + coalesce(e.occ, 0)
          + coalesce(sw.occ, 0)
          + coalesce(s.occ, 0)
          + coalesce(se.occ, 0)
        ) as num_occ
  
    from state c
      left join state nw on nw.row = c.row-1 and nw.col = c.col-1
      left join state n on n.row = c.row-1 and n.col = c.col
      left join state ne on ne.row = c.row-1 and ne.col = c.col+1
  
      left join state w on w.row = c.row and w.col = c.col-1
      left join state e on e.row = c.row and e.col = c.col+1
  
      left join state sw on sw.row = c.row+1 and sw.col = c.col-1
      left join state s on s.row = c.row+1 and s.col = c.col
      left join state se on se.row = c.row+1 and se.col = c.col+1
  ''')
  
  datafile = pathlib.Path('./sample.txt')
  
  with datafile.open('r', encoding='utf-8') as infile, conn:
    curs = conn.cursor()
    
    for x, row in enumerate(infile):
      for y, cell in enumerate(row):
        flr = False
        if cell == 'L':
          occ = False
        elif cell == '#':
          occ = True
        elif cell == '.':
          occ = False
          flr = True

        curs.execute('''
          insert into seat (row, col, occ, flr) 
          values (?, ?, ?, ?)
        ''', (x, y, occ, flr))

  with conn:
    curs = conn.cursor()
    curs.execute('select board from board')
    initial = curs.fetchone()[0]
    print(initial)

  with conn:
    curs = conn.cursor()
    curs.execute('select * from seat')
    previous = curs.fetchall()
    
    curs.execute('''
      select *
      from occupied
    ''')

    for rec in curs:
      print(rec)
    
    print()
    
    for n in range(2):
      curs.execute('''
        delete from state
      ''')
      curs.execute('''
        insert into state
        select * from seat
      ''')
      curs.execute('''
        update seat as s
        set occ = case
          when flr = true then false
          
          when 
            occ = false
            --and t.num_occ = 0
            and (select num_occ from occupied o where (o.row, o.col) = (s.row, s.col)) = 0
          then true

          when
            occ = true
            --and t.num_occ >= 4
            and (select num_occ from occupied o where (o.row, o.col) = (s.row, s.col)) >= 4
          then false

          else occ

        end

        --from occupied t on (t.row, t.col) = (s.row, s.col)
      ''')
    
      curs.execute('select board from board')
      initial = curs.fetchone()[0]
      print(initial)
      print()
  

if __name__ == '__main__':
  main()
