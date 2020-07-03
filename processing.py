import os
from connection import DatabaseConnection
import csv
from datetime import datetime

class Processing(object):
	"""docstring for Processing"""
	def __init__(self):
		super(Processing).__init__()
		self.database_connection = DatabaseConnection()

	def check_login(self, username, password):
		return self.database_connection.check_login(username, password)

	def get_class_session_from_teacher(self, memberID):
		return self.database_connection.get_teachID_from_memberID(memberID)

	def get_information_sections(self, teacherID):
		return self.database_connection.get_information_sections(teacherID)
	
	def get_statistic_remart_student(self, sectionID):
		return self.database_connection.get_statistic_remart_student(sectionID)

	def add_student(self, data):
		self.database_connection.insert_student(data)

	def add_teacher(self, data):
		self.database_connection.insert_teacher(data)

	def add_remark(self, data):
		self.database_connection.insert_remark_student(data)

	def add_image_data(self, data):
		self.database_connection.insert_inform_image(data)

	def get_students_from_class_session(self, sectionID):
		return self.database_connection.get_students_from_class_session(sectionID)

	def get_information_students(self, list_studentID):
		data_student = []
		for studentID in list_studentID:
			name = self.database_connection.get_inform_student(studentID)
			data_student.append([studentID, name])
		return data_student

	def get_embeddings_students(self, list_studentID):
		data_image = []
		for studentID in list_studentID:
			data = self.database_connection.get_embeddings_student(studentID)
			if data is not None:
				data_image.extend(data)
		return data_image

	def write_result_csv_section(self, sectionID):
		data = self.database_connection.get_statistic_remart_student(sectionID)
		timestamp = int(datetime.timestamp(datetime.now()))
		date = str(datetime.fromtimestamp(timestamp))
		filename = os.path.join("file_writer", date + ".csv")
		with open(filename, "w") as file:
			writer = csv.writer(file, delimiter = ',')
			writer.writerow(["STT", "MSV", "Tên sinh viên", "Môn học", 'số tín chỉ', 'tiết bắt đầu', 'ngày', 'điểm danh'])
			i = 1
			if data is None:
				return filename
			for row in data:
				data_write = []
				data_write.extend([i])
				data_write.extend(list(row))
				writer.writerow(data_write)
				i += 1
		return filename

	def get_information_group_from_teachID(self, teacherID):
		return self.database_connection.get_information_group_from_teachID(teacherID)

	def get_group_from_teachID(self, teacherID):
		data = self.database_connection.get_information_group_from_teachID(teacherID)
		map_check = {}
		message = []
		for result in data:
			if map_check.get(result[1]) is None:
				message.append(result)
				map_check[result[1]] = 1
		data_tmp = {}
		data_tmp['groupID'] = []
		data_tmp['groupName'] = []
		data_tmp['subjectName'] = []
		data_tmp['personName'] = []
		data_tmp['credits'] = []
		for sectionID, groupID, groupName, subjectName, credits, personName in message:
			data_tmp['groupID'].append(groupID)
			data_tmp['groupName'].append(groupName)
			data_tmp['subjectName'].append(subjectName)
			data_tmp['personName'].append(personName)
			data_tmp['credits'].append(credits)
		return data_tmp

	def write_result_csv_group(self, groupID):
		list_sectionID = self.database_connection.get_section_from_groupID(groupID)
		timestamp = int(datetime.timestamp(datetime.now()))
		date = str(datetime.fromtimestamp(timestamp))
		filename = os.path.join("file_writer", date + ".csv")
		i = 0
		data_map = {}
		list_studentCode = []
		with open(filename, "w") as file:
			writer = csv.writer(file, delimiter = ',')
			if list_sectionID is None:
				return filename
			for sectionID in list_sectionID:
				data = self.database_connection.get_statistic_remart_student(sectionID)
				if data is None:
					continue
				for elements in data:
					if data_map.get(elements[0]) is None:
						data_map[elements[0]] = []
						list_studentCode.append(elements[0])
					data_map[elements[0]].append(elements)
			data_result = []
			list_time = []
			i = 1
			for studentCode in list_studentCode:
				tmp = []
				index = 0
				for elements in data_map.get(studentCode):
					# print (elements)
					if index == 0:
						tmp = list(elements)[:4]
						tmp.append(elements[-1])
					else :
						tmp.append(elements[-1])
					index += 1
					if i == 1:
						list_time.append((elements[5] + " - tiết " + str(elements[4])))
				data_result.append(tmp)
				i += 1
			title = ["STT", "MSV", "Tên sinh viên", "Môn học", 'số tín chỉ']
			title.extend(list_time)
			writer.writerow(title)
			i = 1
			for row in data_result:
				data_write = []
				data_write.extend([i])
				data_write.extend(list(row))
				writer.writerow(data_write)
				i += 1
		return filename