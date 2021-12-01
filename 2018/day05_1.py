'''
--- Day 5: Alchemical Reduction ---

You've managed to sneak in to the prototype suit manufacturing lab. The Elves are making decent progress, but are still struggling with the suit's size reduction capabilities.

While the very latest in 1518 alchemical technology might have solved their problem eventually, you can do better. You scan the chemical composition of the suit's material and discover that it is formed by extremely long polymers (one of which is available as your puzzle input).

The polymer is formed by smaller units which, when triggered, react with each other such that two adjacent units of the same type and opposite polarity are destroyed. Units' types are represented by letters; units' polarity is represented by capitalization. For instance, r and R are units with the same type but opposite polarity, whereas r and s are entirely different types and do not react.

For example:

In aA, a and A react, leaving nothing behind.
In abBA, bB destroys itself, leaving aA. As above, this then destroys itself, leaving nothing.
In abAB, no two adjacent units are of the same type, and so nothing happens.
In aabAAB, even though aa and AA are of the same type, their polarities match, and so nothing happens.

Now, consider a larger example, dabAcCaCBAcCcaDA:

dabAcCaCBAcCcaDA  The first 'cC' is removed.
dabAaCBAcCcaDA    This creates 'Aa', which is removed.
dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
dabCBAcaDA        No further actions can be taken.
After all possible reactions, the resulting polymer contains 10 units.

How many units remain after fully reacting the polymer you scanned? (Note: in this puzzle and others, the input is large; if you copy/paste your input, make sure you get the whole thing.)
'''

samples = {
  'aA': '',
  'zZ': '',
  'abBA': '',
  'abAB': 'abAB',
  'aabAAB': 'aabAAB',
  'dabAcCaCBAcCcaDA': 'dabCBAcaDA',
}


def solve(data):
  data = data.strip()

  this = data
  last = ''

  letters = [(chr(a), chr(a).upper()) for a in range(ord('a'), ord('z') + 1)]
  letters = [(a+A, A+a) for a, A in letters]

  while this != last:
    last = this

    for aA, Aa in letters:
      this = this.replace(aA, '').replace(Aa, '')

  return this


def evaluate(data):
  print(len(solve(data)))


def test(samples):
  for i, (input, expected) in enumerate(samples.items()):
    actual = solve(input)
    if actual == expected:
      print('solved', i)
    else:
      print(f"problem {i}:")
      print(f"  input: '{input}'")
      print(f"  output: '{actual}")
      print(f"  expect: '{expected}'")

if __name__ == '__main__':
  from lib import timeit, read_input
  
  with timeit('sample'):
    test(samples)
  
  with timeit('data'):
    evaluate(read_input()[0])

