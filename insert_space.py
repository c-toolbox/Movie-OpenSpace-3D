import argparse
import os
import shutil

import common

desc = 'Extends a single frame in an image sequence by duplicating images'

parser = argparse.ArgumentParser(description=desc, epilog='')
parser.add_argument('folder', metavar='<folder>', type=str, help='Location of the frames')
parser.add_argument('start', metavar='<first frame>', type=int, help='Frame number that should be extended (-1 for insertion before first frame)')
parser.add_argument('duration', metavar='<duration>', type=int, help='Number of frames that should be inserted')
parser.add_argument('--duplicate-last-frame', dest='duplicateframe', action='store_true')
parser.add_argument('--dryrun', dest='dryrun', action='store_true')
parser.set_defaults(duplicateframe=False)
parser.set_defaults(dryrun=False)
args = parser.parse_args()

files = common.load_files(args.folder)

for f in files:
  if f.original_index > args.start:
    f.new_index = f.original_index + args.duration
  else:
    f.new_index = f.original_index

files.reverse()
for f in files:
  if f.original_index != f.new_index:
    old_filename = f.path
    new_filename = f.filename_structure.format(f.new_index)

    if args.dryrun:
      print('Rename {} -> {}'.format(old_filename, new_filename))
    else:
      os.rename(old_filename, new_filename)
files.reverse()

if args.duplicateframe:
  for i in range(args.start, args.start + args.duration):
    source_filename = files[args.start].path
    target_filename = files[args.start].filename_structure.format(i + 1)

    if args.dryrun:
      print('Copy {} -> {}'.format(source_filename, target_filename))
    else:
      shutil.copy2(source_filename, target_filename)
