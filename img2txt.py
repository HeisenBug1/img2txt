# convert and image to text to use with our CSCI-381 (Computer Vision) projects

import sys
from PIL import Image
import numpy as np

if(len(sys.argv) < 3):
	print("Need arguments:\n1) image file\n2) threshold\nAnd optional binary flag and/or pretty flag")
	print("eg: python3 image1.jpg 200 [ -b -p (optional) ]")
	exit()

binary = False
pretty = False
threshold = int(sys.argv[2])
img = Image.open(sys.argv[1]).convert('L')
col, row = img.size

if(len(sys.argv) == 5):
	binary = True
	pretty = True
else:
	if(sys.argv[3] == "-b"):
		binary = True
	if(sys.argv[3] == "-p"):
		pretty = True

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
		if x[i][j] <= threshold:
			if not binary:
				if minVal > x[i][j]:
					minVal = x[i][j]
				if maxVal < x[i][j]:
					maxVal = x[i][j]
				st += str(x[i][j]) +" "

			else:
				if x[i][j] > 0:
					st += "1 "
				else:
					if pretty:
						st += ". "
					else:
						st += "0 "
		else:
			if pretty:
				st += ". "
			else:
				st += "0 "

	st += "\n"

f.write(str(row) +" "+ str(col) +" "+ str(minVal) +" "+ str(maxVal))
f.write("\n"+st)

f.close()