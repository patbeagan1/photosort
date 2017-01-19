import argparse
import glob
import json
import os
import sys


# 3rd party
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import exifread


remaining = 0


class Display(object):
    """
    Given two photos, displays them with Matplotlib and provides a graphical
    means of choosing the better photo.

    Click on the select button to pick the better photo.

    ~OR~

    Press the left or right arrow key to pick the better photo.

    """

    def __init__(self, f1, f2, title=None, figsize=None):
        self._choice = None

        if figsize is None:
            figsize = [20, 12]

        fig = plt.figure(figsize=figsize)

        h = 10

        ax11 = plt.subplot2grid((h, 2), (0, 0), rowspan=h - 1)
        ax12 = plt.subplot2grid((h, 2), (0, 1), rowspan=h - 1)

        ax21 = plt.subplot2grid((h, 6), (h - 1, 1))
        ax22 = plt.subplot2grid((h, 6), (h - 1, 4))

        kwargs = dict(s='Select', ha='center', va='center', fontsize=20)

        ax21.text(0.5, 0.5, **kwargs)
        ax22.text(0.5, 0.5, **kwargs)

        self._fig = fig
        self._ax_select_left = ax21
        self._ax_select_right = ax22

        fig.subplots_adjust(
            left=0.02,
            bottom=0.02,
            right=0.98,
            top=0.98,
            wspace=0.05,
            hspace=0,
        )

        ax11.imshow(f1.data())
        ax12.imshow(f2.data())

        for ax in [ax11, ax12, ax21, ax22]:
            ax.set_xticklabels([])
            ax.set_yticklabels([])

            ax.set_xticks([])
            ax.set_yticks([])

        self._attach_callbacks()

        if title:
            fig.suptitle(title, fontsize=20)

        plt.show()

    def _on_click(self, event):

        if event.inaxes == self._ax_select_left:
            self._choice = Photo.LEFT
            plt.close(self._fig)

        elif event.inaxes == self._ax_select_right:
            self._choice = Photo.RIGHT
            plt.close(self._fig)

    def _on_key_press(self, event):

        if event.key == 'left':
            self._choice = Photo.LEFT
            plt.close(self._fig)

        elif event.key == 'right':
            self._choice = Photo.RIGHT
            plt.close(self._fig)

    def _attach_callbacks(self):
        self._fig.canvas.mpl_connect('button_press_event', self._on_click)
        self._fig.canvas.mpl_connect('key_press_event', self._on_key_press)


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