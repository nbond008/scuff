from PIL import Image, ImageStat
from process.bbox import BoundingBox
import matplotlib.pyplot as pp
import numpy as np
from sys import exit, argv
from array import array
import math
from time import clock

def list_to_arr(l):
    return np.flipud(np.array(l).transpose())

def image_subtract(before, after, grain, showing = False):
    outputs = dict()

    start = float(clock())

    # baseline = ImageStat.Stat(before).rms

    # images = [before, after]
    # data   = [[], []]

    # leftover_x = -1
    # leftover_y = -1

    grain = int(min(grain, min(after.width, after.height) / 2.5))

    # if showing:
    #     print 'actual grain = %d' % grain
    #     print baseline

    # outputs['grain'] = grain

    try:
        ith = int(bool(after.width % grain))
        jth = int(bool(after.height % grain))
    except ZeroDivisionError:
        print 'grain size must be a positive integer.'
        return  None

    jth = 0
    ith = 0

    grid = [[None for j in range(after.height / grain + jth)] for i in range(after.width / grain + ith)]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = BoundingBox(
                grain * i,
                grain * j,
                min(grain * (i + 1), after.width),
                min(grain * (j + 1), after.height)
            )

            # if leftover_x == -1:
            #     leftover_x = grain * (i + 1) - after.width
            #
            # if leftover_y == -1:
            #     leftover_y = grain * (i + 1) - after.height

    rd = [[0.0 for j in range(len(grid[0]))] for i in range(len(grid))]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            mask = Image.new('L', after.size)

            try:
                bbox = grid[i][j].get_bounds()

                for p in range(bbox[0], bbox[2]):
                    for q in range(bbox[1], bbox[3]):
                        mask.putpixel((p, q), 255)

                try:
                    avg = ImageStat.Stat(after, mask = mask).rms

                    # rd[i][j] = (avg[0] + avg[1] + avg[2]) / 3

                    try:
                        rd[i][j] = math.sqrt(
                                        math.pow(avg[0], 2)
                                        + math.pow(avg[1], 2)
                                        + math.pow(avg[2], 2)
                                    )
                    except IndexError:
                        rd[i][j] = avg[0]
                except ZeroDivisionError:
                    print 'i = %d, j = %d' % (i, j)
            except AttributeError:
                pass

    # grain = int(before.height * float(grain) / after.height)

    # try:
    #     ith = int(bool(before.width % grain))
    #     jth = int(bool(before.height % grain))
    # except ZeroDivisionError:
    #     print 'grain size must be a positive integer.'
    #     return  None

    # jth = 0
    # ith = 0

    before = before.resize(after.size, Image.ANTIALIAS)

    grid = [[None for j in range(before.height / grain + jth)] for i in range(before.width / grain + ith)]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = BoundingBox(
                grain * i,
                grain * j,
                min(grain * (i + 1), before.width),
                min(grain * (j + 1), before.height)
            )

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            mask = Image.new('L', before.size)

            try:
                bbox = grid[i][j].get_bounds()

                for p in range(bbox[0], bbox[2]):
                    for q in range(bbox[1], bbox[3]):
                        try:
                            mask.putpixel((p, q), 255)
                        except IndexError:
                            pass

                try:
                    avg = ImageStat.Stat(before, mask = mask).rms

                    # rd[i][j] = (avg[0] + avg[1] + avg[2]) / 3

                    try:
                        try:
                            rd[i][j] -= math.sqrt(
                                            math.pow(avg[0], 2)
                                            + math.pow(avg[1], 2)
                                            + math.pow(avg[2], 2)
                                        )
                        except IndexError:
                            rd[i][j] -= avg[0]
                    except IndexError:
                        pass
                except ZeroDivisionError:
                    print 'i = %d, j = %d' % (i, j)
            except AttributeError:
                pass

    return list_to_arr(rd)

if __name__ == '__main__':
    number = 75
    index  = 'B'

    try:
        before = Image.open('/Users/nickbond/Documents/School/Spring 2018/MSE 4420/tiles/unscuffed/A00%d %s.jpg' % (number, index))
        after  = Image.open('/Users/nickbond/Documents/School/Spring 2018/MSE 4420/tiles/scuffed/A00%d %s_.jpg' % (number, index))

        grain = 20

        data = image_subtract(before, after, grain)

        pp.pcolormesh(data)
        pp.show()

    except IOError:
        print 'use a file that exists'
