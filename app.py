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
count = 1
runfaceid = RunFaceID()

# image = cv2.imread("4.png")
# data = runfaceid.get_bb_embeddings(image)
# cv2.imwrite("tmp.png", image)
# with open("tmp.png", 'rb') as file:
# 	image_base64 = base64.b64encode(file.read())
# data['studentID'] = 1
# data['image'] = image_base64
# class_process = Processing()
# class_process.add_image_data(data)
# exit()

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
		if session_id is None or map_session.get(session_id).get('roleName') != 'admin':
			return "NOT ACCESS"
		list_text = ['personName','studentCode','gradeName', 'doB', 'gender', 'email', 'contactMobile', 'address', 'image']
		data = {}
		for name in list_text:
			data[name] = request.form.get(name)
		data['gender'] = 1
		data['studentCode'] = data['studentCode'].upper()
		data['gradeName'] = data['gradeName'].upper()
		class_process.add_student(data)
		return redirect(url_for('home_admin', session_id = session_id))
	session_id = request.args.get('session_id')
	if session_id is None or map_session.get(session_id).get('roleName') != 'admin':
		return "NOT ACCESS"
	return render_template('ThemSV.html', session_id = session_id)


# get information of teacher
@app.route( '/home/admin/themgv', methods = ['GET', 'POST'])
def home_themgv():
	global map_session
	if request.method == "POST":
		session_id = request.form['session_id']
		if session_id is None or map_session.get(session_id).get('roleName') != 'admin':
			return "NOT ACCESS"
		list_text = ['personName','specialize','userName', 'password','doB', 'gender', 'email', 'contactMobile', 'address', 'roleName']
		data = {}
		for name in list_text:
			data[name] = request.form.get(name)
		data['roleName'] = 'giaovien'
		data['gender'] = 0
		class_process.add_teacher(data)
		return redirect(url_for('home_admin', session_id = session_id))
	session_id = request.args.get('session_id')
	if session_id is None or map_session.get(session_id).get('roleName') != 'admin':
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
	if session_id is None or map_session.get(session_id).get('roleName') != 'admin':
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
	if session_id is None or map_session.get(session_id).get('roleName') != 'admin':
		return "NOT ACCESS"
	return render_template('Sua-XoaSV.html', session_id = session_id)


# Giao diện chính quản lý admin
@app.route( '/home/admin', methods = ['GET', 'POST'])
def home_admin():
	global map_session
	if request.method == 'POST':
		session_id = request.form['session_id']
		if session_id is None or map_session.get(session_id).get('roleName') != 'admin':
			return "NOT ACCESS"
		if request.form['submit_button'] == 'Thêm sinh viên':
			return redirect(url_for('home_themsv', session_id = session_id))
		if request.form['submit_button'] in ['Xóa sinh viên', 'Sửa thông tin sinh viên']:
			return redirect(url_for('home_get_thong_tin_sinh_vien', session_id = session_id))
		if request.form['submit_button'] == 'Thêm giảng viên':
			return redirect(url_for('home_themgv', session_id = session_id))
		if request.form['submit_button'] in ['Xóa giảng viên', 'Sửa thông tin giảng viên']:
			return redirect(url_for('home_get_thong_tin_giao_vien', session_id = session_id))
	session_id = request.args.get('session_id')
	if session_id is None or map_session.get(session_id).get('roleName') != 'admin':
		return "NOT ACCESS"
	return render_template('admin.html', session_id = session_id)

# Function Login
@app.route( '/', methods = ['GET', 'POST'])
def home():
	global map_session, class_process
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		data = class_process.check_login(username, password)
		if data is None:
			status = None
		else :
			status = data.get('roleName')
		session_id = request.form['session_id']
		if status == 'admin':
			map_session[session_id] = data
			return redirect(url_for('home_admin', session_id = session_id))
		if status == 'giaovien':
			memberID = data.get('memberID')
			teacherID = class_process.get_class_session_from_teacher(memberID)
			data['teacherID'] = teacherID
			map_session[session_id] = data
			return redirect(url_for('home_giaovien', session_id = session_id))
		return render_template('login.html', data = "Tài khoản mật khẩu không đúng", session_id = session_id)
	session_id = str(random.randint(1, 100000000))
	return render_template('login.html', data = "", session_id = session_id)


# Giao diện giao viên
@app.route( '/home/giaovien', methods = ['GET', 'POST'])
def home_giaovien():
	global map_session, class_process, data_remark
	if request.method == 'POST':
		session_id = request.form['session_id']
		if session_id is None or map_session.get(session_id).get('roleName') != 'giaovien':
			return "NOT ACCESS"
		if request.form['button_submit'] == 'Điểm danh':
			return redirect(url_for('home_giaovien_diemdanh_thaythe', session_id = session_id))
			# return redirect(url_for('home_giaovien_diemdanh', session_id = session_id))
		else :
			if request.form['button_submit'] == 'Xuất kết quả':
				return redirect(url_for('home_giaovien_xuatketqua_sections', session_id = session_id))
	session_id = request.args.get('session_id')
	if session_id is None or map_session.get(session_id).get('roleName') != 'giaovien':
		return "NOT ACCESS"
	return render_template('GiangVien.html', session_id = session_id)



