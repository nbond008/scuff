from PIL import Image

scuffed = Image.open("test_images/testafter.png")
scuffhist = scuffed.histogram() # 768-element list of [number of pixels with R=0, #px with R=1, ... R=255, G = 0,...G=255, B=0....]
clean = Image.open("test_images/testbefore.png")
cleanhist = clean.histogram() # generate an identical list for the clean image
difference = [s-c for c, s in zip(cleanhist, scuffhist)] # take difference between lists

w, h = scuffed.size
totalpx = w*h # get number of pixels in image
threshold = 2
if max([abs(i) for i in difference])>=totalpx*(threshold/100): print "test A detects scuff!" # if more than threshhold% of pixels show a color change, claim it's scuffed


#this is probably not an ideal scuff test, as for example every pixel could change 1 R/G/B due to slight lighting change
#possibly require change of certain number of pixels?
#machine learning stuff could be applied to the RGB list very easily with sufficient training data since neural networks are linear algebra anyway
#but that seems excessive
#another approach...

modifier = range(0, 256)*3 # generate the list [0, 1, ...255, 0, 1, ...255, 0, 1, ...255]
cleanweighted = [cleanhist[i]*modifier[i] for i in range(0, 768)] # weight pixel values according to intensity

# for clarification: recall that the original histogram list is a 768-element list containing the /number/ of pixels with each RGB values
# so the first element in the list is the number of pixels with R=0, the second is with R=1, etc...
# effectively, we are multiplying each element by the intensity it corresponds to, so we have a way to calculate total "redness",  "blueness", "greenness"

scuffweighted = [scuffhist[i]*modifier[i] for i in range(0, 768)]
rgbclean = [sum(cleanweighted[0:255]), sum(cleanweighted[256:511]), sum(cleanweighted[512:767])] # get total R, G, B of clean...
rgbscuff = [sum(scuffweighted[0:255]), sum(scuffweighted[256:511]), sum(scuffweighted[512:767])] # ... and of scuffed
rmsdist = (sum([((rgbclean[i] - rgbscuff[i])**2) for i in range(0, 3)]))**0.5/totalpx # get rms change in color; effectively euclidean metric distance;
# then divided by totalpx to normalize to size of image

print rmsdist
#need to establish a value that actually represents a scuff


