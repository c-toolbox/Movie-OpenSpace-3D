import argparse
import os
import shutil
from PIL import Image

import common

desc = 'Composites overlays onto image sequences using a grey-scale image mask'

parser = argparse.ArgumentParser(description=desc, epilog='')
parser.add_argument('folder', metavar='<folder>', type=str, help='Location of the frames')
parser.add_argument('maskfolder', metavar='<maskfolder>', type=str, help='Folder with mask images. For each image, a black pixel represents the original pixel value, a white pixel represents the overlay, and gray pixels are interpolated')
parser.add_argument('overlayfolder', metavar='<overlayfolder', type=str, help='Folder with overlay images')
parser.add_argument('--dryrun', dest='dryrun', action='store_true')
parser.set_defaults(dryrun=False)
args = parser.parse_args()

files = common.load_files(args.folder)
masks = common.load_files(args.maskfolder)
overlays = common.load_files(args.overlayfolder)

def fileWithIndex(files, idx):
  for f in files:
    if f.original_index == idx:
      return f
  return None

# Check that there are overlays for all masks and vice versa
for f in files:
  mask = fileWithIndex(masks, f.original_index)
  overlay = fileWithIndex(overlays, f.original_index)

  if mask == None and overlay == None:
    continue
  if mask != None and overlay != None:
    continue

  raise Exception('Mismatch detected, one of mask ({}) or overlay ({}) does not exit'.format(mask, overlay))


for f in files:
  print('File {}'.format(f.path))

  mask = fileWithIndex(masks, f.original_index)
  overlay = fileWithIndex(overlays, f.original_index)

  if mask == None and overlay == None:
    continue

  if not args.dryrun:
    im = Image.open(f.path)
    im_mask = Image.open(mask.path).convert("L")
    im_overlay = Image.open(overlay.path)

    out = Image.composite(im_overlay, im, im_mask)
    out.save(f.path)
