import cv2
import numpy as np
import time
import glob
import os
start_time=time.time()
cap = cv2.VideoCapture("1.mp4")
s=1
#segmentation
count=0
s, first_frame = cap.read()
while s:
	s, frame = cap.read()
	cv2.imwrite("orig_frame%d.jpg" % count, frame)
	count += 1
count-=2
print("Video segmented to ",count," frames.")
#difference
first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
first_gray = cv2.GaussianBlur(first_gray, (5, 5), 0)
i=0

while i<=count:
	img=cv2.imread("orig_frame%d.jpg" %i, -1)
	try:
		gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	except:
	   cap.release()
	   cv2.destroyAllWindows()
	gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

	difference = cv2.absdiff(first_gray, gray_frame)
	_, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
	cv2.imwrite("diff_frame%d.jpg" % i, difference)
	i=i+1
print("Generated difference frames.")
#merging
i=0
img_array = []
for filename in sorted(glob.glob('D:/cuda/diff_frame*.jpg') , key=os.path.getmtime):
	img = cv2.imread(filename)
	height, width, layers = img.shape
	size = (width,height)
	img_array.append(img)
out = cv2.VideoWriter('project.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 15, size)
for i in range(len(img_array)):
    out.write(img_array[i])

out.release()	
# while i<=count:
# 	img=cv2.imread("diff_frame%d.jpg" %i, -1)
# 	try:




# 			fourcc = cv2.VideoWriter_fourcc(*"mp4v")
# 			out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (640,480))
# 			#cv2.namedWindow( "Output",cv2.WINDOW_NORMAL)
# 			#cv2.imshow('Output',img)
# 	except:
# 			cap.release()
# 			cv2.destroyAllWindows()

	# key=cv2.waitKey(60)
	# if key == 27:
	# 	break
	# i=i+1
print ("Process Complete after %s seconds"%(time.time()-start_time))

