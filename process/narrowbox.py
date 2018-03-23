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

def find_scuff(before, after, grain, showing = False):
    outputs = dict()

    start = float(clock())

    baseline = ImageStat.Stat(before).rms

    grain = int(min(grain, min(after.width, after.height) / 2.5))

    if showing:
        print 'actual grain = %d' % grain
        print baseline

    outputs['grain'] = grain

    try:
        ith = int(bool(after.width % grain))
        jth = int(bool(after.height % grain))
    except ZeroDivisionError:
        print 'grain size must be a positive integer.'
        return  None

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

    try:
        maxrd = np.unravel_index(
            np.argmax(list_to_arr(np.flipud(rd).transpose()), axis=None),
            list_to_arr(np.flipud(rd).transpose()).shape
        )

        minrd = np.unravel_index(
            np.argmin(list_to_arr(np.flipud(rd).transpose()), axis=None),
            list_to_arr(np.flipud(rd).transpose()).shape
        )

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

    except ValueError:
        print 'grain size must be a positive integer.'
        return None

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

    # print deriv_max.get_bounds()

    outputs['boundingbox'] = deriv_max

    # rd on a log scale
    # for i in range(len(grid)):
    #     for j in range(len(grid[0])):
    #         rd[i][j] = math.pow(2, rd[i][j])

    # pp.figure(1)
    # pp.pcolormesh(
    #     list_to_arr(rd)
    # )
    #
    # pp.figure(2)
    # pp.pcolormesh(
    #     list_to_arr(rd_dx)
    # )
    #
    # pp.figure(3)
    # pp.pcolormesh(
    #     list_to_arr(rd_dy)
    # )
    #
    # pp.figure(4)
    # pp.pcolormesh(
    #     list_to_arr(rd_del2)
    # )

    if showing:
        print 'elapsed time: %0.2fs' % (float(clock()) - start)

    outputs['data'] = {
        'rd'      : list_to_arr(rd),
        'rd_dx'   : list_to_arr(rd_dx),
        'rd_dy'   : list_to_arr(rd_dy),
        'rd_del2' : list_to_arr(rd_del2)
    }

    outputs['extrema'] = {
        'max_rd' : list_to_arr(np.flipud(rd).transpose())[maxrd],
        'min_rd' : list_to_arr(np.flipud(rd).transpose())[minrd],
        'max_dx' : list_to_arr(np.flipud(rd_dx).transpose())[maxdx],
        'min_dx' : list_to_arr(np.flipud(rd_dx).transpose())[mindx],
        'max_dy' : list_to_arr(np.flipud(rd_dy).transpose())[maxdy],
        'min_dy' : list_to_arr(np.flipud(rd_dy).transpose())[mindy]
    }

    dpi_x = after.info['dpi'][0]
    real_width  = after.width / float(dpi_x)
    grain_width = grain / float(dpi_x)

    dpi_y = after.info['dpi'][1]
    real_height  = after.height / float(dpi_y)
    grain_height = grain / float(dpi_y)

    outputs['y'], outputs['x'] = np.mgrid[
        slice(0, real_height, grain_height),
        slice(0, real_width, grain_width)
    ]

    outputs['real_width']   = real_width
    outputs['real_height']  = real_height
    outputs['grain_width']  = grain_width
    outputs['grain_height'] = grain_height

    deriv_bounds = deriv_max.get_bounds()
    outputs['scuff_width']  = (deriv_bounds[2] - deriv_bounds[0]) / float(dpi_x)
    outputs['scuff_height'] = (deriv_bounds[3] - deriv_bounds[1]) / float(dpi_y)
    outputs['scuff_area']   = deriv_max.get_area() / (float(dpi_x) * float(dpi_y))

    return outputs

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
        pass
    except ValueError:
        comment = ' (default - value error)'

    print 'grain = %d%s' % (grain, comment)

    data = find_scuff(before, after, grain)

    try:
        print '\nlist of keys:'
        for key in data:
            print key
    except TypeError:
        print '(none)'
        exit(0)

    cropped = after.crop(data['boundingbox'].get_bounds())
    cropped.show()

    print 'actual grain = %d' % data['grain']

    i = 0
    # for arr in data['data']:

    arr = 'rd'

    pp.figure(i)
    pp.title(arr)
    # try:
    pp.pcolormesh(data['x'], data['y'], data['data'][arr])
    pp.xlabel('x (inches)')
    pp.ylabel('y (inches)')
        # except TypeError:
        #     pass
        #     i += 1

    print '\nimage size: %0.2f\" x %0.2f\"\n' % (
            data['real_width'],
            data['real_height'],
        )

    print 'scuff width: %0.2f inches\nscuff height: %0.2f inches\nscuff area: %0.2f square inches\n' % (
            data['scuff_width'],
            data['scuff_height'],
            data['scuff_area']
        )

    pp.show()

    # print '\nmax rd = %0.3f\nmin rd = %0.3f\nmax d(rd)/dx = %0.3f\nmin d(rd)/dx = %0.3f\nmax d(rd)/dy = %0.3f\nmin d(rd)/dy = %0.3f' % (
