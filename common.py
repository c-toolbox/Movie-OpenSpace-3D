import os
import re

class File:
  path = ''
  filename_structure = ''

  original_index = -1
  new_index = -1
  number_digits = -1

  def __init__(self, file, path):
    base, ext = os.path.splitext(file)

    # (\d+)
    self.path = path + '/' + file
    res = re.findall(r'\d+', base)
    if len(res) != 1:
      raise Exception('Found more than 1 number in the file name. Help')
    self.original_index = int(res[-1])
    self.number_digits = len(res[-1])

    m = re.search(r'\d+', base)
    number_repl = '{{:0{}d}}'.format(self.number_digits)
    self.filename_structure = path + '/' + base[0 : m.start()] + number_repl + base[m.end():-1] + ext

  def __repr__(self):
    return '{{ Path: {}, Original Index: {}, New Index: {}'.format(self.path, self.original_index, self.new_index)

def verify_files(files):
  # Make sure that no indices are used twice
  indices = []
  for f in files:
    if f.original_index in indices:
      raise Exception('Duplicate index found {}'.format(f.original_index))
    indices.append(f.original_index)
  indices = None

  # Make sure that there is only one type of filename structure
  filename_structure = files[0].filename_structure
  for f in files:
    if f.filename_structure != filename_structure:
      raise Exception('Different file structures found: {} / {}'.format(filename_structure, f.filename_structure))
  filename_structure = None

  # Make sure the number of digits are the same for all
  number_digits = files[0].number_digits
  for f in files:
    if f.number_digits != number_digits:
      raise Exception('Different number of digits found: {} / {}'.format(number_digits, f.number_digits))
  number_digits = None

  # Sanity check for filename structure
  for f in files:
    new_file_path = f.filename_structure.format(f.original_index)
    if f.path != new_file_path:
      raise Exception('Somethings up with the path: {} / {}'.format(f.path, new_file_path))

def load_files(path):
  files = [File(f, path) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
  verify_files(files)
  return files
