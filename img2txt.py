# Author M.R.H
# this may not be the most effecient way to do this,
# but i needed a way to get these text images for a class

import sys
from PIL import Image
import numpy as np

# minimum arguments required to convert an image
if(len(sys.argv) < 3):
	print("Need arguments:\n1) image file\n2) threshold\nAnd optional binary / pretty / invert flags")
	print("eg: python3 image1.jpg 200 [ -b -p -i (optional) ]")
	exit()

binary = False
pretty = False
invert = False
threshold = int(sys.argv[2])
img = Image.open(sys.argv[1]).convert('L')	# convert image to greyscale
col, row = img.size

if(len(sys.argv) == 6):
	binary = True
	pretty = True
	invert = True
else:
	for i in range(3, len(sys.argv)):
		if(sys.argv[i] == "-b"):
			binary = True
		if(sys.argv[i] == "-p"):
			pretty = True
		if(sys.argv[i] == "-i"):
			invert = True

# convert PIL.image to 2D np.array or greyscale values
x = np.asarray(img.getdata(), dtype=np.int).reshape((img.size[1], img.size[0]))

minVal = 0
maxVal = 1

if threshold > 254:
	minVal = 255
if not binary:
	maxVal = 0

st = sys.argv[1].split(".")[0] + "_Converted.txt"
f = open(st, "w")
st = ""

for i in range(row):
	for j in range(col):

		cur_pixel = None

		if invert and x[i][j] >= threshold:
			cur_pixel = x[i][j]

		if not invert and x[i][j] <= threshold:
			cur_pixel = x[i][j]

		if not binary and cur_pixel is not None:

			if minVal > cur_pixel:
				minVal = cur_pixel

			if maxVal < cur_pixel:
				maxVal = cur_pixel

			st += str(cur_pixel) +" "

		else:
			if cur_pixel is not None and cur_pixel > 0:
				st += "1 "
			else:
				if pretty:
					st += "· "
				else:
					st += "0 "

	st += "\n"

# image header (row, col, min_val_in_img, max_val_in_img)
f.write(str(row) +" "+ str(col) +" "+ str(minVal) +" "+ str(maxVal))

# write processed data to file
f.write("\n"+st)

f.close()
