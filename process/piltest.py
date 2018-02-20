from PIL import Image, ImageStat, ImageDraw, ImageColor
from process.bbox import BoundingBox
from sys import exit

try:
    before = Image.open('test_images/testbefore.png')
    after  = Image.open('test_images/testafter2.png')
except IOError:
    print 'run from the repo root'
    exit(0)

stat = ImageStat.Stat(before).median
before.close()

if after.size != before.size:
    raise IOError('images must be the same size')

new = Image.new('RGB', after.size)

draw = ImageDraw.Draw(new, 'RGBA')

px = after.load()
index = [[0 for y in range(after.height)] for x in range(after.width)]

threshold = range(5, 256, 1)

for i in range(len(threshold)):

    condition = [[False for y in range(after.height)] for x in range(after.width)]

    for x in range(1, after.width - 1):
        for y in range(1, after.height - 1):
            condition[x][y] = (
                    abs(px[x, y][0] - stat[0]) > threshold[len(threshold) - 1 - i]
                    and abs(px[x, y][1] - stat[1]) > threshold[len(threshold) - 1 - i]
                    and abs(px[x, y][2] - stat[2]) > threshold[len(threshold) - 1 - i]
                )

            if condition[x][y]:
                # draw.point(
                #     [x, y],
                #     fill = (
                #         int(abs(px[x, y][0] - stat[0])),
                #         int(abs(px[x, y][1] - stat[1])),
                #         int(abs(px[x, y][2] - stat[2])),
                #         int(threshold[len(threshold) - 1 - i] * 255 / len(threshold))
                #     ))
                index[x][y] += 1

bbox = [None for i in range(len(threshold))]
margin = 12

for i in range(len(threshold)):
    bounds = [after.width, after.height, -1, -1]
    ex = False

    for x in range(1, after.width - 1):
        for y in range(1, after.height - 1):
            if index[x][y] <= i:
                bounds[0] = x - margin
            else:
                ex = True
                break
        if ex:
            break

    ex = False

    for y in range(1, after.height - 1):
        for x in range(1, after.width - 1):
            if index[x][y] <= i:
                bounds[1] = y - margin
            else:
                ex = True
                break
        if ex:
            break

    ex = False

    for x in reversed(range(1, after.width - 1)):
        for y in reversed(range(1, after.height - 1)):
            if index[x][y] <= i:
                bounds[2] = x + margin
            else:
                ex = True
                break
        if ex:
            break

    ex = False

    for y in reversed(range(1, after.height - 1)):
        for x in reversed(range(1, after.width - 1)):
            if index[x][y] <= i:
                bounds[3] = y + margin
            else:
                ex = True
                break
        if ex:
            break

    bbox[i] = BoundingBox(bounds)

adraw = ImageDraw.Draw(after, 'RGBA')

for i in range(len(bbox)):
    adraw.rectangle(
            bbox[i].get_bounds(),
            outline = (
                0,
                0,
                0,
                int(i * 255 / len(bbox))
            )
        )

final = 0

prev = BoundingBox([after.width, after.height, -1, -1])
prevdiff = 0

for i in range(len(bbox)):
    diff = bbox[i].get_area() - prev.get_area()
    if BoundingBox.combine(prev, bbox[i]) == prev:
        prev = bbox[i]
        if (prevdiff - diff) > 0:
            final = i
        prevdiff = diff

# here's the box we care about

adraw.rectangle(
    bbox[final].get_bounds(),
    outline = (
        255,
        0,
        0,
        255
    )
)

after.show()

after.close()
new.close()
