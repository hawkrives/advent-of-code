'''

Your puzzle answer was 10774.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

Time to improve the polymer.

One of the unit types is causing problems; it's preventing the polymer from collapsing as much as it should. Your goal is to figure out which unit type is causing the most problems, remove all instances of it (regardless of polarity), fully react the remaining polymer, and measure its length.

For example, again using the polymer dabAcCaCBAcCcaDA from above:

Removing all A/a units produces dbcCCBcCcD. Fully reacting this polymer produces dbCBcD, which has length 6.
Removing all B/b units produces daAcCaCAcCcaDA. Fully reacting this polymer produces daCAcaDA, which has length 8.
Removing all C/c units produces dabAaBAaDA. Fully reacting this polymer produces daDA, which has length 4.
Removing all D/d units produces abAcCaCBAcCcaA. Fully reacting this polymer produces abCBAc, which has length 6.
In this example, removing all C/c units was best, producing the answer 4.

What is the length of the shortest polymer you can produce by removing all units of exactly one type and fully reacting the result?
'''

from lib import timeit

samples = {
  'dabAcCaCBAcCcaDA': 'daDA',
}


def solve(data):
  current = data
  last = ''

  letters = [(chr(a), chr(a).upper()) for a in range(ord('a'), ord('z') + 1)]
  letters = [(a+A, A+a) for a, A in letters]

  while current != last:
    last = current

    for aA, Aa in letters:
      current = current.replace(aA, '').replace(Aa, '')

  return current


def an_experiment(data, a, A):
  with timeit(a):
    reduced = data.replace(a, '').replace(A, '')
    return solve(reduced)


def experiment(data):
  data = data.strip()

  letters = [(chr(a), chr(a).upper()) for a in range(ord('a'), ord('z') + 1)]
  
  results = [an_experiment(data, a, A) for a, A in letters]

  return min(results, key=len)


def evaluate(data):
  data = data.strip()
  print(len(experiment(data)))


def test(samples):
  for i, (input, expected) in enumerate(samples.items()):
    actual = experiment(input)
    if actual == expected:
      print('solved', i)
    else:
      print(f"problem {i}:")
      print(f"  input: '{input}'")
      print(f"  output: '{actual}'")
      print(f"  expect: '{expected}'")

if __name__ == '__main__':
  from lib import read_input
  
  with timeit('sample'):
    test(samples)
  
  with timeit('data'):
    evaluate(read_input()[0])
