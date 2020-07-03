from flask import Flask, render_template, redirect, url_for, request, send_file, jsonify
from flask_socketio import SocketIO, emit
from gevent.pywsgi import WSGIServer
from gevent.monkey import patch_all
import requests
import logging
import sys
import argparse
import os
from processing import Processing
import json
import io
from io import StringIO, BytesIO
from PIL import Image
import base64
import cv2
import numpy as np
import random
import copy
from face_detection import FaceDetection
from face_recognition import FaceRecognition
import pickle
from sklearn.metrics.pairwise import cosine_similarity as cs
from datetime import datetime

class RunFaceID(object):
	def __init__(self):
		super(RunFaceID, self).__init__()
		self.face_detection = FaceDetection()
		self.face_recognition = FaceRecognition()
		# self.arr_embeddings = pickle.load(open("data_embeddings", "rb"))
		# self.labels = pickle.load(open("labels", "rb"))

	def predict_labels(self, embeddings, embeddings_source, labels_index, labels_name):
		dis_cs = cs(embeddings, embeddings_source)
		index_list = np.argmax(dis_cs, axis = -1)
		label_pred = []
		for i, index in enumerate(index_list):
			if dis_cs[i][index] > 0.6:
				label_index = labels_index[index]
				for i, (index_tmp, name_tmp) in enumerate(labels_name):
					if label_index == index_tmp:
						label_pred.append(labels_name[i])
			else :
				label_pred.append([-1, "unknown"])
		return label_pred

	def processing(self, images, count, embeddings_source, labels_index, labels_name, message_status):
		frame = copy.deepcopy(images)
		faces = self.face_detection.detect_faces(frame)
		if faces is None or len(faces) < 1:
			return None
		data = {}
		array_img = []
		labels = []
		for x,y,w,h in faces:
			if w > 0 and h > 0:
				img_crop = frame[y:y+h, x:x+w, :]
				array_img.append(img_crop)
				# labels.append("unknown")
		array_img = np.array(array_img)
		# data["labels"] = labels
		if count >= NUMBER_FRAME:
			array_embeddings = self.face_recognition.embedding_image(array_img)
			data["labels"] = self.predict_labels(array_embeddings, embeddings_source, labels_index, labels_name)
		data["bounding_boxs"] = faces
		return data

	def get_faces(self, images):
		faces = self.face_detection.detect_faces(images)
		return list(faces)

	def get_bb_embeddings(self, images):
		faces = self.get_faces(images)
		if len(faces) != 1:
			return None
		array_img = []
		data = {}
		for x, y, w, h in faces:
			if w > 0 and h > 0:
				img_crop = images[y:y+h, x:x+w, :]
				array_img.append(img_crop)
		embeddings = self.face_recognition.embedding_image(array_img)[0]
		data["bounding_box"] = json.dumps(faces[0].tolist())
		data['embeddings'] = json.dumps(embeddings.tolist())
		return data


NUMBER_FRAME = 12
global runfaceid
global count
global map_session, message, data_remark
map_session = {}
data_remark = {}
message = {
		"bbox" : [],
		"labels" : []
}

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

# exit()
count = 1
runfaceid = RunFaceID()

image = cv2.imread("3.png")
data = runfaceid.get_bb_embeddings(image)
cv2.imwrite("tmp.png", image)
with open("tmp.png", 'rb') as file:
	image_base64 = base64.b64encode(file.read())
data['studentID'] = 1
data['image'] = image_base64
class_process = Processing()
class_process.add_image_data(data)
exit()