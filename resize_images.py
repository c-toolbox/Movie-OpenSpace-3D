import argparse
import os
import shutil
from PIL import Image

import common

desc = 'Resizes all images in a folder to a new square size, leaving the originals intact'

parser = argparse.ArgumentParser(description=desc, epilog='')
parser.add_argument('folder', metavar='<folder>', type=str, help='Location of the frames')
parser.add_argument('target', metavar='<target>', type=str, help='Target location of the frames, can be the same as "folder"')
parser.add_argument('size', metavar='<size>', type=int, help='New size')
parser.add_argument('--dryrun', dest='dryrun', action='store_true')
parser.set_defaults(dryrun=False)
args = parser.parse_args()

files = common.load_files(args.folder)

for f in files:
  src = f.path
  dest = args.target + '/' + os.path.basename(f.path)
  print("Resize {} -> {} ({})".format(src, dest, args.size))
  if not args.dryrun:
    im = Image.open(src)
    im_resized = im.resize((args.size, args.size))
    im_resized.save(dest)
