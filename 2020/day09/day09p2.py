from itertools import islice, tee, combinations
from pathlib import Path

def window(iterable, size):
  '''https://stackoverflow.com/a/54110047/2347774'''
  iterators = tee(iterable, size) 
  iterators = [islice(iterator, i, None) for i, iterator in enumerate(iterators)]  
  yield from zip(*iterators)


def is_empty(it):
  for _ in it:
    return False
  return True


def find_invalid(data, size=25):
  for w in window(data, size+1):
    n = w[size]

    candidates = (
      (a,b) 
      for a, b in combinations(w[0:size], 2)
      if a + b == n
    )

    if is_empty(candidates):
      return n


def main(data, size=25):
  invalid = find_invalid(data, size=size)
  
  for n in range(2, len(data) + 1):
    for w in window(data, n):
      w = list(w)
      if sum(w) == invalid:
        return min(w) + max(w)


#file = Path('./sample-25.txt')
#file = Path('./sample-5.txt')
file = Path('./data.txt')

with file.open('r', encoding='utf-8') as infile:
  data = [int(line) for line in infile]
  
print(main(data, 25))

