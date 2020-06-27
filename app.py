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

class RunFaceID(object):
	def __init__(self):
		super(RunFaceID, self).__init__()
		self.face_detection = FaceDetection()
		self.face_recognition = FaceRecognition()
		self.arr_embeddings = pickle.load(open("data_embeddings", "rb"))
		self.labels = pickle.load(open("labels", "rb"))

	def predict_labels(self, embeddings):
		dis_cs = cs(embeddings, self.arr_embeddings)
		index_list = np.argmax(dis_cs, axis = -1)
		label_pred = []
		for i, index in enumerate(index_list):
			if dis_cs[i][index] > 0.6:
				label_pred.append(self.labels[index])
			else :
				label_pred.append("unknown")
		return label_pred

	def processing(self, images, count):
		frame = copy.deepcopy(images)
		faces = self.face_detection.detect_faces(frame)
		if faces is None or len(faces) < 1:
			return None
		data = {}
		array_img = []
		labels = []
		for x,y,w,h in faces:
			if w > 0 and h > 0:
				img_crop = img_crop = frame[y:y+h, x:x+w, :]
				array_img.append(img_crop)
				labels.append("unknown")
		array_img = np.array(array_img)
		# data["labels"] = labels
		if count >= 5:
			array_embeddings = self.face_recognition.embedding_image(array_img)
			data["labels"] = self.predict_labels(array_embeddings)
		data["bounding_boxs"] = faces
		return data

global runfaceid
global count
global map_session, message
map_session = {}
message = {
		"bbox" : [],
		"labels" : []
}
count = 1
runfaceid = RunFaceID()

class_process = Processing()

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

parser = argparse.ArgumentParser()

# get information of student
@app.route( '/home/admin/themsv', methods = ['GET', 'POST'])
def home_themsv():
	global map_session
	if request.method == "POST":
		session_id = request.form['session_id']
		list_text = ["name", "msv", "date", "address", "email", "phone", "image"]
		data = {}
		for name in list_text:
			data[name] = request.form[name]
		return redirect(url_for('home_admin', session_id = session_id))
	session_id = request.args.get('session_id')
	if session_id is None or map_session.get(session_id) != 'admin':
		return "NOT ACCESS"
	return render_template('ThemSV.html', session_id = session_id)


# get information of teacher
@app.route( '/home/admin/themgv', methods = ['GET', 'POST'])
def home_themgv():
	global map_session
	if request.method == "POST":
		session_id = request.form['session_id']
		list_text = ["name", "date", "address", "email", "phone", "username", "password"]
		data = {}
		for name in list_text:
			data[name] = request.form[name]
		# class_process.add_student()
		return redirect(url_for('home_admin', session_id = session_id))
	session_id = request.args.get('session_id')
	if session_id is None or map_session.get(session_id) != 'admin':
		return "NOT ACCESS"
	return render_template('ThemGV.html' , session_id = session_id)



# get information of teacher to fix or delete
@app.route( '/home/admin/thongtingiaovien', methods = ['GET', 'POST'])
def home_get_thong_tin_giao_vien():
	global map_session
	if request.method == "POST":
		list_text = ["name", "date", "address", "email", "phone", "username", "password"]
		data = {}
		for name in list_text:
			data[name] = request.form[name]
	session_id = request.args.get('session_id')
	if session_id is None or map_session.get(session_id) != 'admin':
		return "NOT ACCESS"
	return render_template('Sua-XoaGV.html' , session_id = session_id)


# get information of student to fix or delete
@app.route( '/home/admin/thongtinsinhvien', methods = ['GET', 'POST'])
def home_get_thong_tin_sinh_vien():
	global map_session
	if request.method == "POST":
		list_text = ["name", "msv", "date", "address", "email", "phone", "image"]
		data = {}
		for name in list_text:
			data[name] = request.form[name]
	session_id = request.args.get('session_id')
	if session_id is None or map_session.get(session_id) != 'admin':
		return "NOT ACCESS"
	return render_template('Sua-XoaSV.html', session_id = session_id)


# Giao diện chính quản lý admin
@app.route( '/home/admin', methods = ['GET', 'POST'])
def home_admin():
	global map_session
	if request.method == 'POST':
		session_id = request.form['session_id']
		if request.form['submit_button'] == 'Thêm sinh viên':
			return redirect(url_for('home_themsv', session_id = session_id))
		if request.form['submit_button'] in ['Xóa sinh viên', 'Sửa thông tin sinh viên']:
			return redirect(url_for('home_get_thong_tin_sinh_vien', session_id = session_id))
		if request.form['submit_button'] == 'Thêm giảng viên':
			return redirect(url_for('home_themgv', session_id = session_id))
		if request.form['submit_button'] in ['Xóa giảng viên', 'Sửa thông tin giảng viên']:
			return redirect(url_for('home_get_thong_tin_giao_vien', session_id = session_id))
	session_id = request.args.get('session_id')
	if session_id is None or map_session.get(session_id) != 'admin':
		return "NOT ACCESS"
	return render_template('admin.html', session_id = session_id)

