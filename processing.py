import os


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

	def check_login(self, username, password):
		if username == "hungdv" and password == '123456':
			return 'admin'
		if username == "hungptit" and password == '123456':
			return 'giaovien'
		return None
	# def add_student(self, data):

