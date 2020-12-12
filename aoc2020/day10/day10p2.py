import pathlib
import collections
import itertools

def build(adapters):
  seq = []
  
  for a in adapters:
    if 0 < (a - seq[-1]) <= 3:
      seq.append(a)

def build2(adapters):
  for i, adapter in enumerate(adapters):
    print(f'#{i},', adapter)

    remaining = [
      a for a in adapters[i:] 
      if 0 < (a - adapter) <= 3
    ]
    print(remaining)
    
    for n in remaining:
      yield n

def main():
  file = pathlib.Path('./sample1.txt')
  #file = pathlib.Path('./sample2.txt')
  #file = pathlib.Path('./data.txt')
  
  with file.open('r', encoding='utf8') as infile:
    adapters = [int(l) for l in infile]
  
  builtin = max(adapters) + 3
  
  adapters.append(0)
  adapters.append(builtin)
  
  adapters.sort()
  
  print(list(build2(adapters)))
  
  return
  
  print(builtin)
  min_length = (builtin // 3) - 2
  
  # rules:
  # must start with 0
  # must end with $builtin$
  # the gap between any two items must be 1, 2, or 3
  
  # idea: build the combinations ourselves, so we can terminate early?
  
  arrangements = []
  count = 0
  
  for n in range(min_length, len(adapters) + 1):
  #for n in [15]:
    for i, combo in enumerate(itertools.combinations(adapters, n)):
      # if i % 100000 == 0:
      print(f'{n} - {i:,} - {count}')
      
      if combo[0] != 0 or combo[n-1] != builtin:
        continue

      if is_valid(combo):
        count += 1
        #arrangements.append(combo)

  print(count)
  #print(len(arrangements))
  
  #arrangements.sort(key=lambda l: (len(l), l), reverse=True)
  #arrangements.sort()
  
  #for arr in arrangements:
    #print(' '.join(str(s) if s not in (0, max(adapters)+3) else f'({s})' for s in arr))


def is_valid(adapters):
  previous = adapters[0]
  differences = []
  for joltage in adapters[1:]:
    differences.append(joltage - previous)
    previous = joltage
  
  return all(n in (1,2,3) for n in differences)


if __name__ == '__main__':
  main()

