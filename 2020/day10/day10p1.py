import pathlib
import collections

def main():
  file = pathlib.Path('./sample1.txt')
  file = pathlib.Path('./sample2.txt')
  file = pathlib.Path('./data.txt')
  
  with file.open('r', encoding='utf8') as infile:
    adapters = [int(l) for l in infile]

  adapters.append(0)  # the wall outlet
  adapters.append(max(adapters) + 3)

  adapters.sort()
  
  previous = adapters[0]
  differences = []
  for joltage in adapters[1:]:
    differences.append(joltage - previous)
    previous = joltage

  counted = collections.Counter(differences)
  print(counted)
  print(counted[1] * counted[3])

if __name__ == '__main__':
  main()

