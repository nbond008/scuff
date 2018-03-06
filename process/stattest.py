from scipy import stats
from PIL import Image, ImageStat
from narrowbox import *
import random

alpha = [random.randint(1, 101) for i in range(1, 11)]
beta = [random.randint(10, 101) for i in range(1, 11)]

before = Image.open('test_images/small1.png')
after  = Image.open('test_images/small2.png')

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
heats = data['data']['rd'].tolist()

print data['extrema']['max_rd']

data = find_scuff(after, before, grain)
refheats = data['data']['rd'].tolist()

print stats.ttest_ind(heats, refheats, None, False)

cropped = after.crop(data['boundingbox'].get_bounds())
cropped.show()

print 'actual grain = %d' % data['grain']

print data['extrema']['max_rd']

i = 0
for arr in data['data']:
    pp.figure(i)
    pp.title(arr)
    pp.pcolormesh(data['data'][arr])
    i += 1

pp.show()