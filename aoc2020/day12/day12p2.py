from pathlib import Path
import collections
import enum
import attr


class Action(enum.Enum):
  North = 'N'
  South = 'S'
  East = 'E'
  West = 'W'
  SpinLeft = 'L'
  SpinRight = 'R'
  Forward = 'F'


def move(x, y, direction, amt):
  if direction is Action.North:
    y += amt
  elif direction is Action.South:
    y -= amt
  elif direction is Action.East:
    x += amt
  elif direction is Action.West:
    x -= amt
  
  return x, y


def rotate(x, y, turn, amt):
  if amt == 180:
    x, y = -x, -y

  elif turn is Action.SpinRight:
    if amt == 90:
      x, y = y, -x
    elif amt == 270:
      x, y = -y, x

  elif turn is Action.SpinLeft:
    if amt == 90:
      x, y = -y, x
    elif amt == 270:
      x, y = y, -x
  
  return x, y


@attr.frozen
class Instruction:
  a: Action
  v: int

  def __str__(self):
    return f'{self.a.name} {self.v}'


def parse(datafile):
  with open(datafile, 'r', encoding='utf-8') as infile:
    for line in infile:
      line = line.strip()
      if not line:
        continue

      yield Instruction(
        a=Action(line[0]),
        v=int(line[1:]),
      )


def main():
  datafile = Path('./sample.txt')
  datafile = Path('./data.txt')
  datafile = Path('./data-drew.txt')

  instructions = parse(datafile)
  
  sh_x, sh_y = 0, 0
  wp_x, wp_y = 10, 1

  for inst in instructions:
    if inst.a in (Action.East, Action.West, Action.North, Action.South):
      wp_x, wp_y = move(wp_x, wp_y, inst.a, inst.v)

    elif inst.a in (Action.SpinLeft, Action.SpinRight):
      wp_x, wp_y = rotate(wp_x, wp_y, inst.a, inst.v)

    elif inst.a is Action.Forward:
      for _ in range(inst.v):
        sh_x += wp_x
        sh_y += wp_y

  print('distance:', abs(sh_x) + abs(sh_y))


if __name__ == '__main__':
  import time
  start = time.perf_counter()
  main()
  end = time.perf_counter()
  print(f"Runtime: {end - start:.3f}s")