# Function Login
@app.route( '/', methods = ['GET', 'POST'])
def home():
	global map_session
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		status = class_process.check_login(username, password)
		session_id = request.form['session_id']
		if status == 'admin':
			map_session[session_id] = 'admin'
			return redirect(url_for('home_admin', session_id = session_id))
		if status == 'giaovien':
			map_session[session_id] = 'giaovien'
			return redirect(url_for('home_giaovien', session_id = session_id))
		return render_template('login.html', data = "Tài khoản mật khẩu không đúng", session_id = session_id)
	session_id = str(random.randint(1, 100000000))
	return render_template('login.html', data = "", session_id = session_id)


# Giao diện bắt đầu điểm danh
@app.route( '/home/giaovien/diemdanh/start', methods = ['GET', 'POST'])
def home_giaovien_diemdanh_start():
	global map_session
	if request.method == 'POST':
		return redirect(url_for('home_giaovien'))
	return render_template('index.html')

# Giao diện tìm lớp điểm danh
@app.route( '/home/giaovien/diemdanh', methods = ['GET', 'POST'])
def home_giaovien_diemdanh():
	global map_session
	if request.method == 'POST':
		return redirect(url_for('home_giaovien_diemdanh_start'))
	return render_template('DiemDanh.html')


# Giao diện tìm lớp xuat file
@app.route( '/home/giaovien/tim_lop', methods = ['GET', 'POST'])
def home_giaovien_tim_lop():
	global map_session
	if request.method == 'POST':
		return redirect(url_for('downloadFile'))
	return render_template('Tim_Nhom.html')


# Download file
@app.route('/download')
def downloadFile():
	global map_session
	path = "README.md"
	return send_file(path, as_attachment=True)

# Giao diện giao viên
@app.route( '/home/giaovien', methods = ['GET', 'POST'])
def home_giaovien():
	global map_session
	if request.method == 'POST':
		if request.form['button_submit'] == 'Điểm danh':
			return redirect(url_for('home_giaovien_diemdanh'))
		else :
			if request.form['button_submit'] == 'Xuất kết quả':
				return redirect(url_for('home_giaovien_tim_lop'))
	return render_template('GiangVien.html')

# Function xử lý video
@socketio.on('process_video')
def process_video(data_image):
	global runfaceid, count, message
	count += 1
	data_image = data_image.replace('data:' + 'image/png' + ';base64,', '')
	# decode and convert into image
	imgdata = base64.b64decode(data_image)
	filename = 'hung.png'
	with open(filename, "wb") as file:
		file.write(imgdata)
	img = cv2.imread(filename)
	# image = Image.open(io.BytesIO(imgdata))
	# img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BRG)
	# img = cv2.resize(img, (160, 160))
	# img = np.array(image)
	if img.shape[-1] == 3:
		# message = {
		# 		"bbox" : [],
		# 		"labels" : []
		# }
		data = runfaceid.processing(img, count)
		if data is not None:
			for index, (x, y, w, h) in enumerate(data.get('bounding_boxs')):
				message["bbox"] = []
				message["labels"] = []
				message["bbox"].append([int(x), int(y), int(w), int(h)])
				message["labels"].append(data.get('labels')[index])
				emit('response_back', message)
				# img_source = cv2.rectangle(img_source, (int(x), int(y)), (int(x)+int(w), int(y)+int(h)), (0, 255, 0), 2)
				# cv2.imwrite("hung.png", img_source[:,:150, :])
				# print (img_source[:,:150, :].shape)
				# exit()
				# # img_source = img_source[:, :int(img_source.shape[0]/2)]
				# # img_source = cv2.resize(img_source, (320, 320))
				# while True:
				# 	cv2.imshow("image", img_source)
				# 	# print (f"img_source = {img_source.shape}")
				# 	# exit()
				# 	if cv2.waitKey(1) & 0xff == ord('q'):
				# 		break
				# cv2.destroyAllWindows() 
			if count >= 5:
				count = 1
		else :
			if count < 5:
				emit('response_back', message)
			else :
				message["bbox"] = []
				message["labels"] = []
				emit('response_back', message)


if __name__ == '__main__':
	socketio.run(app, port=7320, host = "127.0.0.1" ,debug = True)
