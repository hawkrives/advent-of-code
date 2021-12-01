from contextlib import contextmanager
import time


@contextmanager
def timed(label='Runtime'):
  start = time.perf_counter()
  yield
  end = time.perf_counter()
  print(f"{label}: {end - start:.3f}s")


def evaluate(starting):
  history = {v: [turn + 1] for turn, v in enumerate(starting)}

  last_spoken = starting[-1]
  for turn in range(len(starting) + 1, 2021):
    # we need to know the number of times last_spoken has been said
    # and we need to know the most recent two turns on which the it was said
    turns_spoken = history.setdefault(last_spoken, [])

    if len(turns_spoken) < 2:
      value = 0
    else:
      value = turns_spoken[-1] - turns_spoken[-2]
    
    last_spoken = value
    history.setdefault(last_spoken, []).append(turn)

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
  tests()

  input = (15,5,1,4,7,0)
  with timed(str(input)):
    print(evaluate(input))
