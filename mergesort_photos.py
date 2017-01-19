#!/usr/bin/env python

from photo import Photo
from display import Display
import argparse
import glob
import json
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import exifread



_photos = []
_photo_instances = {}


def add_photo(filename_or_photo):

    if isinstance(filename_or_photo, str):

        filename = filename_or_photo

        if filename not in _photo_instances:
            _photo_instances[filename] = Photo(filename)
            _photos.append(filename)

    elif isinstance(filename_or_photo, Photo):

        photo = filename_or_photo

        if photo.filename() not in _photo_instances:
            _photo_instances[photo.filename()] = photo
            _photos.append(photo.filename())


def rank_photos(alist):
    print("Splitting ", alist)
    if len(alist) > 1:
        mid = len(alist) // 2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        rank_photos(lefthalf)
        rank_photos(righthalf)

        i = 0
        j = 0
        k = 0
        while i < len(lefthalf) and j < len(righthalf):

            if compare_photo(_photo_instances[lefthalf[i]], _photo_instances[righthalf[j]]):
                alist[k] = lefthalf[i]
                i = i + 1
            else:
                alist[k] = righthalf[j]
                j = j + 1
            k = k + 1

        while i < len(lefthalf):
            alist[k] = lefthalf[i]
            i = i + 1
            k = k + 1

        while j < len(righthalf):
            alist[k] = righthalf[j]
            j = j + 1
            k = k + 1
    print("Merging ", alist)

# alist = [54, 26, 93, 17, 77, 31, 44, 55, 20]
# mergeSort(alist)
# print(alist)


def compare_photo(photo_a, photo_b):
    # match_up = j / 2
    global remaining
    title = remaining
    remaining -= 1
    # title = 'Round %d / %d, Match Up %d / %d' % (
    #     i + 1, n_iterations,
    #     match_up + 1,
    #     n_matchups)
    if not isinstance(photo_a, Photo):
        return False
    if not isinstance(photo_b, Photo):
        return True
    if photo_a is photo_b:
        return True

    d = Display(photo_a, photo_b, title)

    if d._choice == Photo.LEFT:
        return False
    elif d._choice == Photo.RIGHT:
        return True
    else:
        raise RuntimeError("oops, found a bug!")


def main():

    description = """\
Uses the Elo ranking algorithm to sort your images by rank.  The program globs
for .jpg images to present to you in random order, then you select the better
photo.  After n-rounds, the results are reported.

Click on the "Select" button or press the LEFT or RIGHT arrow to pick the
better photo.

"""
    parser = argparse.ArgumentParser(description=description)

    # parser.add_argument(
    #     "-r",
    #     "--n-rounds",
    #     type=int,
    #     default=3,
    #     help="Specifies the number of rounds to pass through the photo set (3)"
    # )

    # parser.add_argument(
    #     "-f",
    #     "--figsize",
    #     nargs=2,
    #     type=int,
    #     default=[20, 12],
    #     help="Specifies width and height of the Matplotlib figsize (20, 12)"
    # )

    parser.add_argument(
        "photo_dir",
        help="The photo directory to scan for .jpg images"
    )

    args = parser.parse_args()

    assert os.path.isdir(args.photo_dir)

    os.chdir(args.photo_dir)

    ranking_table_json = 'ranking_table.json'
    ranked_txt = 'ranked.txt'

    # Create the ranking table and add photos to it.
    #--------------------------------------------------------------------------
    # Read in table .json if present

    sys.stdout.write("Reading in photos and downsampling ...")
    sys.stdout.flush()

    if os.path.isfile(ranking_table_json):
        with open(ranking_table_json, 'r') as fd:
            d = json.load(fd)

        # read photos and add to table

        for p in d['photos']:

            photo = Photo(**p)

            add_photo(photo)

    #--------------------------------------------------------------------------
    # glob for files, to include newly added files
    filelist = []
    validImages = ['jpg', 'png', 'jpeg', 'gif']
    for i in validImages:
        filelist += glob.glob('*.' + i)
    print filelist
    for f in filelist:
        add_photo(f)

    global remaining
    remaining = int(math.floor(len(filelist) * math.log(len(filelist), 2)))
    print(remaining)
    print(" done!")
    #--------------------------------------------------------------------------
    # Rank the photos!

    rank_photos(_photos)

    #--------------------------------------------------------------------------
    # save the table

    # with open(ranking_table_json, 'w') as fd:

    #     d = table.to_dict()

    #     jstr = json.dumps(d, indent=4, separators=(',', ' : '))

    #     fd.write(jstr)

    #--------------------------------------------------------------------------
    # dump ranked list to disk

    with open(ranked_txt, 'w') as fd:

        ranked_list = _photos

        heading_fmt = "%4d    %s\n"

        heading = "\n\nRank    Filename\n"

        fd.write(heading)

        for i, photo in enumerate(ranked_list):

            line = heading_fmt % (
                i + 1,
                photo)

            fd.write(line)

    #--------------------------------------------------------------------------
    # dump ranked list to screen

    print "Final Ranking:"

    with open(ranked_txt, 'r') as fd:
        text = fd.read()

    print text


if __name__ == "__main__":
    main()
