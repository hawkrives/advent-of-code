from pathlib import Path
import collections
import enum
import itertools
import attr
import math
from contextlib import contextmanager


@contextmanager
def timed(label=''):
  import time
  start = time.perf_counter()
  yield
  end = time.perf_counter()
  print(f"{label} runtime: {end - start:.3f}s")
  print()


def parse(datafile):
  with open(datafile, 'r', encoding='utf-8') as infile:
    for line in infile:
      line = line.strip()

      if not line:
        continue

      yield line


def load():
  datafile = Path('./sample.txt')
  datafile = Path('./data.txt')
  #datafile = Path('./data-drew.txt')

  lines = list(parse(datafile))
  
  assert len(lines) == 2

  return lines[1]


def find_earliest(intervals):
  originals = intervals
  print(originals)
  intervals = [
    int(x) if x != 'x' else None
    for x in intervals.split(',')
  ]
  
  initial_interval = next(n for n in intervals if n is not None)

  # range_end = 922337203685477580
  #ranges = {
    #interval: range(0, range_end, interval) if interval is not None else None
    #for interval in intervals
  #}

  start_ts = 0  # start at 1 with the first iter
  
  #times = range(0, range_end, intervals[0])
  #print(times)

  while True:
    ts = start_ts

    if ts > 0 and ts % 1_000_000 == 0:
      print(f'... {ts:,}')

    this_round_ok = True
    for interval in intervals:
      if interval is None:
        ts += 1
      elif ts % interval == 0:
        ts += 1
      else:
        this_round_ok = False
        break

    if this_round_ok:
      break

    start_ts += initial_interval

  print(f'-> {start_ts:,}')
  return start_ts


def lcm(a, b):
    return (a * b) // math.gcd(a, b)


def test():
  with timed('block 1'):
    assert find_earliest('17,x,13,19') == 3_417

  with timed('block 2'):
    assert find_earliest('67,7,59,61') == 754_018

  with timed('block 3'):
    assert find_earliest('67,x,7,59,61') == 779_210

  with timed('block 4'):
    assert find_earliest('67,7,x,59,61') == 1_261_476

  with timed('block 5'):
    assert find_earliest('1789,37,47,1889') == 1_202_161_486
  
  with timed('main'):
    find_earliest(load())


if __name__ == '__main__':
  #with timed():
  #  main()
  #import sys
  #print(sys.maxsize)
  test()

