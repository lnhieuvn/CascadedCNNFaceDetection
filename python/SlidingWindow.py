import numpy as np
import cv2
import time
import math
from imagepyramid import ImagePyramid
from PIL import Image
import matplotlib.pyplot as plt

#defines a sliding window that is sliding over the image cascade

def slideWindow(imagePyramid, stepSize, windowLength):
	# labels are stored as [[cx,cy,w], [cx,cy,w]....]

	subwindows = []
	windowCenters = []
	sublabels = []
	for i in range(0, len(imagePyramid.pyramid)):
		image = imagePyramid.pyramid[i].image
		label = imagePyramid.pyramid[i].label
		image_width = image.shape[1]
		image_height = image.shape[0]

		
		for y in np.arange(0,image_height-windowLength,30):
			for x in np.arange(0,image_width-windowLength,30):
				windowCenter = [x+int(windowLength/2),y+int(windowLength/2)]
				subwindow = [image[x:x+windowLength], image[y:y+windowLength]]
				windowCenters.append(windowCenter)
				subwindows.append(subwindow)
				labelwidth = label[2]
				xlabel_left = label[0]-int(labelwidth/2)
				xlabel_right = label[0]+int(labelwidth/2)
				ylabel_upper = label[1]+int(labelwidth/2)
				ylabel_lower = label[1]-int(labelwidth/2)
				margin = 2.0/labelwidth
				sublabelx = 1- margin*(math.fabs(x-xlabel_left)+ math.fabs(x+windowLength-xlabel_right))
				sublabelx = max(sublabelx, 0)
				sublabely = 1- margin*(math.fabs(y-ylabel_upper)+ math.fabs(y+windowLength-ylabel_lower))
				sublabely = max(sublabely, 0)
				print(margin)
				sublabels[i].append([sublabelx, sublabely])
				#copy = image.copy()
				#cv2.rectangle(copy, (x,y), (x+windowLength, y+windowLength), [255, 255, 255],1 )
				#cv2.imshow("Window", copy)
				#cv2.waitKey(1)
				#time.sleep(0.03)


	return [windowCenters, sublabels, subwindow]

## Test the implementation

pil_img = Image.open('images/2002/07/19/big/img_581.jpg').convert('L')
img = np.array(pil_img)


imagePyramid = ImagePyramid(img, np.asarray([155.093404, 189.450662, 205.0]))

rect = imagePyramid.pyramid[0].labelToRect()
cv2.rectangle(imagePyramid.pyramid[0].image, rect[0], rect[1], [0, 255, 0],1 )
[windowCenters, sublabels, subwindow] = slideWindow(imagePyramid, 12, 128)

print(sublabels)