from itertools import islice, tee, combinations

def window(iterable, size):
  '''https://stackoverflow.com/a/54110047/2347774'''
  iterators = tee(iterable, size) 
  iterators = [islice(iterator, i, None) for i, iterator in enumerate(iterators)]  
  yield from zip(*iterators)

#print(list(window(range(26), 25)))
# [(0, 1, 2), (1, 2, 3), (2, 3, 4)]

sample = [7, 16, 23, 3, 17, 22, 14, 1, 8, 11, 15, 0, 12, 19, 10, 24, 9, 2, 5, 21, 4, 6, 20, 18, 13, 45]

def is_empty(it):
  for _ in it:
    return False
  return True

def find_invalid(data, size=25):
  for w in window(data, size+1):
    n = w[size]

    candidates = (
      (a,b) 
      for a, b in combinations(w[0:size], 2)
      if a + b == n
    )

    if is_empty(candidates):
      return n

    #print(n, list(c))

def main(data, size=25):
  invalid = find_invalid(data, size=size)
  
  for n in range(2, len(data) + 1):
    for w in window(data, n):
      w = list(w)
      if sum(w) == invalid:
        return min(w) + max(w)

#main(sample, 25)

sample5 = [
  35,
20,
15,
25,
47,
40,
62,
55,
65,
95,
102,
117,
150,
182,
127,
219,
299,
277,
309,
576,
]

#print(main(sample5, 5))


with open('./data.txt', 'r') as infile:
  data = [int(line) for line in infile]
  #print(data)
  
print(main(data, 25))

