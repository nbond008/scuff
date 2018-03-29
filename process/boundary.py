from PIL import Image
from math import sqrt, floor
from numpy import array, ndarray, empty, maximum

def imageDiff(pic):
	print 'b'
	
def pxrms(pixel): # rms magnitude of pixel
	return sqrt(sum([pixel[i]**2 for i in range(0, 3)]))
	
def rmsfrom(comp, pxin):
	out = sqrt(sum([(comp[i]-pxin[i])**2 for i in range(0, 3)]))
	print out
	return out
	
def arrdiff(arr):
	dim = arr.shape
	diff = empty((dim[0]-1, dim[1]-1))

	print arr
			
	print arr[0][0], arr[1][1]
	for i in range(0, dim[0]-1):
		for j in range(0, dim[1]-1):
			diff[i][j] = (arr[i][j]-arr[i+1][j+1])

	rescale = 10 # should instead rescale to a max of 255
	diff = diff*rescale
	
	return diff

pic = Image.open('test_images/realafter_cropped.jpg')
arr = array(pic)
newarr = ndarray.copy(arr)
pxavg = arr.mean(0).mean(0)
dim = arr.shape

'''
for i in range(0, dim[0]):
	for j in range(0, dim[1]):
		for k in range(0, dim[2]):
			newarr[i][j][k]=floor(abs(newarr[i][j][k]-pxavg[k]))
'''
			
pic = pic.convert('L')
arr = array(pic, dtype='int64')
dxy = arrdiff(arr)
print dxy
#diffpic = Image.fromarray(dxy)
#diffpic.show()



		
		
		
		
		
		
		
		
		

out = Image.fromarray(newarr)
out.show()