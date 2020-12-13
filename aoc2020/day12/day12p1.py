from pathlib import Path
import collections
import enum
import attr


class Action(enum.Enum):
  North = 'N'
  South = 'S'
  East = 'E'
  West = 'W'
  TurnLeft = 'L'
  TurnRight = 'R'
  Forward = 'F'

HEADING_DIRECTION = {
  0: Action.East,
  270: Action.North,
  90: Action.South,
  180: Action.West,
}

DIRECTION_HEADING = {
  v: k for k, v in HEADING_DIRECTION.items()
}


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


def turn(heading, turn, amt):
  #print('currently heading', heading)
  #print('turning', turn, amt)
  deg = DIRECTION_HEADING[heading]

  if turn is Action.TurnRight:
    deg += amt
  elif turn is Action.TurnLeft:
    deg -= amt
  
  deg = deg % 360

  #print('rotating to', deg, HEADING_DIRECTION[deg])

  return HEADING_DIRECTION[deg]


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
  #datafile = Path('./data-drew.txt')

  instructions = parse(datafile)
  
  x, y = 0, 0
  heading = Action.East
  for inst in instructions:
    #print(inst)
    if inst.a in (Action.East, Action.West, Action.North, Action.South):
      x, y = move(x, y, inst.a, inst.v)

    elif inst.a in (Action.TurnLeft, Action.TurnRight):
      heading = turn(heading, inst.a, inst.v)

    elif inst.a is Action.Forward:
      x, y = move(x, y, heading, inst.v)

    else:
      raise Exception()

    #print(x, y)

  print('distance:', abs(x) + abs(y))


if __name__ == '__main__':
  import time
  start = time.perf_counter()
  main()
  end = time.perf_counter()
  print("Runtime:{:.3f}".format(end-start))
