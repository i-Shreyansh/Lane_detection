from tkinter import *
from Vision import *
import os

from PIL import Image
from PIL import ImageTk as imgtk

def start_clicked():

	vid1 = "lanes_clip.mp4"
	vid2 = "Road vid - Made with Clipchamp.mp4"
	path = vid2

	global vid
	vid = cv2.VideoCapture(path)
	
	h,w = 500,500
	# ScrollBar()
	crop_mask = np.zeros(shape=(h,w,3))

	l1=Label(TK_frame)
	l1.pack()
	while(True):
		ret, frame = vid.read()
		
		if not ret:
			img=crop_mask
		
			img= Image.fromarray(img)
			img= imgtk.PhotoImage(img)
			l1['image']=img
			window.update()

		frame  = imgResize(frame,h,w)

		# values = Values()
		#values = [0.0 ,89.7 ,0.0 ,161.6, 201.1, 255.0]
		values = [0.0, 179.0, 0.0, 30.6, 151.5, 255.0]# white lane filter
		
		mask =  Mask(frame,values)
		

		masked = BITWISE_and(frame,mask)
		mask2 = np.zeros(masked.shape[:2], dtype="uint8") #Rectangular mask
		cv2.rectangle(mask2, (0, h//2), (w, h), 255, -1)
		# cv2.imshow("Rectangular Mask", mask2)


		# cv2.imshow("Rectangular Mask", mask2)

		# cropped out
		masked = cv2.bitwise_and(masked, masked, mask=mask2)

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
		

		

		# cv2.imshow('frame1',frame)
		# cv2.imshow('frame3',mask)
		# cv2.imshow('Lane detection',masked)
		#cv2.imshow('Lane detection',Detection)

		img=Detection
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img= Image.fromarray(img)
		img= imgtk.PhotoImage(img)
		l1['image']=img
		window.update()

def Stop_clicked():
	print("Stop")
	vid.release()


def exit_clicked(): #exit
  
    os._exit(0)
window = Tk()

window.geometry("1410x810")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 810,
    width = 1410,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    714.5, 405.0,
    image=background_img)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = Stop_clicked,
    relief = "flat")

b0.place(
    x = 790, y = 690,
    width = 164,
    height = 45)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = start_clicked,
    relief = "flat")

b1.place(
    x = 441, y = 692,
    width = 166,
    height = 45)

img2 = PhotoImage(file = f"img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = exit_clicked,
    relief = "flat")

b2.place(
    x = 1060, y = 139,
    width = 164,
    height = 45)

TK_frame=Frame(window)
TK_frame.pack()
TK_frame.place(x=415,y=197, height=400, width=560)
window.resizable(False, False)
window.mainloop()
