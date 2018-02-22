from PIL import Image, ImageStat
from process.bbox import BoundingBox
from process import findscuff
from sys import exit
from time import clock
import math

start = float(clock())

maxvalue = 10

before = Image.open('test_images/testbefore.png')
after = Image.open('test_images/testafter2.png')

print 'starting first run. time elapsed since start: %ss' % (float(clock()) - float(start))

box = findscuff.find_scuff(
    before,
    after,
    step = 10,
    stopping = False
)

# bb = box[0].get_bounds()
#
# bbb = BoundingBox(bb[0], bb[1], bb[2], (bb[3] + bb[1]) / 2)
bbb = box[0]
bbb.expand(5)
print bbb

x = bbb.get_bounds()[0]
y = bbb.get_bounds()[1]

print 'starting second run. time elapsed since start: %ss' % (float(clock()) - float(start))

box2 = findscuff.find_scuff(
    before.crop(bbb.get_bounds()),
    after.crop(bbb.get_bounds()),
    step = 0.5,
    stopping = True
)

print 'finished second run. time elapsed since start: %ss' % (float(clock()) - float(start))

box2[0].translate(x, y)
box2[0].expand(5)

before = Image.open('test_images/testbefore.png')
cropped_before = before.crop(box2[0].get_bounds())
before.close()

after2 = Image.open('test_images/testafter2.png')
cropped_after = after2.crop(box2[0].get_bounds())
after2.close()

print box2[0].get_area()

rms_before = ImageStat.Stat(cropped_before).rms
rms_after = ImageStat.Stat(cropped_after).rms

print 'final cutoff: %0.1f' % box2[1]

print 'before: [%3.3f, %3.3f, %3.3f]' % (rms_before[0], rms_before[1], rms_before[2])
print 'after: [%3.3f, %3.3f, %3.3f]\n' % (rms_after[0], rms_after[1], rms_after[2])

print '%f\n' % findscuff.get_rms(rms_before, rms_after)

if findscuff.get_rms(rms_before, rms_after) < maxvalue:
    print 'no scuff detected\n'
    # after.show()
else:
    print 'scuff detected\n'
    # cropped_after.show()

cropped_before.close()
cropped_after.close()

# this is now a test for running find_scuff under different conditions
# and measuring using rms distances whether a scuff seems to be visible.
#
# find_scuff still needs some work, but for now we have a basic framework
# that picks out the scuffed area, crops the image to fit it, and finally
# checks against a (currently arbitrary) standard to guage whether the
# area is large or visible enough to constitute a scuff.
