"""
Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

For example:

For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
For a mass of 1969, the fuel required is 654.
For a mass of 100756, the fuel required is 33583.
"""

def fuel(mass):
  return (mass // 3) - 2


def tests():
  assert fuel(12) == 2
  assert fuel(14) == 2
  assert fuel(1969) == 654
  assert fuel(100756) == 33_583


inputs = '''
83285
96868
121640
51455
128067
128390
141809
52325
68310
140707
124520
149678
87961
52040
133133
52203
117483
85643
84414
86558
65402
122692
88565
61895
126271
128802
140363
109764
53600
114391
98973
124467
99574
69140
144856
56809
149944
138738
128823
82776
77557
51994
74322
64716
114506
124074
73096
97066
96731
149307
135626
121413
69575
98581
50570
60754
94843
72165
146504
53290
63491
50936
79644
119081
70218
85849
133228
114550
131943
67288
68499
80512
148872
99264
119723
68295
90348
146534
52661
99146
95993
130363
78956
126736
82065
77227
129950
97946
132345
107137
79623
148477
88928
118911
75277
97162
80664
149742
88983
74518
'''

inputs = [int(l) for l in inputs.splitlines() if l]

def part1():
  return sum(fuel(m) for m in inputs)


"""
So, for each module mass, calculate its fuel and add it to the total. Then, treat the fuel amount you just calculated as the input mass and repeat the process, continuing until a fuel requirement is zero or negative. For example:

A module of mass 14 requires 2 fuel. This fuel requires no further fuel (2 divided by 3 and rounded down is 0, which would call for a negative fuel), so the total fuel required is still just 2.

At first, a module of mass 1969 requires 654 fuel. Then, this fuel requires 216 more fuel (654 / 3 - 2). 216 then requires 70 more fuel, which requires 21 fuel, which requires 5 fuel, which requires no further fuel. So, the total fuel required for a module of mass 1969 is 654 + 216 + 70 + 21 + 5 = 966.

The fuel required by a module of mass 100756 and its fuel is: 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.
"""
def rfuel(mass):
  amt = fuel(mass)
  if amt <= 0:
    return 0
  return amt + rfuel(amt)


def ifuel(starting_mass):
  fuel_needed = fuel(starting_mass)
  
  more_fuel_needed_for_fuel = fuel(fuel_needed)
  sum_fuel_needed_for_fuel = fuel_needed
  
  while more_fuel_needed_for_fuel > 0:
    sum_fuel_needed_for_fuel += more_fuel_needed_for_fuel
    more_fuel_needed_for_fuel = fuel(more_fuel_needed_for_fuel)
  
  return sum_fuel_needed_for_fuel
    

def more():
  assert rfuel(14) == 2
  assert rfuel(1969) == 966
  assert rfuel(100756) == 50_346

  assert ifuel(14) == 2
  assert ifuel(1969) == 966
  assert ifuel(100756) == 50_346


def part2():
  return sum(rfuel(m) for m in inputs)


def part2_take2():
  return sum(ifuel(m) for m in inputs)


def benchmark():
  import timeit
  n = 10_000
  p2  = timeit.timeit('part2()', number=n, globals=globals())
  print('part2', p2)
  p22 = timeit.timeit('part2_take2()', number=n, globals=globals())
  print('part2v2', p22)
  

if __name__ == '__main__':
  tests()
  more()
  #print(part1())
  print(part2())
  print(part2_take2())
  benchmark()
