import argparse
import os
import shutil

import common

desc = 'Renames a bunch of files keeping their indices fixed'

parser = argparse.ArgumentParser(description=desc, epilog='')
parser.add_argument('folder', metavar='<folder>', type=str, help='Location of the frames')
parser.add_argument('newstructure', metavar='<newstructure>', type=str, help='New filename structure')
parser.add_argument('--dryrun', dest='dryrun', action='store_true')
parser.set_defaults(dryrun=False)
args = parser.parse_args()

files = common.load_files(args.folder)

for f in files:
  old_filename = f.path
  new_filename = (args.folder + '/' + args.newstructure).format(f.original_index)

  if args.dryrun:
    print('Rename {} -> {}'.format(old_filename, new_filename))
  else:
    os.rename(old_filename, new_filename)
