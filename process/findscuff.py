from PIL import Image, ImageStat, ImageDraw, ImageColor
from process.bbox import BoundingBox
from sys import exit

def get_bbox(cond, margin): #there's gotta be a better way to do this
    bounds = [after.width, after.height, -1, -1]
    ex = False

    for x in range(len(cond)):
        for y in range(len(cond[0])):
            if not cond[x][y]:
                bounds[0] = max(0, x - margin)
            else:
                ex = True
                break
        if ex:
            break

    ex = False

    for y in range(len(cond[0])):
        for x in range(len(cond)):
            if not cond[x][y]:
                bounds[1] = max(0, y - margin)
            else:
                ex = True
                break
        if ex:
            break

    ex = False

    for x in reversed(range(len(cond))):
        for y in reversed(range(len(cond[0]))):
            if not cond[x][y]:
                bounds[2] = min(len(cond), x + margin)
            else:
                ex = True
                break
        if ex:
            break

    ex = False

    for y in reversed(range(len(cond[0]))):
        for x in reversed(range(len(cond))):
            if not cond[x][y]:
                bounds[3] = min(len(cond[0]), y + margin)
            else:
                ex = True
                break
        if ex:
            break

    return BoundingBox(bounds)

try:
    before = Image.open('test_images/testbefore.png')
    after  = Image.open('test_images/testafter2.png') #these will be user-defined later
except IOError:
    print 'run from the repo root'
    exit(0)

stat = ImageStat.Stat(before).rms #might have to test rms/mean/median
before.close()

if after.size != before.size:
    raise IOError('images must be the same size')

new = Image.new('RGB', after.size)

px = after.load() #ugh there's gotta be a better way than loading pixels

step = 5
cutoff = 255

# index = [[0 for y in range(after.height)] for x in range(after.width)]    #i don't think indexing is gonna be necessary
cond = [[False for y in range(after.height)] for x in range(after.width)]
prevbox = BoundingBox(1, 1, after.width - 1, after.height - 1)

finalcutoff = 256
finalbox    = None

margin = 5 #this will either be user defined or learned

while cutoff > 0:
    prev_bound = prevbox.get_bounds()
    for x in range(prev_bound[0] - 1, prev_bound[2] + 1):
        for y in range(prev_bound[1] - 1, prev_bound[3] + 1):
            if (abs(px[x, y][0] - stat[0]) > cutoff
                    and abs(px[x, y][1] - stat[1]) > cutoff
                    and abs(px[x, y][2] - stat[2]) > cutoff):
                cond[x][y] = True

    try:
        currbox = get_bbox(cond, margin)
        if currbox != prevbox:
            print '%s - %d' % (currbox.get_bounds(), currbox.get_area())
    except IndexError:
        cutoff = -1

    if BoundingBox.combine(currbox, prevbox) != prevbox:
        finalcutoff = cutoff
        finalbox = prevbox
        cutoff = -1 #comment out this line to see how the box changes after reaching this size

    prevbox = currbox
    cutoff -= step

max_index = -1

print finalbox
print finalcutoff

cropped = after.crop(currbox.get_bounds())
cropped.show()
