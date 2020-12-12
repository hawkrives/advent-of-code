import pathlib
import collections
import itertools
import sqlite3

def initdb(adapters):
  conn = sqlite3.connect(':memory:')
  
  with conn:
    curs = conn.cursor()
    
    curs.execute('''
      create table adapters (
        joules int not null primary key
      )
    ''')
    
    for joules in adapters:
      curs.execute('''
        insert into adapters (joules)
        values (?)
      ''', (joules,))
  
  return conn


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
  
  conn = initdb(adapters)
  
  with conn:
    curs = conn.cursor()
    curs.execute('''
    
    select 
      a.joules,
      a.joules - a1.joules as m1,
      a.joules - a2.joules as m2,
      a.joules - a3.joules as m3
    from adapters a
    left join adapters a1 on a1.rowid = a.rowid - 1
    left join adapters a2 on a2.rowid = a.rowid - 2
    left join adapters a3 on a3.rowid = a.rowid - 3
    where a1.joules in (1,2,3)
    or a2.joules in (1,2,3)
    or a3.joules in (1,2,3)
    ''')
    for row in curs:
      print(repr(row))
  
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
