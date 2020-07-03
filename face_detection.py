import cv2
import os
import sys
import numpy as np
import time
import detect_face
import tensorflow as tf
import configure

class FaceDetection(object):
	"""docstring for FaceDetection"""
	def __init__(self):
		super(FaceDetection, self).__init__()
		self.model_detect = self.load_model() 
		# print (self.model_detect.minNeighbors)

	def load_model(self, filename = "model_opencv/haarcascades/haarcascade_frontalface_default.xml"):
		model = cv2.CascadeClassifier(filename)
		return model

	def detect_faces(self, image, scaleFactor = 1.3, minNeighbors=5):
	    img_copy = np.copy(image)
	    #convert the test image to gray image as opencv face detector expects gray images
	    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
	    #let's detect multiscale (some images may be closer to camera than others) images
	    faces = self.model_detect.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors = minNeighbors)
	    return faces

	def draw_faces_image(self, image, scaleFactor = 1.3):
		# get bounding box for face detection
		faces = self.detect_faces(image, scaleFactor)

		#go over list of faces and draw them as rectangles on original colored img
		for (x, y, w, h) in faces:
			cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
		return image


# class FaceDetection(object):
# 	def __init__(self):
# 		super(FaceDetection, self).__init__()
# 		self.pnet, self.rnet, self.onet = self.load_data()
# 		self.detect_minsize = 40
# 		self.detect_threshold = [ 0.6, 0.7, 0.7 ]
# 		self.detect_factor = 0.709
# 		self.start_model()

# 	def load_data(self):
# 		os.environ["CUDA_VISIBLE_DEVICES"]="-1"
# 		config = tf.ConfigProto()
# 		config.gpu_options.allow_growth = True
# 		sess = tf.Session(config=config)
# 		pnet, rnet, onet = detect_face.create_mtcnn(sess, configure.MODEL_DETECT)
# 		return pnet, rnet, onet

# 	def start_model(self):
# 		inputs = np.ones((100, 100, 3))
# 		self.detect_faces(inputs)

# 	def detect_faces(self, frame):
# 		list_bouding_box = []
# 		total_box, point = detect_face.detect_face(frame, self.detect_minsize, self.pnet, self.rnet, self.onet, 
# 								self.detect_threshold, self.detect_factor)
# 		for box in total_box:
# 			x = (int)(box[0])
# 			y = (int)(box[1])
# 			w = (int)(box[2] - box[0])
# 			h = (int)(box[3] - box[1])
# 			if w != 0 and h != 0:
# 				list_bouding_box.append((x,y,w,h))
# 		return list_bouding_box



# cap = cv2.VideoCapture(0)
# face_detect = FaceDetection()
# i = 0

# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     faces = face_detect.detect_faces(frame)
#     if len(faces) > 0:
#     	cv2.imwrite(str(i) + ".png", frame)
#     	i += 1
#     	if i == 5:
#     		break

#     # Display the resulting frame
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()