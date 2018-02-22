from PIL import Image, ImageStat
from process.bbox import BoundingBox
from process import findscuff
from sys import exit
from time import clock
import math

# find_scuff still needs some work, but for now we have a basic framework
# that picks out the scuffed area, crops the image to fit it, and finally
# checks against a (currently arbitrary) standard to guage whether the
# area is large or visible enough to constitute a scuff.

# score_scuff
# inputs:
#         before_path: path to the pre-scuff image
#         after_path : path to the post-scuff image
#         maxvalue   : the maximum acceptable rms difference between the images
#         cutoff     : initial cutoff for find_scuff
#         step       : cutoff step for find_scuff
#         margin     : the amount of margin around the cropped image
#         showing    : toggle for debug information
#
# outputs: a tuple containing the following:
#         a binary score (is this sample scuffed?)
#         the rms RGB values for the pre-scuff image
#         the rms RGB values for the post-scuff image
#         a BoundingBox object representing the location and size of the scuff
#         the final cutoff from find_scuff
def score_scuff(before_path, after_path, maxvalue, cutoff = 255, step = 10, margin = 5, showing = False):
    start = float(clock())

    before = Image.open(before_path)
    after = Image.open(after_path)

    if showing:
        print 'starting first run. time elapsed since start: %ss' % (float(clock()) - float(start))

    box = findscuff.find_scuff(
        before,
        after,
        cutoff = cutoff,
        step = step,
        margin = margin,
        stopping = False
    )

    box[0].expand(margin)
    x = box[0].get_bounds()[0]
    y = box[0].get_bounds()[1]

    if showing:
        print 'bounding box after first run: %s' % box[0]
        print 'starting second run. time elapsed since start: %ss' % (float(clock()) - float(start))

    box2 = findscuff.find_scuff(
        before.crop(box[0].get_bounds()),
        after.crop(box[0].get_bounds()),
        cutoff = cutoff,
        step = 0.5,
        margin = margin,
        stopping = True
    )

    if showing:
        print 'finished second run. time elapsed since start: %ss' % (float(clock()) - float(start))

    box2[0].translate(x, y)
    box2[0].expand(5)

    before = Image.open(before_path)
    cropped_before = before.crop(box2[0].get_bounds())
    before.close()

    after2 = Image.open(after_path)
    cropped_after = after2.crop(box2[0].get_bounds())
    after2.close()

    rms_before = ImageStat.Stat(cropped_before).rms
    rms_after = ImageStat.Stat(cropped_after).rms

    if showing:
        print 'final cutoff: %0.1f' % box2[1]

        print 'before: [%3.3f, %3.3f, %3.3f]' % (rms_before[0], rms_before[1], rms_before[2])
        print 'after: [%3.3f, %3.3f, %3.3f]\n' % (rms_after[0], rms_after[1], rms_after[2])

        print '%f\n' % findscuff.get_rms(rms_before, rms_after)

    if showing:
        if findscuff.get_rms(rms_before, rms_after) / 3 < maxvalue:
            print 'no scuff detected\n'
        else:
            print 'scuff detected\n'

    cropped_before.close()
    cropped_after.close()

    return (
        findscuff.get_rms(rms_before, rms_after) / 3 >= maxvalue,
        rms_before,
        rms_after,
        box2[0],
        box2[1]
    )

def format_row(info, header = False):
    if header:
        return '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n' % (
            'Is it scuffed?',
            'R before',
            'G before',
            'B before',
            'R after',
            'G after',
            'B after',
            'x0 (px)',
            'y0 (px)',
            'x1 (px)',
            'y1 (px)',
            'Box Area (px^2)',
            'Final cutoff'
        )
    try:
        scuffed = 'No'
        if info[0]:
            scuffed = 'Yes'

        return '%s, %3.3f, %3.3f, %3.3f, %3.3f, %3.3f, %3.3f, %d, %d, %d, %d, %d, %d\n' % (
            scuffed,
            info[1][0],
            info[1][1],
            info[1][2],
            info[2][0],
            info[2][1],
            info[2][2],
            info[3].get_bounds()[0],
            info[3].get_bounds()[1],
            info[3].get_bounds()[2],
            info[3].get_bounds()[3],
            info[3].get_area(),
            info[4]
        )
    except IndexError, AttributeError:
        return ''
