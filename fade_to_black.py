import argparse
import os
import shutil
from PIL import Image

import common

desc = 'Renames a bunch of files keeping their indices fixed'

parser = argparse.ArgumentParser(description=desc, epilog='')
parser.add_argument('folder', metavar='<folder>', type=str, help='Location of the frames')
parser.add_argument('start', metavar='<start>', type=int, help='Image index to start fade to black')
parser.add_argument('--dryrun', dest='dryrun', action='store_true')
parser.set_defaults(dryrun=False)
args = parser.parse_args()

files = common.load_files(args.folder)

for f in files:
  if f.original_index < args.start:
    continue

  t = (f.original_index - args.start) / (files[-1].original_index - args.start)
  t_inv = 1.0 - t

  if args.dryrun:
    print('Image {} * {}', f.path, t_inv)
  else:
    im = Image.open(f.path)
    out = im.point(lambda i: i * t_inv)
    out.save(f.path)
