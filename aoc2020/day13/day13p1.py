from pathlib import Path
import collections
import enum
import attr
from contextlib import contextmanager
import time


@contextmanager
def timed():
  start = time.perf_counter()
  yield
  end = time.perf_counter()
  print(f"Runtime: {end - start:.3f}s")


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
  
  ts = int(lines[0])
  ids = set(lines[1].split(','))
  ids.remove('x')
  
  return ts, sorted(int(bid) for bid in ids)


def main():
  ts, bus_ids = load()
  print('ts:', ts)
  
  potential = dict()
  
  for bid in bus_ids:
    departures = range(ts - (ts % bid), ts + bid, bid)
    
    for d in departures:
      if d < ts:
        continue
      
      potential[d] = bid
  
  nearest = min((p for p in potential.keys()), key=lambda p: p - ts)
  
  best_bid = potential[nearest]
  to_wait = nearest - ts
  
  print('route', best_bid)
  print('wait', to_wait)
  print('answer', best_bid * to_wait)


if __name__ == '__main__':
  with timed():
    main()

