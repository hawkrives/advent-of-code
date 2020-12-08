'''
--- Day 3: No Matter How You Slice It ---

The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit (thanks to someone who helpfully wrote its box IDs on the wall of the warehouse in the middle of the night). Unfortunately, anomalies are still affecting them - nobody can even agree on how to cut the fabric.

The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for Santa's suit. All claims have an ID and consist of a single rectangle with edges parallel to the edges of the fabric. Each claim's rectangle is defined as follows:

The number of inches between the left edge of the fabric and the left edge of the rectangle.
The number of inches between the top edge of the fabric and the top edge of the rectangle.
The width of the rectangle in inches.
The height of the rectangle in inches.

A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge, 2 inches from the top edge, 5 inches wide, and 4 inches tall. Visually, it claims the square inches of fabric represented by # (and ignores the square inches of fabric represented by .) in the diagram below:

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........

The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example, consider the following claims:

#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2

Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........

The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric are within two or more claims?
'''

from lib import read_input
import collections
import itertools

input = read_input()
test_input = '''
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
'''
test_input = [s for s in test_input.splitlines() if s]


class Claim(object):
  def __init__(self, claim_line):
    num, _, coords, area = claim_line.split()
    #print(num, coords, area)
    
    num = int(num[1:])
    coords = [int(n) for n in coords[:-1].split(',')]
    area = [int(n) for n in area.split('x')]
    
    self.num = num
    self.x, self.y = coords[0], coords[1]
    self.w, self.h = area[0], area[1]
    self.x2 = self.x + self.w
    self.y2 = self.y + self.h


class Board(object):
  EMPTY = '•'
  SINGLE = '*'
  DOUBLED = 'X'

  def __init__(self, w, h):
    self.w = w
    self.h = h
    self.cells = [
      [[] for col in range(w)] 
      for row in range(h)
    ]
  
  def to_symbols(self):
    for row in self.cells:
      for cell in row:
        if len(cell) is 0:
          yield self.EMPTY
        elif len(cell) is 1:
          yield self.SINGLE
        else:
          yield self.DOUBLED
      yield '\n'

  def format(self):
    return ''.join(self.to_symbols())

  def insert(self, claim):
    for i in range(claim.x, claim.x2):
      for j in range(claim.y, claim.y2):
        self.cells[i][j].append(claim.num)
  
  def double_claimed(self):
    return len([cell for row in self.cells for cell in row if len(cell) > 1])
  
  def print_cells(self):
    for row in self.cells:
      print(row)


def solve(values):
  largest_x = max([c.x2 for c in values])
  largest_y = max([c.y2 for c in values])
  b = Board(largest_x + 1, largest_y + 1)
  for claim in values:
    b.insert(claim)
  print(b.double_claimed())
  b.print_cells()


if __name__ == '__main__':
  test_input = [Claim(c) for c in test_input]
  solve(test_input)
  
  input = [Claim(c) for c in input]
  solve(input)

