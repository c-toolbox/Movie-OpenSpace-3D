import argparse
import os

import common


desc = 'Compresses frame numbers to close any gaps in frame numbers'

parser = argparse.ArgumentParser(description=desc, epilog='')
parser.add_argument('folder', metavar='<folder>', type=str, help='Location of the frames')
parser.add_argument('--dryrun', dest='dryrun', action='store_true')
parser.set_defaults(dryrun=False)
args = parser.parse_args()

files = common.load_files(args.folder)

sorted_files = files
sorted_files.sort(key=lambda x: x.original_index)

i = 0
for f in files:
  f.new_index = i
  i = i + 1
i = None

for f in files:
  old_filename = f.path
  new_filename = f.filename_structure.format(f.new_index)

  if args.dryrun:
    print('Rename {} -> {}'.format(old_filename, new_filename))
  else:
    os.rename(old_filename, new_filename)
