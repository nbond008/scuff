from scipy import stats
from numpy import mean, std
from PIL import Image, ImageStat
from math import sqrt
from bbox import boundingbox
import narrowbox

#outputs['boundingbox']	

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
	
def rgblist(image): # returns r/g/b px values
	size = image.size
	pixels = []
	for i in range(0, size[0]):
		for j in range(0, size[1]):
			for k in range(0, 3):
				px = image.getpixel((i,j))
				pixels.append(px[k])
				
	return pixels


def imdiff(bp, ap): #image difference	
	new = Image.new('RGB', after.size)
	for x in range(after.width):
		for y in range(after.height):
			bp = before.getpixel((x, y))
			ap = after.getpixel((x, y))
			new.putpixel(
				(x, y), (
					abs(bp[0] - ap[0]),
					abs(bp[1] - ap[1]),
					abs(bp[2] - ap[2])
				)
			)
	return new
	
def listMod(list, constant, mode): # adds a constant to a list or multiplies by one
	newlist = []
	for i in list:
		if mode=='+': newlist.append(i+constant)
		elif mode=='*': newlist.append(i*constant)
		else: newlist.append(i)
	
	return newlist
	
	
	

left = Image.open('test_images/zoomin.png')
right = Image.open('test_images/realbefore_cropped.jpg')



#left = left.crop(BoundingBox.get_bounds())
rgbLeft = rgblist(left)
rgbRight = rgblist(right)
rR = rgbLeft[::3]
rG = rgbLeft[1::3]
rB = rgbLeft[2::3]
rRr = rgbRight[::3]
rGr = rgbRight[1::3]
rBr = rgbRight[2::3]
means = [mean(rR), mean(rG), mean(rB)]
stds = [std(rR), std(rG), std(rB)]
zR = abs(mean(rR)-mean(rRr))/std(rR)
zG = abs(mean(rG)-mean(rGr))/std(rG)
zB = abs(mean(rB)-mean(rBr))/std(rB)
print zR, zG, zB








#print listify(rgblist)
#dim = left.size
#right.crop((0, 0, dim[0]-1, dim[1]-1))

#llist = listify(left)
#lmean = mean(llist)
#lstd = std(llist)
#rlist = listify(right)
#rmean = mean(rlist)
#zr = abs(rmean-lmean)/lstd
#print zr
#llist.sort()
#rlist.sort()
#for i in range(-20, 20):
	#print stats.ttest_ind(llist, listMod(rlist, i), None, False)

# need consistent lighting!

