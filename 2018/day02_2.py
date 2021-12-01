'''
Confident that your list of box IDs is complete, you're ready to find the boxes full of prototype fabric.

The boxes will have IDs which differ by exactly one character at the same position in both strings. For example, given the following box IDs:

abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz

The IDs abcde and axcye are close, but they differ by two characters (the second and fourth). However, the IDs fghij and fguij differ by exactly one character, the third (h and u). Those must be the correct boxes.

What letters are common between the two correct box IDs? (In the example above, this is found by removing the differing character from either ID, producing fgij.)
'''

test_inputs = '''
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
'''
test_inputs = [s for s in test_inputs.splitlines() if s]

from lib import read_input
inputs = read_input()

from itertools import zip_longest as zip

def compare(v1, v2):
  diff = 0
  common = ''
  #print()
  #print(v1, v2)
  for c1, c2 in zip(v1, v2):
    #print(c1, c2)
    if c1 != c2:
      diff += 1
    else:
      common += c1
    if diff > 1:
      return
  
  return common


def solve(values):
  for v1 in values:
    for v2 in values:
      if v1 == v2:
        continue
      
      common = compare(v1, v2)
      if not common:
        continue
      
      print(common)
      return


solve(inputs)
