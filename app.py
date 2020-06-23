from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO, emit
from gevent.pywsgi import WSGIServer
from gevent.monkey import patch_all
import requests
import logging
import sys
import argparse
import os
from processing import Processing


class_process = Processing()

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

parser = argparse.ArgumentParser()

# get information of student
@app.route( '/home/admin/themsv', methods = ['GET', 'POST'])
def home_themsv():
	if request.method == "POST":
		list_text = ["name", "msv", "date", "address", "email", "phone", "image"]
		data = {}
		for name in list_text:
			data[name] = request.form[name]
		return redirect(url_for('home_admin'))
	return render_template('ThemSV.html')


# get information of teacher
@app.route( '/home/admin/themgv', methods = ['GET', 'POST'])
def home_themgv():
	if request.method == "POST":
		list_text = ["name", "date", "address", "email", "phone", "username", "password"]
		data = {}
		for name in list_text:
			data[name] = request.form[name]
		# class_process.add_student()
		return redirect(url_for('home_admin'))
	return render_template('ThemGV.html')

@app.route( '/home/admin', methods = ['GET', 'POST'])
def home_admin():
	if request.method == 'POST':
		if request.form['submit_button'] == 'Thêm sinh viên':
			return redirect(url_for('home_themsv'))
		if request.form['submit_button'] == 'Thêm giảng viên':
			return redirect(url_for('home_themgv'))
	return render_template('admin.html')

# Function Login
@app.route( '/', methods = ['GET', 'POST'])
def home():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		status = class_process.check_login(username, password)
		if status == 'admin':
			return redirect(url_for('home_admin'))
		if status == 'giaovien':
			return redirect(url_for('home_giaovien'))	
	return render_template('login.html')


@app.route( '/home/giaovien/diemdanh', methods = ['GET', 'POST'])
def home_giaovien_diemdanh():
	if request.method == 'POST':
		#doing st;
		a = 1
	return render_template('DiemDanh.html')

@app.route( '/home/giaovien', methods = ['GET', 'POST'])
def home_giaovien():
	if request.method == 'POST':
		if request.form['button_submit'] == 'Điểm danh':
			return redirect(url_for('home_giaovien_diemdanh'))
		else :
			if request.form['button_submit'] == 'Xuất kết quả':
				print ("download ket qua")
	return render_template('GiangVien.html')


if __name__ == '__main__':
	socketio.run(app, port=7320, host = "127.0.0.1" ,debug = True)
