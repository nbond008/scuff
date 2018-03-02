from PIL import Image, ImageStat
from process.bbox import BoundingBox
import matplotlib.pyplot as pp
import numpy as np
from sys import exit, argv
from array import array
import math
from time import clock

#dumb array transformations just to get it to look like the original image
def list_to_arr(l):
    return np.flipud(np.array(l).transpose())

def arr_to_list(a):
    return np.flipud(a).transpose().tolist()

def find_scuff(before, after, grain, testpath = '/Users/nickbond/Desktop/test.csv'):
    start = float(clock())

    baseline = ImageStat.Stat(before).rms

    print baseline

    ith = int(bool(after.width % grain))
    jth = int(bool(after.height % grain))

    grid = [[None for j in range(after.height / grain + jth)] for i in range(after.width / grain + ith)]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = BoundingBox(
                grain * i,
                grain * j,
                min(grain * (i + 1), after.width),
                min(grain * (j + 1), after.height)
            )

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

                    rd[i][j] = math.sqrt(
                                    math.pow(avg[0] - baseline[0], 2)
                                    + math.pow(avg[1] - baseline[1], 2)
                                    + math.pow(avg[2] - baseline[2], 2)
                                )
                except ZeroDivisionError:
                    print 'i = %d, j = %d' % (i, j)
            except AttributeError:
                pass

            # print rd[i][j]

    # newimg = Image.fromarray(np.array(rd).transpose())
    # newimg.show()

    rd_dx   = [[0.0 for j in range(len(grid[0]))] for i in range(len(grid) - 2)]
    rd_dy   = [[0.0 for j in range(len(grid[0]) - 2)] for i in range(len(grid))]
    rd_del2 = [[0.0 for j in range(len(grid[0]) - 2)] for i in range(len(grid) - 2)]

    dx = 2 * grain
    dy = 2 * grain

    # d(rd)/dx
    for i in range(1, len(grid) - 1):
        for j in range(len(grid[0])):
            drd = (rd[i + 1][j] - rd[i - 1][j])

            rd_dx[i - 1][j] = drd / dx

    # d(rd)/dy
    for i in range(len(grid)):
        for j in range(1, len(grid[0]) - 1):
            drd = (rd[i][j + 1] - rd[i][j - 1])

            rd_dy[i][j - 1] = drd / dy

    # d^2(rd)/dxdy
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            drdy = (rd_dy[i + 1][j - 1] - rd_dy[i - 1][j - 1])
            drdx = (rd_dx[i - 1][j + 1] - rd_dx[i - 1][j - 1])

            try:
                rd_del2[i - 1][j - 1] = (drdy / dx + drdx / dy) / 2
            except IndexError:
                print 'i = %d, j = %d' % (i, j)

    maxdx = np.unravel_index(
        np.argmax(list_to_arr(np.flipud(rd_dx).transpose()), axis=None),
        list_to_arr(np.flipud(rd_dx).transpose()).shape
    )

    mindx = np.unravel_index(
        np.argmin(list_to_arr(np.flipud(rd_dx).transpose()), axis=None),
        list_to_arr(np.flipud(rd_dx).transpose()).shape
    )

    maxdy = np.unravel_index(
        np.argmax(list_to_arr(np.flipud(rd_dy).transpose()), axis=None),
        list_to_arr(np.flipud(rd_dy).transpose()).shape
    )

    mindy = np.unravel_index(
        np.argmin(list_to_arr(np.flipud(rd_dy).transpose()), axis=None),
        list_to_arr(np.flipud(rd_dy).transpose()).shape
    )

    deriv_max_dx = BoundingBox(
        max((mindx[0] - 2) * grain, 0),
        max((mindx[1] - 2) * grain, 0),
        min((maxdx[0] + 2) * grain, after.width),
        min((maxdx[1] + 2) * grain, after.height)
    )

    deriv_max_dy = BoundingBox(
        max((mindy[0] - 2) * grain, 0),
        max((mindy[1] - 2) * grain, 0),
        min((maxdy[0] + 2) * grain, after.width),
        min((maxdy[1] + 2) * grain, after.height)
    )

    deriv_max = BoundingBox.combine(deriv_max_dx, deriv_max_dy)
    # deriv_max.expand(grain, 'es')

    print deriv_max.get_bounds()

    cropped = after.crop(deriv_max.get_bounds())
    cropped.show()

    # rd on a log scale
    # for i in range(len(grid)):
    #     for j in range(len(grid[0])):
    #         rd[i][j] = math.pow(2, rd[i][j])

    pp.figure(1)
    pp.pcolormesh(
        list_to_arr(rd)
    )

    pp.figure(2)
    pp.pcolormesh(
        list_to_arr(rd_dx)
    )

    pp.figure(3)
    pp.pcolormesh(
        list_to_arr(rd_dy)
    )

    pp.figure(4)
    pp.pcolormesh(
        list_to_arr(rd_del2)
    )

    print 'elapsed time: %0.2fs' % (float(clock()) - start)

    print 'max d(rd)/dx = %0.3f\nmin d(rd)/dx = %0.3f\nmax d(rd)/dy = %0.3f\nmin d(rd)/dy = %0.3f' % (
        list_to_arr(np.flipud(rd_dx).transpose())[maxdx],
        list_to_arr(np.flipud(rd_dx).transpose())[mindx],
        list_to_arr(np.flipud(rd_dy).transpose())[maxdy],
        list_to_arr(np.flipud(rd_dy).transpose())[mindy]
    )

    pp.show()



    # testcsv = open()


if __name__ == '__main__':
    before = Image.open('test_images/testbefore.png')
    after  = Image.open('test_images/testafter3.png')

    grain = int(math.sqrt(after.width**2 + after.height**2)) / 100
    comment = ' (default)'

    try:
        if argv[1]:
            grain = int(argv[1])
            comment = ''
    except IndexError:
        comment = ' (default - input error)'
    except ValueError:
        comment = ' (default - value error)'

    print 'grain = %d%s' % (grain, comment)

    find_scuff(before, after, grain)
