import argparse
import os
import shutil

import common

desc = 'Duplicates a specific frame a number of times; the available space in the image sequence has to be available'

parser = argparse.ArgumentParser(description=desc, epilog='')
parser.add_argument('folder', metavar='<folder>', type=str, help='Location of the frames')
parser.add_argument('frame', metavar='<frame>', type=int, help='Number of the frame to duplicate')
parser.add_argument('count', metavar='<count>', type=int, help='Number of times the frame should be copied')
parser.add_argument('--dryrun', dest='dryrun', action='store_true')
parser.set_defaults(dryrun=False)
args = parser.parse_args()

files = common.load_files(args.folder)

start = args.frame
end = args.frame + args.count

# First check if the space is available
for f in files:
    if f.original_index > start and f.original_index <= end:
        raise Exception('Image index {} already in use; file would be overwritten'.format(f.original_index))

# Now we now that we can safely copy the files
for f in files:
    if f.original_index != start:
        continue

    for i in range(start, end):
        old_filename = f.path
        new_filename = f.filename_structure.format(i + 1)
        shutil.copyfile(old_filename, new_filename)
