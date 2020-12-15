from pathlib import Path
import collections
import enum
import attr
from contextlib import contextmanager
import time
import itertools


@contextmanager
def timed(label='Runtime'):
  start = time.perf_counter()
  yield
  end = time.perf_counter()
  print(f"{label}: {end - start:.3f}s")


def parse(datafile):
  with open(datafile, 'r', encoding='utf-8') as infile:
    for line in infile:
      line = line.strip()

      if not line:
        continue

      yield line


def load():
  datafile = Path('./sample.txt')
  #datafile = Path('./data.txt')
  #datafile = Path('./data-drew.txt')

  yield from parse(datafile)


def main():
  data = load()
  
  ...
  

def evaluate(starting):
  history = {v: [turn + 1] for turn, v in enumerate(starting)}

  last_spoken = starting[-1]
  for turn in range(len(starting) + 1, 30_000_000 + 1):
    if turn % 1_000_000 == 0:
      print(f'{turn:,}')
    # we need to know the number of times last_spoken has been said
    # and we need to know the most recent two turns on which the it was said
    turns_spoken = history.setdefault(last_spoken, [])

    #print(history)
    #print(turns_spoken)
    #print(last_spoken)

    if len(turns_spoken) < 2:
      value = 0
    else:
      value = turns_spoken[-1] - turns_spoken[-2]
    
    last_spoken = value
    history.setdefault(last_spoken, []).append(turn)
    
    #print('said', last_spoken)
    #print()

  return last_spoken


def tests():
  examples = [
    ((0,3,6), 436),
    ((1,3,2), 1),
    ((2,1,3), 10),
    ((1,2,3), 27),
    ((2,3,1), 78),
    ((3,2,1), 438),
    ((3,1,2), 1836),
  ]

  for input, expected in examples:
    with timed(str(input)):
      actual = evaluate(input)
      assert actual == expected, f'expected {input} == {expected:,}; got {actual}'


if __name__ == '__main__':
  #tests()

  input = (15,5,1,4,7,0)
  with timed(str(input)):
    print(evaluate(input))

