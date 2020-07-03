import os
import mysql.connector as mysql_db
import cv2
import base64
import json
import numpy as np
import csv

class DatabaseConnection(object):
	"""docstring for DatabaseConnection"""
	def __init__(self, host = "localhost", username = "root", password = "",
				db = "face_recognition_pthtttql", port = 3306):
		super(DatabaseConnection, self).__init__()
		self.connect = mysql_db.connect(host=host, username=username,
                                        password=password,
                                        db=db,
                                        port=port)
		#face_recognition_pthtttql
		# database_example
		self.connect.autocommit = True

	def insert_teacher(self, data):
		id_people = self.insert_people(data)
		data['personID'] = int(id_people)
		roleID = self.check_role(data.get('roleName'))
		data['roleID'] = int(roleID)

		id_member = self.insert_member(data)

		name_table = "Teacher"
		list_parammeter = ['personID', 'specialize']
		self.insert_overall(data, name_table, list_parammeter)
		return "Sucessul"

	def insert_student(self, data):
		id_people = self.insert_people(data)
		data['personID'] = int(id_people)
		gradeID = self.check_grade(data.get('gradeName'))
		if gradeID is None:
			gradeID = self.insert_grade(data.get('gradeName'))
		data['gradeID'] = int(gradeID)
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		list_parammeter = ['personID', 'gradeID', 'studentCode']
		keyword = ",".join(list_parammeter)
		tmp_key = []
		for i in range(len(list_parammeter)):
			tmp_key.append("%s")
		value_key = ",".join(tmp_key)
		sql = "INSERT INTO Student (" +  keyword + ") VALUES (" + value_key + ")" 
		val = []
		for name in list_parammeter:
			val.append(data.get(name))
		mycursor.execute(sql, tuple(val))
		self.connect.commit()
		return "Sucessul"

	def insert_people(self, data):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		list_parammeter = ['personName', 'doB', 'gender', 'email', 'contactMobile', 'address']
		keyword = ",".join(list_parammeter)
		tmp_key = []
		for i in range(len(list_parammeter)):
			tmp_key.append("%s")
		value_key = ",".join(tmp_key)
		sql = "INSERT INTO People (" +  keyword + ") VALUES (" + value_key + ")" 
		val = []
		for name in list_parammeter:
			val.append(data.get(name))
		mycursor.execute(sql, tuple(val))
		self.connect.commit()
		id_people = mycursor.lastrowid
		return id_people

	def check_grade(self, gradeName):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT gradeID FROM Grade WHERE gradeName like %s"
		mycursor.execute(sql, [gradeName])
		myresult = mycursor.fetchall()
		if len(myresult) > 0:
			for gradeID in myresult:
				return gradeID[0]
		return None

	def insert_grade(self, gradeName):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "INSERT INTO Grade (gradeName) VALUES (%s)"
		val = (gradeName, )
		mycursor.execute(sql, val)
		self.connect.commit()  
		gradeID = mycursor.lastrowid
		return gradeID

	def check_role(self, roleName):
		return 1

	def insert_member(self, data):
		name_table = "Member"
		list_parammeter = ['userName', 'password', 'personID', 'roleID']
		self.insert_overall(data, name_table, list_parammeter)

	def insert_remark_student(self, data):
		id_attendance = self.insert_attendance(data)
		sectionID = data.get('sectionID')
		startedTime = data.get('startedTime')
		endedTime = data.get('endedTime')
		self.update_class_session(sectionID)
		data_sub = {}
		for studentID, isAttendanced in data.get('remark'):
			data_sub['attendanceID'] = id_attendance
			data_sub['sectionID'] = sectionID
			data_sub['startedTime'] = startedTime
			data_sub['endedTime'] = endedTime
			data_sub['studentID'] = studentID
			data_sub['isAttendanced'] = isAttendanced
			self.insert_remark(data_sub)

	def insert_attendance(self, data):
		name_table = "Attendance"
		list_parammeter = ["sectionID", "startedTime", "endedTime"]
		id_attendance = self.insert_overall(data, name_table, list_parammeter)
		return id_attendance

	def insert_remark(self, data):
		name_table = "Remark"
		list_parammeter = ["attendanceID", "isAttendanced", "studentID"]
		self.insert_overall(data, name_table, list_parammeter)

	def check_login(self, username, password):
		return self.get_user_using(username, password)

	def get_user_using(self, username, password):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT Member.memberID, Member.personID, Member.roleID, Role.roleName FROM Member, Role WHERE userName like %s and password like %s and Member.roleID = Role.roleID"
		mycursor.execute(sql, [username, password])
		myresult = mycursor.fetchall()
		data = {}
		if len(myresult) > 0:
			for memberID, personID, roleID, roleName in myresult:
				data['memberID'] = memberID
				data['personID'] = personID
				data['roleID'] = roleID
				data['roleName'] = roleName
				return data
		return None


	def insert_inform_image(self, data):
		# cv2.imwrite("1.png", image)
		# with open("1.png", 'rb') as file:
		# 	image = base64.b64encode(file.read())
		name_table = "Image"
		list_parammeter = ["studentID", "bounding_box", "embeddings", "image"]
		self.insert_overall(data, name_table, list_parammeter)

	def insert_overall(self, data, name_table, list_parammeter):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		keyword = ",".join(list_parammeter)
		tmp_key = []
		for i in range(len(list_parammeter)):
			tmp_key.append("%s")
		value_key = ",".join(tmp_key)
		sql = "INSERT INTO " + name_table +  " (" +  keyword + ") VALUES (" + value_key + ")" 
		val = []
		for name in list_parammeter:
			val.append(data.get(name))
		mycursor.execute(sql, tuple(val))
		self.connect.commit()
		id_insert = mycursor.lastrowid
		return id_insert

	def get_students_from_class_session(self, sectionID):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT GroupStudent.studentID FROM ClassSection, GroupStudent WHERE "
		sql += "ClassSection.sectionID = %s and GroupStudent.groupID = ClassSection.groupID"
		mycursor.execute(sql, [sectionID])
		myresult = mycursor.fetchall()
		output = {}
		output['studentID'] = []
		if len(myresult) > 0:
			for studentID in myresult:
				output['studentID'].append(studentID[0])
			return output
		return None

	def get_inform_student(self, studentID):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT People.personName FROM Student, People WHERE People.personID = Student.personID and Student.studentID = %s"
		mycursor.execute(sql, [studentID])
		myresult = mycursor.fetchall()
		if len(myresult) > 0:
			for personID in myresult:
				return personID[0]
		return None

	def get_embeddings_student(self, studentID):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT Image.embeddings FROM Image, Student WHERE Student.studentID = Image.studentID and Student.studentID = %s"
		mycursor.execute(sql, [studentID])
		myresult = mycursor.fetchall()
		data = []
		if len(myresult) > 0:
			for embeddings in myresult:
				data.append([studentID, json.loads(embeddings[0])])
			return data
		return None

	def update_class_session(self, sectionID):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "UPDATE ClassSection SET attendanceStatus = 1 WHERE sectionID = %s"
		mycursor.execute(sql, [sectionID])
		self.connect.commit()

	def get_teachID_from_memberID(self, memberID):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT Teacher.teacherID FROM Teacher, People, Member WHERE Teacher.personID = People.personID and People.personID = Member.personID and Member.memberID = %s"
		mycursor.execute(sql, [memberID])
		myresult = mycursor.fetchall()
		data = []
		if len(myresult) == 1:
			for teacherID in myresult:
				return teacherID[0]
		return None

	def get_information_sections(self, teacherID):
		data_section = self.get_class_session_from_teacher(teacherID)
		if data_section is None:
			return None
		data_tmp = {}
		data_tmp['sectionID'] = []
		data_tmp['groupName'] = []
		data_tmp['subjectName'] = []
		data_tmp['credits'] = []
		data_tmp['weekDay'] = []
		data_tmp['startSlot'] = []
		data_tmp['personName'] = []
		data_tmp['attendanceStatus'] = []
		data_tmp['startedTime'] = []
		data_tmp['endedTime'] = []
		for sectionID, groupName, subjectName, credits, weekDay, startSlot, personName, attendanceStatus in data_section:
			if attendanceStatus == 0:
				startedTime = ""
				endedTime = ""
			else :
				startedTime, endedTime = self.get_time_start_end_from_attendance(sectionID)
			data_tmp['sectionID'].append(sectionID)
			data_tmp['groupName'].append(groupName)
			data_tmp['subjectName'].append(subjectName)
			data_tmp['credits'].append(credits)
			data_tmp['weekDay'].append(weekDay)
			data_tmp['startSlot'].append(startSlot)
			data_tmp['personName'].append(personName)
			data_tmp['attendanceStatus'].append(attendanceStatus)
			data_tmp['startedTime'].append(startedTime)
			data_tmp['endedTime'].append(endedTime)
		return data_tmp

	def get_class_session_from_teacher(self, teacherID):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT ClassSection.sectionID, GroupSubject.groupName, Subject.subjectName, Subject.credits, "
		sql += "ClassSection.weekDay, ClassSection.startSlot, People.personName, ClassSection.attendanceStatus "
		sql += "FROM People, Teacher, ClassSection, GroupSubject, Subject "
		sql += "WHERE Teacher.teacherID = %s and Teacher.personID = People.personID and Teacher.teacherID = ClassSection.teacherID and "
		sql += "ClassSection.groupID = GroupSubject.groupID and GroupSubject.subjectID = Subject.subjectID"
		mycursor.execute(sql, [teacherID])
		myresult = mycursor.fetchall()
		data = []
		if len(myresult) > 0:
			for result in myresult:
				data.append(result)
			return data
		return None

	def get_time_start_end_from_attendance(self, sectionID):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT Attendance.startedTime, Attendance.endedTime FROM Attendance, ClassSection WHERE Attendance.sectionID = ClassSection.sectionID and Attendance.sectionID = %s"
		mycursor.execute(sql, [sectionID])
		myresult = mycursor.fetchall()
		data = []
		if len(myresult) > 0:
			start_final = ""
			end_final = ""
			i = 0
			for startedTime, endedTime in myresult:
				i += 1
				if i == 1:
					start_final = startedTime
				end_final = endedTime
			return start_final, end_final
		return "", ""

	def get_statistic_remart_student(self, sectionID):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT Student.studentCode, People.personName, Subject.subjectName, Subject.credits, ClassSection.startSlot, ClassSection.weekDay, Remark.isAttendanced "
		sql += "FROM ClassSection, Attendance, Remark, Student, People, Subject, GroupSubject WHERE "
		sql += "ClassSection.sectionID = %s and ClassSection.sectionID = Attendance.sectionID and "
		sql += "Attendance.attendanceID = Remark.attendanceID and Remark.studentID = Student.studentID and "
		sql += "Student.personID = People.personID and Subject.subjectID = GroupSubject.subjectID and "
		sql += "GroupSubject.groupID = ClassSection.groupID"
		mycursor.execute(sql, [sectionID])
		myresult = mycursor.fetchall()
		data = []
		map_data = {}
		list_student = []
		if len(myresult) > 0:
			for result in myresult:
				# print (f"result = {result}")
				if map_data.get(result[0]) is None:
					map_data[result[0]] = result
					list_student.append(result[0])
				else :
					if map_data.get(result[0])[-1] == 0 and result[-1] == 1:
						map_data[result[0]] = result
			for masv in list_student:
				data.append(map_data.get(masv))
			return data
		return None

	def get_information_group_from_teachID(self, teacherID):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT ClassSection.sectionID, GroupSubject.groupID, GroupSubject.groupName, Subject.subjectName, Subject.credits, "
		sql += "People.personName "
		sql += "FROM People, Teacher, ClassSection, GroupSubject, Subject "
		sql += "WHERE Teacher.teacherID = %s and Teacher.personID = People.personID and Teacher.teacherID = ClassSection.teacherID and "
		sql += "ClassSection.groupID = GroupSubject.groupID and GroupSubject.subjectID = Subject.subjectID"
		mycursor.execute(sql, [teacherID])
		myresult = mycursor.fetchall()
		data = []
		if len(myresult) > 0:
			for result in myresult:
				data.append(result)
			return data
		return None

	def get_section_from_groupID(self, groupID):
		self.connect.ping(reconnect=True)
		mycursor = self.connect.cursor()
		sql = "SELECT ClassSection.sectionID FROM ClassSection, GroupSubject "
		sql += "WHERE ClassSection.groupID = GroupSubject.groupID and GroupSubject.groupID = %s"
		mycursor.execute(sql, [groupID])
		myresult = mycursor.fetchall()
		data = []
		if len(myresult) > 0:
			for result in myresult:
				data.append(result[0])
			return data
		return None



# con = DatabaseConnection()
# data = con.get_section_from_groupID(2)
# print (data)


# con = DatabaseConnection()
# data = con.get_information_group_from_teachID(3)
# print (data)


# data = {}
# data['']
# con = DatabaseConnection()
# data = con.get_statistic_remart_student(1)
# print (data)
# with open("file_writer/sections.csv", "w") as file:
# 	writer = csv.writer(file, delimiter = ',')
# 	writer.writerow(["STT", "MSV", "Tên sinh viên", "Môn học", 'số tín chỉ', 'tiết bắt đầu', 'ngày', 'điểm danh'])
# 	i = 1
# 	for row in data:
# 		data_write = []
# 		data_write.extend([i])
# 		data_write.extend(list(row))
# 		writer.writerow(data_write)
# 		i += 1
# print (f"out = {out}")
# memberID = "4"
# print (con.get_teachID_from_memberID(memberID))
# con = DatabaseConnection()
# data = con.get_class_session_from_teacher(3)
# print (data)
# data = {}
# data['sectionID'] = 9
# output = con.get_students_from_class_session(data)
# print (output)
# username = "admin"
# password = "123"
# message = con.get_user_using(username, password)
# print (f"message = {message}")