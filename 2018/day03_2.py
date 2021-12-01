'''
Amidst the chaos, you notice that exactly one claim doesn't overlap by even a single square inch of fabric with any other claim. If you can somehow draw attention to it, maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are made.

What is the ID of the only claim that doesn't overlap?
'''

from day03_1 import Board, Claim
from lib import read_input, timeit

class Board2(Board):
  def find_singles(self):
    singles = set()
    blacklist = set()
    for row in self.cells:
      for cell in row:
        if len(cell) is 1:
          if cell[0] not in blacklist:
            singles.add(cell[0])
        else:
          for val in cell:
            singles.discard(val)
            blacklist.add(val)
    return singles

input = read_input()

test_input = '''
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
'''
test_input = [s for s in test_input.splitlines() if s]


def solve(values):
  with timeit('init'):
    largest_x = max([c.x2 for c in values])
    largest_y = max([c.y2 for c in values])
    b = Board2(largest_x + 1, largest_y + 1)
  with timeit('claims'):
    for claim in values:
      b.insert(claim)
  with timeit('find'):
    return b.find_singles()


if __name__ == '__main__':
  '''
  with timeit():
    test_input = [Claim(c) for c in test_input]
    solve(test_input)
  '''

  with timeit():
    input = [Claim(c) for c in input]
    print(solve(input))
    print(len(input))

