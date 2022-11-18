from Vision import *
from tensorflow import  keras



	

if __name__ == '__main__':
	vid1 = "lanes_clip.mp4"
	vid2 = "Road vid - Made with Clipchamp.mp4"
	path = vid2
	vid = cv2.VideoCapture(path)
	ScrollBar()
	crop_mask = np.zeros(shape=(500,500,3))
	while(True):
		ret, frame = vid.read()
		if not ret:
			vid = cv2.VideoCapture(path)
			continue

		frame  = imgResize(frame,500,500)

		values = Values()
		#values = [0.0 ,89.7 ,0.0 ,161.6, 201.1, 255.0]
		values = [0.0, 179.0, 0.0, 30.6, 151.5, 255.0]# white lane filter
		
		mask =  Mask(frame,values)
		
	
		masked = BITWISE_and(frame,mask)
		mask2 = np.zeros(masked.shape[:2], dtype="uint8") #Rectangular mask
		cv2.rectangle(mask2, (0, 250), (500, 500), 255, -1)
		cv2.imshow("Rectangular Mask", mask2)
		
		# cropped out
		masked = cv2.bitwise_and(masked, masked, mask=mask)

		gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
		 
		

		edges = cv2.Canny(image=gray, threshold1=100, threshold2=200) 
		img_blur = cv2.GaussianBlur(edges, (7,7), 0)
		sobely = cv2.Sobel(img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5).astype(np.uint8)
		lines = cv2.HoughLinesP(edges,1,np.pi/180,40,maxLineGap=100,minLineLength=100)
		
		Detection = frame.copy()
		if lines is not None:
			for line in lines:
				x1,y1,x2,y2 = line[0]
				cv2.line(Detection,(x1,y1),(x2,y2),(0,255,0),5)
				
		cv2.imshow('frame1',frame)
		cv2.imshow('frame2',Detection)
		cv2.imshow('frame3',mask)
		cv2.imshow('frame4',masked)
		
		
		
		

		if cv2.waitKey(1) &  0xFF == ord('q'):
			break
	vid.release()
	cv2.destroyAllWindows()