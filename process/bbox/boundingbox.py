# The BoundingBox class provides an easy framework for manipulating
# rectangular bounding boxes for image manipulation.
#
# Bounds will be written in the format [x0, y0, x1, y1] in order to
# match Pillow's standards within ImageDraw.

class BoundingBox(object):
    bounds = [0, 0, 0, 0]
    area   = 0

    def __init__(self, *bounds):
        self.set_bounds(bounds)

    # set_bounds
    # inputs:  bounds (either four ints or a tuple)
    # outputs: none
    def set_bounds(self, bounds):
        try:
            for i in bounds[0]:
                pass
            self.bounds = list(bounds[0])
        except TypeError:
            self.bounds = list(bounds)

        if self.bounds[0] > self.bounds[2]:
            temp = self.bounds[0]
            self.bounds[0] = self.bounds[2]
            self.bounds[2] = temp

        if self.bounds[1] > self.bounds[3]:
            temp = self.bounds[1]
            self.bounds[1] = self.bounds[3]
            self.bounds[3] = temp

        if len(self.bounds) != 4:
            raise IndexError('Bounding box requires 4 indices: [x0, y0, x1, y1]')

        self.area = abs(self.bounds[2] - self.bounds[0]) * abs(self.bounds[3] - self.bounds[1])

    # get_bounds
    # inputs:  none
    # outputs: bounds (tuple)
    def get_bounds(self):
        return tuple(self.bounds)

    # get_area
    # inputs:  none
    # outputs: the area enclosed within bounds
    def get_area(self):
        return self.area

    ### static methods ###

    # combine
    # inputs:  two BoundingBox objects
    # outputs: one BoundingBox object containing the union of both inputs
    @staticmethod
    def combine(a, b):
        if a == b:
            print 'nice'
            return a

        av = a.get_bounds()
        bv = b.get_bounds()

        return BoundingBox(
            min(av[0], bv[0]),
            min(av[1], bv[1]),
            max(av[2], bv[2]),
            max(av[3], bv[3])
        )

    ### comparison methods ###

    def __lt__(self, other):
        return self.get_area() < other.get_area()

    def __le__(self, other):
        return self.get_area() <= other.get_area() or (self == other)

    def __eq__(self, other):
        sv = self.get_bounds()
        ov = other.get_bounds()

        return self.get_area() == other.get_area() and (
            sv[0] == ov[0]
            and sv[1] == ov[1]
            and sv[2] == ov[2]
            and sv[3] == ov[3]
        )

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return self.get_area() > other.get_area()

    def __ge__(self, other):
        return self.get_area() >= other.get_area() or (self == other)

    def __hash__(self):
        sv = self.get_bounds()
        return hash((
            self.get_area(),
            sv[0],
            sv[1],
            sv[2],
            sv[3]
        ))

    def __repr__(self):
        sv = self.get_bounds()
        return 'BoundingBox(bounds=[%d, %d, %d, %d])' % (sv[0], sv[1], sv[2], sv[3])

    def __contains__(self, item):
        try:
            for i in item:
                pass
        except TypeError:
            return False

        sv = self.get_bounds()
        try:
            point = (item[0], item[1])
            return item[0] >= sv[0] and item[1] >= sv[1] and item[0] < sv[2] and item[1] < sv[3]
        except IndexError:
            return False

if __name__ == '__main__':
    bb = BoundingBox(0, 0, 10, 10)
    bb2 = BoundingBox([0, 0, 10, 10])
    print bb2.get_area()
