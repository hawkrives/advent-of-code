from pathlib import Path
import collections
import enum
import attr
from contextlib import contextmanager
import time
import array


@attr.frozen
class Mask:
  mask: str

  def apply(self, value: str):
    value = value.rjust(36, '0')
    value = [ch for ch in value]
    for i, bit in enumerate(self.mask):
      if bit == 'X':
        continue

      value[i] = bit

    value = ''.join(value)
    value = value.lstrip('0')

    return value


@attr.frozen
class Assign:
  index: int
  value: int


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

  mask = Mask('X' * 36)
  for line in parse(datafile):
    lhs, rhs = line.split(' = ')

    if lhs == 'mask':
      mask = Mask(rhs)
    else:
      # find the address
      index = int(lhs[4:-1])
      # convert the rhs into a base-2 string
      rhs = bin(int(rhs, base=10))[2:]
      # apply the current mask to the value
      rhs = mask.apply(rhs)
      # convert the value into an integer
      value = int(rhs, base=2)
      # return it
      yield Assign(index, value)


def main():
  data = load()

  memory = {}
  for inst in data:
    memory[inst.index] = inst.value

  #print(memory)
  s = sum(memory.values())
  print(f'{s:,}')


if __name__ == '__main__':
  with timed():
    main()

