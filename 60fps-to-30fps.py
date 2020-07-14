import argparse
import os
import shutil

import common

desc = 'Renames a bunch of files keeping their indices fixed'

parser = argparse.ArgumentParser(description=desc, epilog='')
parser.add_argument('folder', metavar='<folder>', type=str, help='Location of the frames')
parser.add_argument('--dryrun', dest='dryrun', action='store_true')
parser.set_defaults(dryrun=False)
args = parser.parse_args()

files = common.load_files(args.folder)

for f in files:
  if f.original_index % 2 == 0:
    if args.dryrun:
      print('Remove {}'.format(f.path))
    else:
      os.remove(f.path)
