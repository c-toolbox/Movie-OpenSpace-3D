import argparse
import os
import shutil
from PIL import Image

import common

desc = 'Applies a fading-from-black animation to a subset of images in an image sequence'

parser = argparse.ArgumentParser(description=desc, epilog='')
parser.add_argument('folder', metavar='<folder>', type=str, help='Location of the frames')
parser.add_argument('start', metavar='<start>', type=int, help='Image index to start fade to black')
parser.add_argument('end', metavar='<end>', type=int, help='Image index to end fade to black (-1 for end)')
parser.add_argument('--dryrun', dest='dryrun', action='store_true')
parser.set_defaults(dryrun=False)
args = parser.parse_args()

files = common.load_files(args.folder)

for f in files:
  if f.original_index < args.start or f.original_index > args.end:
    continue

  t = (f.original_index - files[args.start].original_index) / (files[args.end].original_index - files[args.start].original_index)
  t_inv = t

  print('Image {} * {}'.format(f.path, t_inv))
  if not args.dryrun:
    im = Image.open(f.path)
    out = im.point(lambda i: i * t_inv)
    out.save(f.path)
