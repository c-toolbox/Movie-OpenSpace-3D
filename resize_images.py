import argparse
import os
import shutil
from PIL import Image

import common

desc = 'Renames a bunch of files keeping their indices fixed'

parser = argparse.ArgumentParser(description=desc, epilog='')
parser.add_argument('folder', metavar='<folder>', type=str, help='Location of the frames')
parser.add_argument('size', metavar='<size>', type=int, help='New size')
parser.add_argument('--dryrun', dest='dryrun', action='store_true')
parser.set_defaults(dryrun=False)
args = parser.parse_args()

files = common.load_files(args.folder)

for f in files:
  print(f.path)
  im = Image.open(f.path)
  im_resized = im.resize((args.size, args.size))
  im_resized.save(f.path)
