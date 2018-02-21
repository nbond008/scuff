from PIL import Image, ImageStat
from process import findscuff

box = findscuff.find_scuff(
    'test_images/testbefore.png',
    'test_images/testafter2.png'
)

print box[0].get_bounds()

box2 = findscuff.find_scuff(
    'test_images/testbefore.png',
    'test_images/testafter2.png',
    cutoff = box[1] + 10
)

print box2[0].get_bounds()

before = Image.open('test_images/testbefore.png')
cropped_before = before.crop(box2[0].get_bounds())
before.close()

after2 = Image.open('test_images/testafter2.png')
cropped_after = after2.crop(box2[0].get_bounds())
after2.close()

cropped_after.show()

rms_before = ImageStat.Stat(cropped_before).rms
rms_after = ImageStat.Stat(cropped_after).rms

print 'before: [%3.3f, %3.3f, %3.3f]' % (rms_before[0], rms_before[1], rms_before[2])
print 'after: [%3.3f, %3.3f, %3.3f]' % (rms_after[0], rms_after[1], rms_after[2])

cropped_before.close()
cropped_after.close()

#right now, this is just a test for running find_scuff
#using previous find_scuff parameters as an input.
#
#most of find_scuff's parameters can be user-defined
#but are optional, including the debug options 'showing' and 'stopping'.
#
#it seems obvious, but setting initial cutoff lower leads to much faster divergence.
