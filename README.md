Bitmap Converter for uGui
---------------------

A tool for converting bitmaps to C arrays for uGui ( )

Based on https://github.com/DanNixon/GLCD-BitmapConverter

Usage
-----

Use ```python bmp2ugui.py -h``` to see a list of arguments.

Requires PIL package


Example
-------

python ./bmp2ugui.py -f test.bmp -o test_img.c -a test_img

Notes
-----

Still early stage of development. Works, but not much of e.g. error checks and protections.