# Giao diện xuất kết quả giao viên
@app.route( '/home/giaovien/xuatketquasections', methods = ['GET', 'POST'])
def home_giaovien_xuatketqua_sections():
	global map_session, class_process, data_remark
	if request.method == 'POST':
		session_id = request.form.get('session_id')
		if session_id is None or map_session.get(session_id).get('roleName') != 'giaovien':
			return "NOT ACCESS"
		name_button = None
		for name in request.form:
			if name!="session_id":
				groupID = name
				name_button = request.form.get(groupID)
		if name_button == "Xuất kết quả":
			filename = class_process.write_result_csv_group(groupID)
			return redirect(url_for('downloadFile', session_id = session_id, filename = filename))
	session_id = request.args.get('session_id')
	teacherID = map_session.get(session_id).get('teacherID')
	data_group = class_process.get_group_from_teachID(teacherID)
	if session_id is None or map_session.get(session_id).get('roleName') != 'giaovien':
		return "NOT ACCESS"
	return render_template('giaodiensections.html', session_id = session_id, data_group = data_group)


@app.route( '/home/giangvien/sections', methods = ['GET', 'POST'])
def home_giaovien_diemdanh_thaythe():
	global map_session, data_remark, class_process
	if request.method == 'POST':
		session_id = request.form.get('session_id')
		if session_id is None or map_session.get(session_id).get('roleName') != 'giaovien':
			return "NOT ACCESS"
		name_button = None
		for name in request.form:
			if name!="session_id":
				sectionID = name
				name_button = request.form.get(sectionID)
		if name_button == "Điểm danh":
			data_remark = {}
			data_remark[session_id] = {}
			list_studentID = class_process.get_students_from_class_session(sectionID)
			data_remark[session_id]['inform_student'] = class_process.get_information_students(list_studentID['studentID'])
			data_remark[session_id]['sectionID'] = sectionID
			timestamp = int(datetime.timestamp(datetime.now()))
			data_remark[session_id]['startedTime'] = str(datetime.fromtimestamp(timestamp))
			data_embeddings = class_process.get_embeddings_students(list_studentID['studentID'])
			embeddings = []
			labels_index = []
			for label_index, embedding in data_embeddings:
				embeddings.append(np.array(embedding))
				labels_index.append(label_index)
			data_remark[session_id]['embeddings'] = embeddings
			data_remark[session_id]['labels_index'] = labels_index
			data_remark[session_id]['remark'] = {}
			return redirect(url_for('home_giaovien_diemdanh_start', session_id = session_id))
		if name_button == "Xem kết quả":
			filename = class_process.write_result_csv_section(sectionID)
			return redirect(url_for('downloadFile', session_id = session_id, filename = filename))

	session_id = request.args.get('session_id')
	teacherID = map_session.get(session_id).get('teacherID')
	data_table = class_process.get_information_sections(teacherID)
	if session_id is None or map_session.get(session_id).get('roleName') != 'giaovien':
		return "NOT ACCESS"
	return render_template('giaodiendiemdanh.html', session_id = session_id, data_table = data_table)


# Giao diện bắt đầu điểm danh
@app.route( '/home/giaovien/diemdanh/start', methods = ['GET', 'POST'])
def home_giaovien_diemdanh_start():
	global map_session, data_remark, class_process
	if request.method == 'POST':
		session_id = request.form.get('session_id')
		if session_id is None or map_session.get(session_id).get('roleName') != 'giaovien':
			return "NOT ACCESS"
		timestamp = int(datetime.timestamp(datetime.now()))
		data_remark[session_id]['endedTime'] = str(datetime.fromtimestamp(timestamp))
		logs = data_remark.get(session_id).get('remark')
		data = {}
		data['sectionID'] = data_remark[session_id]['sectionID']
		data['startedTime'] = data_remark[session_id]['startedTime']
		data['endedTime'] = data_remark[session_id]['endedTime']
		data['remark'] = []
		for studentID, name_student in data_remark[session_id]['inform_student']:
			if data_remark[session_id]['remark'].get(studentID) is None:
				data['remark'].append([studentID, 0])
			else :
				if data_remark[session_id]['remark'].get(studentID) == 1:
					data['remark'].append([studentID, 1])
				else :
					print ("----------error get student--------------------")
					exit()
		class_process.add_remark(data)
		return redirect(url_for('home_giaovien', session_id = session_id))
	session_id = request.args.get('session_id')
	if session_id is None or map_session.get(session_id).get('roleName') != 'giaovien':
		return "NOT ACCESS"
	return render_template('index.html', session_id = session_id)

