from PIL import Image, ImageStat, ImageDraw, ImageColor
from process.bbox import BoundingBox
from sys import exit, argv

def get_bbox(cond, margin): #there's gotta be a better way to do this
    bounds = [len(cond) + 1, len(cond[0]) + 1, -1, -1]
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

# a lot of parameters are user defined now
def find_scuff(before_path, after_path, cutoff = 255, step = 5, margin = 5, prevbox = BoundingBox(-100000, -100000, 100000, 100000), showing = False, stopping = True):
    try:
        before = Image.open(before_path)
        after  = Image.open(after_path) #these will be user-defined later
    except IOError:
        raise IOError('run from the repo root')

    stat = ImageStat.Stat(before).rms #might have to test rms/mean/median
    before.close()

    if after.size != before.size:
        raise IOError('images must be the same size')

    new = Image.new('RGB', after.size)

    px = after.load() #ugh there's gotta be a better way than loading pixels

    cond = [[False for y in range(after.height)] for x in range(after.width)]

    if BoundingBox.combine(prevbox, BoundingBox(1, 1, after.width - 1, after.height - 1)) != prevbox or prevbox > BoundingBox(1, 1, after.width - 1, after.height - 1):
        prevbox = BoundingBox(1, 1, after.width - 1, after.height - 1)

    finalcutoff = 256
    finalbox    = None

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
            if currbox != prevbox and showing:
                print '%s - %d' % (currbox.get_bounds(), currbox.get_area())
        except IndexError:
            cutoff = -1

        if BoundingBox.combine(currbox, prevbox) != prevbox:
            finalcutoff = cutoff
            finalbox = prevbox
            if stopping:
                cutoff = -1

        prevbox = currbox
        cutoff -= step

    max_index = -1

    if showing: #only show these things in debug mode
        print finalbox
        print finalcutoff
        cropped = after.crop(currbox.get_bounds())
        cropped.show()

    return (finalbox, finalcutoff) #returns both values:
    #the latter might be useful for learning, and
    #the former is actually what we care about

#running findscuff.py from command line is basically debug mode
if __name__ == '__main__':
    try:
        find_scuff(argv[1], argv[2], showing = True, stopping = False)
    except IndexError:
        print 'usage: python findscuff.py <before>.png <after>.png'
