from PIL import Image, ImageStat, ImageDraw, ImageColor
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

threshold = range(5, 256, 10)

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
                draw.point(
                    [x, y],
                    fill = (
                        int(abs(px[x, y][0] - stat[0])),
                        int(abs(px[x, y][1] - stat[1])),
                        int(abs(px[x, y][2] - stat[2])),
                        int(threshold[len(threshold) - 1 - i] * 255 / len(threshold))
                    ))
                index[x][y] += 1

bbox = [[after.width, after.height, -1, -1] for i in range(len(threshold))]
margin = 12

for i in range(len(threshold)):
    ex = False

    for x in range(1, after.width - 1):
        for y in range(1, after.height - 1):
            if index[x][y] <= i:
                bbox[i][0] = x - margin
            else:
                ex = True
                break
        if ex:
            break

    ex = False

    for y in range(1, after.height - 1):
        for x in range(1, after.width - 1):
            if index[x][y] <= i:
                bbox[i][1] = y - margin
            else:
                ex = True
                break
        if ex:
            break

    ex = False

    for x in reversed(range(1, after.width - 1)):
        for y in reversed(range(1, after.height - 1)):
            if index[x][y] <= i:
                bbox[i][2] = x + margin
            else:
                ex = True
                break
        if ex:
            break

    ex = False

    for y in reversed(range(1, after.height - 1)):
        for x in reversed(range(1, after.width - 1)):
            if index[x][y] <= i:
                bbox[i][3] = y + margin
            else:
                ex = True
                break
        if ex:
            break

for i in range(len(bbox)):
    draw.rectangle(
            bbox[i],
            outline = (
                255,
                255,
                255,
                int(i * 255 / len(bbox))
            )
        )

new.show()

new.close()
