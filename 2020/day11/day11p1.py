import sqlite3
import pathlib
from collections import defaultdict
from copy import deepcopy

def _board(seats):
  for x, row in seats.items():
    #print(x, row)
    for y, occu in row.items():
      if occu is None:
        yield '.'
      elif occu is True:
        yield '#'
      else:
        yield 'L'
    
    yield '\n'

def board(seats):
  return ''.join(_board(seats))

def main():
  seats = dict()

  datafile = pathlib.Path('./sample.txt')
  datafile = pathlib.Path('./data.txt')

  with datafile.open('r', encoding='utf-8') as infile:
    for x, row in enumerate(infile):
      #print(x)
      seats[x] = dict()

      for y, cell in enumerate(row):
        #print((x,y))
        if cell == 'L':
          occ = False
        elif cell == '#':
          occ = True
        elif cell == '.':
          occ = None
        else:
          continue
        
        seats[x][y] = occ

  round = 0
  while True:
  #for _ in range(2):
    print('round', round)
    print('before:', count_occupied(seats))
    print(board(seats))
    
    p_seats = {
      k: {k2: v2 for k2, v2 in v.items()}
      for k, v in seats.items()
    }

    for x, row in p_seats.items():
      for y, cell_occ in row.items():
        if cell_occ is None:
          continue

        north_row = p_seats.get(x-1, {})
        south_row = p_seats.get(x+1, {})
        
        nw = north_row.get(y-1, False) or False
        n  = north_row.get(y, False) or False
        ne = north_row.get(y+1, False) or False
        
        w = row.get(y-1, False) or False
        e = row.get(y+1, False) or False
        
        sw = south_row.get(y-1, False) or False
        s  = south_row.get(y, False) or False
        se = south_row.get(y+1, False) or False

        adjacent_occ = (
          nw + n + ne +
           w +   +  e +
          sw + s + se
        )
        
        if cell_occ is False and adjacent_occ == 0:
          seats[x][y] = True
        elif cell_occ is True and adjacent_occ >= 4:
          seats[x][y] = False
    
    print('after:', count_occupied(seats))
    print(board(seats))
    
    if seats == p_seats:
      print(count_occupied(seats), 'seats occupied')
      break
    
    print()
    print()
    round += 1


def count_occupied(seats):
  acc = 0
  for x, row in seats.items():
    for y, cell_occ in row.items():
      if cell_occ:
        acc += 1
  return acc

if __name__ == '__main__':
  main()

