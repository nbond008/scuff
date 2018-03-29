from scipy import stats, fftpack
from numpy import mean, std
import numpy
from PIL import Image, ImageStat, ImageEnhance
from math import sqrt
from bbox import boundingbox
import narrowbox

pic = Image.open('test_images/realafter_cropped.jpg')
contraster = ImageEnhance.Contrast(pic)
pic.show()
pic = contraster.enhance(0.5)
pic = pic.convert('L')
pic.show()
pic.save('test.png')
transformed = fftpack.fft2(pic)
transformed = abs(transformed)
trans = Image.fromarray(numpy.uint8(transformed), 'L')
trans.show()