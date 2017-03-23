# PhotoSort

This is a small utility which will allow you to sort photos in order of aesthetic appeal. To get started with the program, simply clone it and run mergesort_photos.py from the terminal. The number at the top of the window will let you know how many pictures remain to be sorted before the results will be generated.

Next steps include implementing a [binary insertion sort](https://en.wikipedia.org/wiki/Insertion_sort) which will allow us to insert images into an already sorted list.

The following line will open up the images in order if feh is installed
```
for i in $(cat ranked.txt | sed 's/^.* //g' | sed '3d'); do echo $i; done | feh
```
