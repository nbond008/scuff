from PIL import Image

scuffed = Image.open("test_images/testafter.png")
scuffhist = scuffed.histogram() # 768-element list of [number of pixels with R=0, #px with R=1, ... R=255, G = 0,...G=255, B=0....]
clean = Image.open("test_images/testbefore.png")
cleanhist = clean.histogram() # generate an identical list for the clean image
difference = [s-c for c, s in zip(cleanhist, scuffhist)] # take difference between lists

w, h = scuffed.size
totalpx = w*h # get number of pixels in image
threshold = 2
if max([abs(i) for i in difference])>=totalpx*(threshold/100): print "scuffed!" # if more than threshhold% of pixels show a color change, claim it's scuffed

#this is probably not an ideal scuff test, as for example every pixel could change 1 R/G/B due to slight lighting change
#possibly require change of certain number of pixels?
#machine learning stuff could be applied to the RGB list very easily with sufficient training data since neural networks are linear algebra anyway
#but that seems excessive
