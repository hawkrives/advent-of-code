import pathlib
import enum
import collections

Instruction = collections.namedtuple('Instruction', ['op', 'arg'])

Instruction.__str__ = lambda self: f'{self.op.value} {self.arg:5.0f}'

class Operation(enum.Enum):
  ACC = 'acc'
  JMP = 'jmp'
  NOP = 'nop'


def parse():
  sample = pathlib.Path('./sample.txt')
  sample = pathlib.Path('./data.txt')
  
  with sample.open('r', encoding='utf-8') as infile:
      data = (l.strip() for l in infile.readlines())
      data = [l for l in data if l]
  
  separated = (line.split() for line in data)
  
  instructions = [
    Instruction(Operation(op), int(arg))
    for op, arg in separated
  ]
  
  return instructions


def interpret(instructions):
  counter = collections.Counter()
  order = collections.defaultdict(list)

  ex_index = 0
  index = 0
  accumulator = 0
  while True:
    ex_index += 1
    instruction = instructions[index]
    #print(instruction)
    counter[id(instruction)] += 1
    order[id(instruction)].append(ex_index)
    
    if counter[id(instruction)] > 1:
      print(accumulator)
      break

    if instruction.op is Operation.ACC:
      accumulator += instruction.arg
      index += 1
    elif instruction.op is Operation.JMP:
      index += instruction.arg
    elif instruction.op is Operation.NOP:
      index += 1
      pass
    else:
      raise TypeError(f'unknown operation {instruction.op}')
  
  for instruction in instructions:
    print(instruction, '|', order[id(instruction)])
    
  print(accumulator)


def main():
  instructions = parse()
  #for i in instructions:
  #  print(i)
  interpret(instructions)


if __name__ == '__main__':
  main()

