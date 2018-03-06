from scipy import stats
from numpy import mean, std
from PIL import Image, ImageStat
from math import sqrt

def pxrms(pixel): # rms magnitude of pixel
	return sqrt(sum([pixel[i]**2 for i in range(0, 3)]))
	
def geom(pixel): # geometric mean of rgb
	return (pixel[0]*pixel[1]*pixel[2])**(0.333333)
	
def listify(image): #returns list of rms pixel values in img
	size = image.size
	pixels = []
	for i in range(0, size[0]):
		for j in range(0, size[1]):
			pixels.append(pxrms(image.getpixel((i, j))))

	return pixels
	

left = Image.open('test_images/testbefore.png')
right = Image.open('test_images/testafter3.png')
dim = left.size
#right.crop((0, 0, dim[0]-1, dim[1]-1))

llist = listify(left)
rlist = listify(right)
print stats.ttest_ind(llist, rlist, None, False)
print std(llist), std(rlist)

# need consistent lighting!

