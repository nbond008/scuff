from process import findscuff

box = findscuff.find_scuff(
    'test_images/testbefore.png',
    'test_images/testafter2.png'
)

print box

box2 = findscuff.find_scuff(
    'test_images/testbefore.png',
    'test_images/testafter2.png',
    cutoff = box[1] + 10
)

print box2

#right now, this is just a test for running find_scuff
#using previous find_scuff parameters as an input.
#
#most of find_scuff's parameters can be user-defined
#but are optional, including the debug options 'showing' and 'stopping'.
#
#it seems obvious, but setting initial cutoff lower leads to much faster divergence. 
