import os
from connection import DatabaseConnection


class ConnectionDB(object):
	"""docstring for ConnectionDB"""
	def __init__(self):
		super(ConnectionDB, self).__init__()

	def get_username_password(self):
		data = None
		return data
	
	def check_login(self, username, password):
		position = 'giaovien'
		return position
	
		

class Processing(object):
	"""docstring for Processing"""
	def __init__(self):
		super(Processing).__init__()
		self.dbcnx = DatabaseConnection()

	def check_login(self, username, password):
		return self.dbcnx.get_user_role(username, password)

		if username == "hungdv" and password == '123456':
			return 'admin'
		if username == "hungptit" and password == '123456':
			return 'giaovien'
		return None
	
	def add_teacher(self, data):
		self.dbcnx.add_teacher(data)
	
	def add_student(self, data):
		self.dbcnx.add_student(data)
	
	def check_room_existence(self, subject, room):
		return self.dbcnx.contain_class(subject, room)

	# def add_student(self, data):

