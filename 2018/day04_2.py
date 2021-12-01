'''
--- Part Two ---

Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

In the example above, Guard #99 spent minute 45 asleep more than any other guard or minute - three times in total. (In all other cases, any guard spent any minute asleep at most twice.)

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 99 * 45 = 4455.)
'''

import collections
import itertools
import re

sample = '''
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
'''

Entry = collections.namedtuple('Entry', 'year,month,day,hour,minute,action,id')

def parse(line):
  regex = r'\[(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) (?P<hour>\d{2}):(?P<minute>\d{2})\] (?P<action>(Guard #(?P<id>\d+)|falls|wakes))'
  
  result = re.match(regex, line)
  #print(len(line))
  
  if not result:
    return None
    
  matches = result.groupdict()
  for key in matches.keys():
    if key == 'action':
      continue
    if key == 'id' and matches[key] is None:
      continue
    matches[key] = int(matches[key])
  
  return Entry(**matches)


def to_sortable(e: Entry):
  return f'{e.year:02}.{e.month:02}.{e.day:02}.{e.hour:02}.{e.minute:02}'


def group(entries):
  ordered = sorted(entries, key=to_sortable)
  id = None
  collection = collections.defaultdict(list)
  for e in ordered:
    if e.id is not None:
      id = e.id
    collection[id].append(e)
  return collection


def sleep_sum(entries):
  start = None
  end = None
  sum = 0
  for e in entries:
    if e.action == 'falls':
      start = e.minute
    elif e.action == 'wakes':
      end = e.minute
      sum += end - start
      start = None
      end = None
  return sum


def most_asleep(grouped):
  ordered = {id: sleep_sum(g) for id, g in grouped.items()}
  return max(ordered.items(), key=lambda args: args[1])


def most_commonly_asleep_at(entries):
  start = None
  end = None
  c = collections.Counter()
  for e in entries:
    if e.action == 'falls':
      start = e.minute
    elif e.action == 'wakes':
      end = e.minute
      c.update(list(range(start, end)))
      start = None
      end = None
  
  if len(c) is 0:
    return (-1, 0)

  return c.most_common(1)[0]


def the_sleepiest_at(grouped):
  mapped = {id: most_commonly_asleep_at(entries) for id, entries in grouped.items()}
  #print(mapped)
  return max(mapped.items(), key=lambda args: args[1][1])


def main(sample):
  sample = [parse(l) for l in sample]
  #print(sample)
  g = group(sample)
  id, (at, count) = the_sleepiest_at(g)
  print('id', id, 'at', at)
  print('result', id * at)


if __name__ == '__main__':
  from lib import read_input, timeit
  with timeit('sample'):
    main([l for l in sample.splitlines() if l.strip()])
  with timeit('real'):
    data = read_input()
    main(data)

