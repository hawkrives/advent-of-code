from os.path import realpath, join, dirname, basename
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager
import __main__

def read_input():
  file = realpath(__main__.__file__)
  filename = basename(file).split('.')[0]
  root = join(dirname(file), 'input')
  try:
    return readlines(join(root, filename))
  except FileNotFoundError:
    try:
      return readlines(join(root, filename.split('_')[0]))
    except FileNotFoundError as ex:
      raise ex

def readlines(filepath):
  with open(filepath, 'r', encoding='utf-8') as infile:
      return [l for l in infile.readlines() if l.strip()]

@contextmanager
def timeit(label='duration'):
  start = datetime.now()
  yield 
  end = datetime.now()
  print(f'{label}:', end - start, 'seconds')

