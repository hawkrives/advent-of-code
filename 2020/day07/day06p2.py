import collections

with open('./day06.txt', 'r', encoding='utf-8') as infile:
  data = [l.strip() for l in infile.readlines()]


parsed = {}
for l in data:
  key, values_text = l.split(' contain ')
  key = key[:-5]

  values = {}
  for value in values_text.split(', '):
    value = value.rstrip('.')
    
    if value == 'no other bags':
      continue
    
    count, accent, color, _ = value.split()
    values[f'{accent} {color}'] = int(count)

  parsed[key] = values


debug = False
def required_contents(lookup, root, level=0):
  if debug: print('-' * level, 'start:', root)

  c = collections.Counter()

  if not lookup[root]:
    if debug: print('-' * level, 'empty')
    return c

  for can_contain, count in lookup[root].items():
    if debug: print('-' * level, 'needs', count, repr(can_contain))
    nested = required_contents(lookup, can_contain, level + 1)
    if debug: print('-' * level, '^', nested)
    c[can_contain] = count + (sum(nested.values()) * count)

  if debug: print('-' * level, '<', c)
  return c


if debug:
  for key, items in parsed.items():
    print(key, '=', items)
  
  print()

c = required_contents(parsed, 'shiny gold')
print(sum(c.values()))

