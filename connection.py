import os
import mysql.connector as mysql_db
import cv2
import base64
import json
import numpy as np

class DatabaseConnection(object):
	"""docstring for DatabaseConnection"""
	def __init__(self, host = "localhost", username = "root", password = "",
				db = "pthtttql", port = 3306):
		super(DatabaseConnection, self).__init__()
		self.connect = mysql_db.connect(host=host, username=username,
                                        password=password,
                                        db=db,
                                        port=port)
		self.connect.autocommit = True

	def processing_video(self, path_video, data):
		self.connect.ping(reconnect=True)
		id_video = self.insert_inform_video(path_video)
		for images, array_boxs, array_embeddings in data:
			id_image = self.insert_inform_image_from_video(int(id_video), images)
			for j, bounding_box in enumerate(array_boxs):
				embeddings = array_embeddings[j].tolist()
				self.insert_inform_meta_data_image(id_image, bounding_box, embeddings)

	def insert_inform_video(self, path_video):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "INSERT INTO video (path_video) VALUES (%s)"
		val = (path_video, )
		mycursor.execute(sql, val)
		self.connect.commit()  
		id_video = mycursor.lastrowid
		return id_video

	def insert_inform_image_from_video(self, id_video, image):
		cv2.imwrite("1.png", image)
		with open("1.png", 'rb') as file:
			image = base64.b64encode(file.read())
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "INSERT INTO image (id_video, image) VALUES (%s, %s)"
		val = (id_video, image)
		mycursor.execute(sql, val)
		self.connect.commit()  
		id_image = mycursor.lastrowid
		return id_image

	def insert_inform_meta_data_image(self, id_image, bounding_box, embeddings):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "INSERT INTO meta_image (id_image, bounding_box, embeddings) VALUES (%s, %s, %s)"
		bounding_box = np.array(bounding_box).tolist()
		bounding_box = json.dumps(bounding_box)
		embeddings = json.dumps(embeddings)
		val = (id_image, bounding_box, embeddings)
		mycursor.execute(sql, val)
		self.connect.commit()

	def get_id_video(self, path_video):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT id FROM video WHERE path_video like %s"
		mycursor.execute(sql, [path_video])
		myresult = mycursor.fetchall()
		id_video = None
		for id_tmp in myresult:
			id_video = id_tmp
		return id_video

	def get_image_from_image(self):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT image FROM image"
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		for row in myresult:
			return base64.b64decode(row[0])

	def get_meta_image(self):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT id_image, bounding_box, embeddings FROM meta_image"
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		for id_images, bounding_box, embeddings in myresult:
			return json.loads(bounding_box), json.loads(embeddings)

	def get_meta_data(self):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT video.path_video, image.image, meta_image.bounding_box, meta_image.embeddings "
		sql += "FROM video, image, meta_image WHERE video.id = image.id_video AND image.id = meta_image.id_image"
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		embedings_source = []
		labels_source = []
		for path_video, image, bounding_box, embeddings in myresult:
			embedings_source.append(np.array(json.loads(embeddings)))
			labels_source.append(path_video)
		embedings_source = np.array(embedings_source)
		return embedings_source, labels_source
	
	def get_user_role(self, username, password):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT roleID FROM Member WHERE userName = %s AND password = %s"
		val = (username, password)
		mycursor.execute(sql, val)
		myresult = mycursor.fetchall()
		if len(myresult) == 0: return None
		if myresult[0][0] == 1: return 'giaovien'
		if myresult[0][0] == 2: return 'admin'

	def add_teacher(self, data):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "INSERT INTO People (personName, doB, gender, email, contactMobile, address) VALUES (%s, %s, 0, %s, %s, %s);"
		val = (data["name"], data["date"], data["email"], data["phone"], data["address"])
		mycursor.execute(sql, val)
		self.connect.commit()  
		sql = "INSERT INTO Member (userName, password, personID, roleID) VALUES (%s, %s, LAST_INSERT_ID(), 1);"
		val = (data["username"], data["password"])
		mycursor.execute(sql, val)
		self.connect.commit()
		id_image = mycursor.lastrowid
		return id_image

	def add_student(self, data):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "INSERT INTO People (personName, doB, gender, email, contactMobile, address) VALUES (%s, %s, 0, %s, %s, %s);"
		val = (data["name"], data["date"], data["email"], data["phone"], data["address"])
		mycursor.execute(sql, val)
		self.connect.commit()  
		sql = "INSERT INTO Student (personID, gradeID, studentCode) VALUES (LAST_INSERT_ID(), 1, %s);"
		val = (data["msv"], )
		mycursor.execute(sql, val)
		self.connect.commit()
		id_image = mycursor.lastrowid
		return id_image
		
	def contain_class(self, subject, room):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT * FROM ((ClassSection INNER JOIN ClassRoom ON ClassSection.roomID = ClassRoom.roomID) "
		sql += "INNER JOIN Subject ON ClassSection.subjectID = Subject.subjectID) "
		sql += "WHERE ClassRoom.roomCode = %s AND Subject.subjectCode = %s"
		val = (room, subject)
		mycursor.execute(sql, val)
		myresult = mycursor.fetchall()
		return len(myresult) > 0

# con = DatabaseConnection()
# embedings_source, labels_source = con.get_meta_data()
# print (labels_source)
# print (f"embedings_source = {embedings_source.shape}")

# id_video = 5
# with open("test_image/test.png", 'rb') as file:
# 	images = base64.b64encode(file.read())
# con.insert_inform_image_from_video(int(id_video), images)
# data = con.get_image_from_image()
# filename = "1.png"
# with open(filename, 'wb') as file:
# 	file.write(data)

# id_images = 7
# bounding_box = [10, 11, 110, 110]
# bounding_box = json.dumps(bounding_box)
# embeddings = json.dumps(np.random.rand(512).tolist())
# con.insert_inform_meta_data_image(id_images, bounding_box, embeddings)

# bounding_box, embeddings = con.get_meta_image()
# print (bounding_box)

