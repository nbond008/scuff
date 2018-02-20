from PIL import Image
from PIL import PSDraw
import numpy

def avglist(list):
	return tuple([int(round(sum(list)/len(list))) for num in list]) # takes a pixel as a list and returns a 3-tuple of the average value 3 times

def rmspx(avg, normal): # takes RMS distance of pixel from its greyscaled equivalent
	value = 0
	for i in range(0, len(normal)):
		value+=(avg[i]-normal[i])**4
	value = int(round((value/len(normal))**0.25))
	return tuple([value, value, value])

im = Image.open("Test_Images/testafter.png")
w, h = im.size
grey = Image.open("Test_Images/testafter.png") # sacrificial image to greyscale

for i in range(0, w):
	for j in range(0, h):
		grey.putpixel((i, j), avglist(im.getpixel((i, j)))) # replace pixel with its RGB average

rms = Image.open("Test_Images/testafter.png")

for i in range(0, w):
	for j in range(0, h):
		rms.putpixel((i, j), rmspx(list((grey.getpixel((i, j)))), (im.getpixel((i, j))))) # replace pixel with its RMS distance

rms.save("testout.png")
