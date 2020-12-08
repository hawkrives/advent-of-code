import itertools

with open('./day01.txt', 'r', encoding='utf-8') as infile:
  data = [int(point) for point in infile.read().split() if point]

for a, b, c in itertools.combinations(data, 3):
  if a + b + c == 2020:
    print(a * b * c)
