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

                    rd[i][j] = (avg[0] + avg[1] + avg[2]) / 3

                    # rd[i][j] = math.sqrt(
                    #                 math.pow(avg[0] - baseline[0], 2)
                    #                 + math.pow(avg[1] - baseline[1], 2)
                    #                 + math.pow(avg[2] - baseline[2], 2)
                    #             )
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
        for j in range(len(grid[0]) - 2):
            drd = (rd_dy[i + 1][j] - rd_dy[i - 1][j])

            try:
                rd_del2[i - 1][j] = drd / dx
            except IndexError:
                print 'i = %d, j = %d' % (i, j)

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
    pp.show()

    # testcsv = open()


if __name__ == '__main__':
    before = Image.open('test_images/realbefore_cropped.jpg')
    after  = Image.open('test_images/realafter_cropped.jpg')

    grain = int(math.sqrt(after.width**2 + after.height**2)) / 100

    try:
        if argv[1]:
            grain = int(argv[1])
    except IndexError, ValueError:
        pass

    print 'grain = %d' % grain

    find_scuff(before, after, grain)