# Download file
@app.route('/download')
def downloadFile():
	global map_session
	session_id = request.args.get('session_id')
	if session_id is None or map_session.get(session_id).get('roleName') != 'giaovien':
		return "NOT ACCESS"
	filename = request.args.get('filename')
	return send_file(filename, as_attachment=True)

# # Giao diện tìm lớp điểm danh
# @app.route( '/home/giaovien/diemdanh', methods = ['GET', 'POST'])
# def home_giaovien_diemdanh():
# 	global map_session, data_remark, class_process
# 	if request.method == 'POST':
# 		session_id = request.form['session_id']
# 		if session_id is None or map_session.get(session_id).get('roleName') != 'giaovien':
# 			return "NOT ACCESS"
# 		data_remark = {}
# 		data_remark[session_id] = {}
# 		sectionID = 5
# 		list_studentID = class_process.get_students_from_class_session(sectionID)
# 		data_remark[session_id]['inform_student'] = class_process.get_information_students(list_studentID['studentID'])
# 		data_remark[session_id]['sectionID'] = sectionID
# 		timestamp = int(datetime.timestamp(datetime.now()))
# 		data_remark[session_id]['startedTime'] = str(datetime.fromtimestamp(timestamp))
# 		data_embeddings = class_process.get_embeddings_students(list_studentID['studentID'])
# 		embeddings = []
# 		labels_index = []
# 		for label_index, embedding in data_embeddings:
# 			embeddings.append(np.array(embedding))
# 			labels_index.append(label_index)
# 		data_remark[session_id]['embeddings'] = embeddings
# 		data_remark[session_id]['labels_index'] = labels_index
# 		data_remark[session_id]['remark'] = {}
# 		return redirect(url_for('home_giaovien_diemdanh_start', session_id = session_id))
# 	session_id = request.args.get('session_id')
# 	if session_id is None or map_session.get(session_id).get('roleName') != 'giaovien':
# 		return "NOT ACCESS"
# 	return render_template('DiemDanh.html', session_id = session_id)

# # Giao diện tìm lớp xuat file
# @app.route( '/home/giaovien/tim_lop', methods = ['GET', 'POST'])
# def home_giaovien_tim_lop():
# 	global map_session
# 	if request.method == 'POST':
# 		session_id = request.form.get('session_id')
# 		if session_id is None or map_session.get(session_id).get('roleName') != 'giaovien':
# 			return "NOT ACCESS"
# 		return redirect(url_for('downloadFile', session_id = session_id))
# 	session_id = request.args.get('session_id')
# 	if session_id is None or map_session.get(session_id).get('roleName') != 'giaovien':
# 		return "NOT ACCESS"
# 	return render_template('Tim_Nhom.html', session_id = session_id)

# Function xử lý video
@socketio.on('process_video')
def process_video(data_image_source):
	global runfaceid, count, message, data_remark
	session_id = data_image_source.get('session_id')
	data_image = data_image_source['image'].replace('data:' + 'image/png' + ';base64,', '')
	# decode and convert into image
	imgdata = base64.b64decode(data_image)
	filename = 'hung.png'
	with open(filename, "wb") as file:
		file.write(imgdata)
	img = cv2.imread(filename)
	count += 1
	# image = Image.open(io.BytesIO(imgdata))
	# img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BRG)
	img = cv2.resize(img, (500, 375))
	# img = np.array(image)
	if img.shape[-1] == 3:
		embeddings_source = data_remark.get(session_id).get('embeddings')
		labels_index = data_remark.get(session_id).get('labels_index')
		labels_name = data_remark.get(session_id).get('inform_student')
		if count >= NUMBER_FRAME:
			data = runfaceid.processing(img, count, embeddings_source, labels_index, labels_name, message)
		else :
			data = None
		if data is not None and count >= NUMBER_FRAME:
			message["bbox"] = []
			message["labels"] = []
			for index, (x, y, w, h) in enumerate(data.get('bounding_boxs')):
				message["bbox"].append([int(x), int(y), int(w), int(h)])
				if count >= NUMBER_FRAME:
					message["labels"].append(data.get('labels')[index][-1])
					studentID = data.get('labels')[index][0]
					if studentID != -1:
						data_remark[session_id]['remark'][studentID] = 1
				else :
					message["labels"].append("unknown")
				emit('response_back', message)
			if count >= NUMBER_FRAME:
				count = 1
		else :
			if count < 3:
				emit('response_back', message)
			else :
				message["bbox"] = []
				message["labels"] = []
				emit('response_back', message)


if __name__ == '__main__':
	socketio.run(app, port=7320, host = "127.0.0.1" ,debug = True)
