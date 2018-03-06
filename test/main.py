from process import im_process as ip
from time import clock

start = float(clock())

scores = [
    ip.score_scuff(
        'test_images/testbefore.png',
        'test_images/testbefore.png',
        3,
        showing = True
    ),
    ip.score_scuff(
        'test_images/testbefore.png',
        'test_images/testafter.png',
        3,
        showing = True
    ),
    ip.score_scuff(
        'test_images/testbefore.png',
        'test_images/testafter2.png',
        3,
        showing = True
    ),
    ip.score_scuff(
        'test_images/testbefore.png',
        'test_images/testafter3.png',
        3,
        showing = True
    ),
    ip.score_scuff(
        'test_images/testbefore.png',
        'test_images/testafter4.png',
        3,
        showing = True
    )
]

f = open('/Users/nickbond/Desktop/test.csv', 'w') #replace this line

f.write(ip.format_row(None, header = True))

for score in scores:
    f.write(ip.format_row(score))

f.close()

print 'success! total time elapsed: %ss' % (float(clock()) - float(start))
