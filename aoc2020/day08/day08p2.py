import pathlib
import enum
import collections

class Instruction:
  def __init__(self, op, arg):
    self.op = op
    self.arg = arg
  
  def __str__(self):
    return f'{self.op.value} {self.arg:5.0f}'
  
  def __repr__(self):
    return str(self)


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


class InfiniteLoopError(BaseException):
  def __init__(self, *, acc):
    super()
    self.acc = acc
    

class OutOfBoundsError(BaseException):
  def __init__(self, *, acc):
    super()
    self.acc = acc


def interpret(instructions):
  counter = collections.Counter()
  order = collections.defaultdict(list)

  try:
    ex_index = 0
    index = 0
    accumulator = 0
    while True:
      ex_index += 1
      
      try:
        instruction = instructions[index]
      except IndexError:
        raise OutOfBoundsError(acc=accumulator)
      #print(instruction)
      counter[id(instruction)] += 1

      if counter[id(instruction)] > 1:
        raise InfiniteLoopError(acc=accumulator)
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
      
      order[id(instruction)].append((ex_index, accumulator))
  finally:
    if False:
      for instruction in instructions:
        print(instruction, '|', order[id(instruction)])
    
  return accumulator


def mutate(instructions):
  nops = [i for i, instr in enumerate(instructions) if instr.op is Operation.NOP]
  jmps = [i for i, instr in enumerate(instructions) if instr.op is Operation.JMP]
  
  #print(instructions)
  yield instructions
  
  for index in nops:
    orig = instructions[index]
    instructions[index] = Instruction(Operation.JMP, orig.arg)
    yield instructions
    instructions[index] = orig
  
  for index in jmps:
    orig = instructions[index]
    instructions[index] = Instruction(Operation.NOP, orig.arg)
    yield instructions
    instructions[index] = orig
  
  print('exhausted')


def main():
  instructions = parse()
  #for i in instructions:
  #  print(i)
  for i, inst_set in enumerate(mutate(instructions)):
    try:
      acc = interpret(instructions)
      print(acc)
    except InfiniteLoopError as ex:
      print('inf', i)
      continue
    except OutOfBoundsError as ex:
      print('oob', i)
      print(ex.acc)
      break

if __name__ == '__main__':
  main()

