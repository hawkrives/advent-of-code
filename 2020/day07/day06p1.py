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


def build_paths(lookup, root, target, path=()):
  #print(root)
  path = (*path, root)

  if not lookup[root]:
    # print('case 1')
    return path

  for can_contain in lookup[root]:
    if can_contain == target:
      #print('case 2')
      #yield (*path, target)
      yield path

    yield from build_paths(lookup, can_contain, target, path=path)


bags = set()
for root_color in parsed:
  for path in build_paths(parsed, root_color, 'shiny gold'):
    #print(path)
    bags.update(path)


print(len(bags))
