#!/usr/bin/env python
# -*- coding: utf-8 -*-

import png
import sys
import numpy as np

"""
AUTHOR Krusty/Benediction
28 april 2011

Return the palette as gate array data
"""
def extract_fields(intcpcolor):
    """Return a tuple containing the values"""

    return \
    (
    (intcpcolor & 0xff0000) >> 16,
    (intcpcolor & 0x00ff00) >> 8,
    (intcpcolor & 0x0000ff) )


def get_closer_color( color):
    """Returns the closer gate array color from the png color"""


    distances = [ \
                abs(color[0] - cpccolor[1][0])**2+
                abs(color[1] - cpccolor[1][1])**2+
                abs(color[2] - cpccolor[1][2])**2 \
                    for cpccolor in CPC_COLORS]
    pos = np.argmin(distances)



    return CPC_COLORS[pos][0]


#List of cpc colors
CPC_COLORS = (
 (0x54, extract_fields(0x000201)),
 (0x44, extract_fields(0x00026B)),
 (0x55, extract_fields(0x0c02f4)),
 (0x5c, extract_fields(0x6c0201)),
 (0x58, extract_fields(0x690268)),
 (0x5d, extract_fields(0x6c02f2)),
 (0x4c, extract_fields(0xf30506)),
 (0x45, extract_fields(0xf00268)),
 (0x4d, extract_fields(0xf302f4)),
 (0x56, extract_fields(0x027801)),
 (0x46, extract_fields(0x007868)),
 (0x57, extract_fields(0x0c7bf4)),
 (0x5e, extract_fields(0x6e7b01)),
 (0x40, extract_fields(0x6e7d6b)),
 (0x5f, extract_fields(0x6e7bf6)),
 (0x4e, extract_fields(0xf37d0d)),
 (0x47, extract_fields(0xf37d6b)),
 (0x4f, extract_fields(0xfa80f9)),
 (0x52, extract_fields(0x02f001)),
 (0x42, extract_fields(0x00f36b)),
 (0x53, extract_fields(0x0ff3f2)),
 (0x5a, extract_fields(0x71f504)),
 (0x59, extract_fields(0x71f36b)),
 (0x5b, extract_fields(0x71f3f4)),
 (0x4a, extract_fields(0xf3f30d)),
 (0x43, extract_fields(0xf3f36d)),
 (0x4b, extract_fields(0xfff3f9)) )



def extract_png_palette(fname, nb_col, same_order=False):
    """Return the color tuples"""
    # Read the file
    reader = png.Reader(fname)
    reader.preamble()

    # Get the palette in storage order
    if same_order:
        return reader.palette()[:nb_col]

    # Return the palette in order of pixel appearance
    (width, height, pixels, metadata)  = reader.asRGB8()

    readed_pixels = []
    #for row in pixels:
    for row in reader.iterboxed(pixels):
        #reader.iterboxed(pixels):
        for i in range(len(row)/3):
            pixel = (row[i*3], row[i*3+1], row[i*3+2])
            if pixel not in readed_pixels:
                readed_pixels.append(pixel)


    return readed_pixels


if __name__ == "__main__":
    fname = sys.argv[1]
    nb_col = 16

    pngpalette = extract_png_palette(fname, nb_col, True)

    print '; Color extraction'
    print '; Krusty/Benediction'
    for ink, color in enumerate(pngpalette):
        print '\tdb 0x%x\t; ink %d' % (get_closer_color(color), ink)
